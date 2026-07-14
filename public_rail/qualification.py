"""Offline structural validation for a qualified AI model profile.

This module validates declared registry and evaluation artifacts.  It neither
calls a model nor verifies the issuer identity of those artifacts.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .authorization import parse_utc_timestamp
from .bootstrap import load_json
from .paths import PathError, resolve_below
from .schema import validate as validate_schema


QUALIFICATION_CATEGORIES = frozenset({
    "instruction_following", "coding", "planning", "validation",
    "hallucination", "security", "tool_use", "determinism",
    "long_context", "resource_use",
})


def validate_model_qualification(root: Path, actor: dict[str, Any]) -> list[str]:
    """Validate that an AI actor has a current, complete public eval record."""

    findings: list[str] = []
    registry_ref = actor.get("model_registry_ref")
    evaluation_ref = actor.get("model_evaluation_ref")
    version = actor.get("model_version")
    if not all(isinstance(value, str) and value for value in (registry_ref, evaluation_ref, version)):
        return ["model qualification: AI actor requires registry, evaluation, and model version references."]
    try:
        registry = load_json(resolve_below(root, registry_ref))
        evaluation = load_json(resolve_below(root, evaluation_ref))
    except (PathError, ValueError) as exc:
        return [f"model qualification: {exc}"]
    findings.extend(
        f"MODEL-REGISTRY.json: {finding.removeprefix('model-registry: ')}"
        for finding in validate_schema("model-registry", registry)
    )
    findings.extend(
        f"MODEL-EVALUATION.json: {finding.removeprefix('model-evaluation: ')}"
        for finding in validate_schema("model-evaluation", evaluation)
    )
    model = next(
        (
            item for item in registry.get("models", [])
            if isinstance(item, dict)
            and item.get("model_id") == actor.get("id")
            and item.get("model_version") == version
        ),
        None,
    )
    if model is None:
        findings.append("model qualification: actor model and version are absent from the registry.")
    else:
        if model.get("status") != "QUALIFIED":
            findings.append("model qualification: registered model is not QUALIFIED.")
        if model.get("evaluation_ref") != evaluation_ref:
            findings.append("model qualification: registry evaluation reference mismatch.")
    if evaluation.get("model_id") != actor.get("id") or evaluation.get("model_version") != version:
        findings.append("model qualification: evaluation model identity or version mismatch.")
    if evaluation.get("result") != "QUALIFIED":
        findings.append("model qualification: evaluation result must be QUALIFIED.")
    categories = evaluation.get("categories")
    if not isinstance(categories, list):
        findings.append("model qualification: categories must be a list.")
    else:
        names = [item.get("category") for item in categories if isinstance(item, dict)]
        if set(names) != QUALIFICATION_CATEGORIES or len(names) != len(QUALIFICATION_CATEGORIES):
            findings.append("model qualification: all qualification categories must appear exactly once.")
        for item in categories:
            if not isinstance(item, dict):
                continue
            if item.get("status") != "PASS":
                findings.append(f"model qualification: category {item.get('category')!r} is not PASS.")
            try:
                evidence = resolve_below(root, item.get("evidence_ref"))
                if not evidence.is_file():
                    findings.append(f"model qualification: evidence artifact is missing for {item.get('category')!r}.")
            except PathError as exc:
                findings.append(f"model qualification: {exc}")
    try:
        evaluated_at = parse_utc_timestamp(evaluation.get("evaluated_at"), "evaluated_at")
        valid_until = parse_utc_timestamp(evaluation.get("valid_until"), "valid_until")
        now = datetime.now(timezone.utc)
        if evaluated_at > now:
            findings.append("model qualification: evaluated_at is in the future.")
        if valid_until <= evaluated_at:
            findings.append("model qualification: valid_until must be later than evaluated_at.")
        if now >= valid_until:
            findings.append("model qualification: evaluation is expired.")
    except (TypeError, ValueError) as exc:
        findings.append(f"model qualification: {exc}")
    return findings
