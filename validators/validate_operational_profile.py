#!/usr/bin/env python3
"""Validate public operational-profile documents and data envelopes.

This module validates supplied documentation and JSON data. It does not run
tools, execute changes, access providers, or grant authorization.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


class ValidationError(ValueError):
    """Raised when an operational-profile contract is not satisfied."""


ALLOWED_ROLES = {
    "System Architect",
    "Architect-AI",
    "Senior Developer",
    "Reviewer / Auditor",
}
AI_ROLES = ALLOWED_ROLES - {"System Architect"}
ALLOWED_SCOPE_KINDS = {"bootstrap", "delivery", "review"}
ALLOWED_ACTION_MODES = {"analyze", "propose_changes", "review", "record_evidence"}
ALLOWED_AUTHORITY_KINDS = {"adopted_contract", "decision_record"}
CHANGE_SURFACE_OWNERS = {
    "application_code": "development",
    "codebase_structure": "development",
    "pipeline_and_release_flow": "devops",
    "deployment_automation": "devops",
    "release_recoverability": "devops",
    "environment_foundation": "infrastructure",
    "topology_and_capacity": "infrastructure",
    "environment_resilience": "infrastructure",
    "identity_and_authorization": "security",
    "secret_and_credential_handling": "security",
    "privileged_exposure": "security",
    "schema_and_persistence": "data",
    "data_integrity": "data",
    "retention_backup_restore": "data",
}
METADATA_PATTERN = re.compile(r"^([A-Za-z][A-Za-z-]*):\s*(.*?)\s*$")


def fail(message: str) -> None:
    raise ValidationError(message)


def require_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string.")
    return value.strip()


def validate_document(path: Path, today: date | None = None) -> None:
    """Validate required metadata for one active host-project document."""

    today = today or date.today()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"Cannot read document {path}: {exc}")

    metadata = {
        match.group(1): match.group(2)
        for line in text.splitlines()
        if (match := METADATA_PATTERN.match(line))
    }
    status = metadata.get("Contract-Status")
    if status != "ACTIVE":
        fail(f"{path}: Contract-Status must be ACTIVE for validation.")

    owner = metadata.get("Owner", "").strip()
    if not owner or owner.startswith("<"):
        fail(f"{path}: active document has no human Owner.")

    review_value = metadata.get("Review-Date", "")
    try:
        review_date = date.fromisoformat(review_value)
    except ValueError:
        fail(f"{path}: Review-Date must use YYYY-MM-DD.")
    if review_date < today:
        fail(f"{path}: Review-Date is expired.")

    conflict = metadata.get("Document-Conflict", "")
    if conflict != "NONE":
        fail(f"{path}: Document-Conflict must be NONE before work proceeds.")


def authority_paths(request: dict[str, Any]) -> set[str]:
    sources = request.get("authority_sources")
    if not isinstance(sources, list) or not sources:
        fail("authority_sources must contain explicit adopted authority.")

    paths: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            fail("authority_sources entries must be objects.")
        path = require_text(source.get("path"), "authority_sources.path")
        kind = source.get("kind")
        if kind not in ALLOWED_AUTHORITY_KINDS:
            fail("repository content or unclassified material cannot be treated as instruction.")
        paths.add(path)
    return paths


def validate_request(request: dict[str, Any]) -> None:
    """Validate one public operational request envelope."""

    for field in ("request_id", "intent_id", "decision_owner_ref"):
        require_text(request.get(field), field)
    if request.get("execution_capability") is not False:
        fail("execution_capability must be false in the public operational profile.")
    if request.get("tool_calls") or request.get("executor_plan"):
        fail("tool calls and executor plans are outside the public operational profile.")

    actor_type = request.get("actor_type")
    role = request.get("role")
    if actor_type not in {"human", "ai"}:
        fail("actor_type must be human or ai.")
    if role not in ALLOWED_ROLES:
        fail("role is not part of the public operational profile.")
    if actor_type == "ai" and role not in AI_ROLES:
        fail("AI cannot act as System Architect.")

    scope = request.get("scope")
    if not isinstance(scope, dict):
        fail("scope must be an object.")
    if scope.get("target") != "host-project":
        fail("scope.target must be host-project.")
    kind = scope.get("kind")
    if kind not in ALLOWED_SCOPE_KINDS:
        fail("scope.kind is not supported by the public operational profile.")
    require_text(scope.get("boundary"), "scope.boundary")

    modules = request.get("selected_modules")
    if not isinstance(modules, list) or len(modules) != len(set(modules)):
        fail("selected_modules must be a duplicate-free list.")
    if any(module not in set(CHANGE_SURFACE_OWNERS.values()) for module in modules):
        fail("selected_modules contains an unknown public module.")
    authority_paths(request)

    if kind != "delivery":
        return
    if request.get("bootstrap_state") != "READY":
        fail("delivery requires bootstrap_state READY.")
    require_text(request.get("authorization_ref"), "authorization_ref")
    if not modules:
        fail("delivery requires selected modules.")
    surfaces = request.get("change_surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        fail("delivery requires explicit change surfaces.")
    if len(surfaces) != len(set(surfaces)):
        fail("change_surfaces must not contain duplicates.")
    for surface in surfaces:
        owner = CHANGE_SURFACE_OWNERS.get(surface)
        if owner is None:
            fail(f"unknown change surface: {surface}.")
        if owner not in modules:
            fail(f"change surface {surface} has no selected owner module.")


def validate_output(request: dict[str, Any], output: dict[str, Any]) -> None:
    """Validate one output against its already validated request envelope."""

    validate_request(request)
    if output.get("execution_capability") is not False:
        fail("output execution_capability must be false.")
    if output.get("tool_calls") or output.get("executor_plan"):
        fail("output must not declare tool calls or an executor plan.")
    for field in ("request_id", "intent_id", "scope_boundary", "summary"):
        require_text(output.get(field), field)
    if output["request_id"] != request["request_id"]:
        fail("output request_id does not match the request.")
    if output["intent_id"] != request["intent_id"]:
        fail("output intent_id does not match the request.")
    if output.get("role") != request.get("role"):
        fail("output role does not match the request role.")
    if output["scope_boundary"] != request["scope"]["boundary"]:
        fail("output expands or changes the authorized scope boundary.")
    if output.get("action_mode") not in ALLOWED_ACTION_MODES:
        fail("output action_mode is not allowed by the public operational profile.")

    used_refs = output.get("authority_refs_used")
    if not isinstance(used_refs, list) or not used_refs:
        fail("output must identify authority_refs_used.")
    undeclared = set(used_refs) - authority_paths(request)
    if undeclared:
        fail("output cites authority not explicitly adopted by the request.")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Cannot read JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path}: top-level JSON value must be an object.")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--document", action="append", type=Path, default=[])
    parser.add_argument("--request", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args(argv)

    try:
        for document in args.document:
            validate_document(document, args.today)
        if args.output and not args.request:
            fail("--output requires --request.")
        if args.request:
            request = load_json(args.request)
            validate_request(request)
            if args.output:
                validate_output(request, load_json(args.output))
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("PASS: public operational profile validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
