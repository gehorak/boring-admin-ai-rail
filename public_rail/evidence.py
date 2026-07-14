"""Provider-neutral evidence-chain validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .bootstrap import load_json
from .documents import sha256
from .paths import PathError, resolve_below
from .results import Result
from .schema import validate as validate_schema


ORDER = ["intent", "architect_review", "authorization", "proposed_output", "review_result", "closure"]


def validate_evidence(root: Path, evidence_path: Path) -> Result:
    try:
        evidence = load_json(evidence_path)
    except ValueError as exc:
        return Result("BLOCKED", [str(exc)])
    findings: list[str] = validate_schema("evidence", evidence)
    records = evidence.get("records")
    if not isinstance(records, list) or not records:
        return Result("BLOCKED", [*findings, "evidence: records must be a non-empty list."])
    intent_id = evidence.get("intent_id")
    workspace_id = evidence.get("workspace_id")
    ids: set[str] = set()
    expected_index = 0
    actual_types = [record.get("record_type") for record in records if isinstance(record, dict)]
    expected_types = ["intent", "authorization", "proposed_output", "review_result", "closure"]
    if len(actual_types) > 1 and actual_types[1] == "architect_review":
        expected_types.insert(1, "architect_review")
    previous: str | None = None
    for record in records:
        if not isinstance(record, dict):
            findings.append("evidence: invalid record entry.")
            continue
        record_id = record.get("record_id")
        if not isinstance(record_id, str) or not record_id or record_id in ids:
            findings.append("evidence: record_id must be unique.")
        else:
            ids.add(record_id)
        record_type = record.get("record_type")
        expected_type = expected_types[expected_index] if expected_index < len(expected_types) else None
        if record_type != expected_type:
            findings.append(f"evidence: invalid record order at {record_id}.")
        else:
            expected_index += 1
        if record.get("previous_record_id") != previous:
            findings.append(f"evidence: broken previous_record_id at {record_id}.")
        previous = record_id if isinstance(record_id, str) else previous
        if record.get("intent_id") != intent_id or record.get("workspace_id") != workspace_id:
            findings.append(f"evidence: intent or workspace mismatch at {record_id}.")
        try:
            artifact = resolve_below(root, record.get("artifact_path"))
            if not artifact.is_file() or record.get("artifact_sha256") != sha256(artifact):
                findings.append(f"evidence: artifact missing or hash mismatch at {record_id}.")
        except PathError as exc:
            findings.append(f"evidence: {exc}")
    required = {"intent", "authorization", "proposed_output", "review_result", "closure"}
    types = {record.get("record_type") for record in records if isinstance(record, dict)}
    if not required <= types or records[-1].get("record_type") != "closure":
        findings.append("evidence: required chain or final closure is missing.")
    return Result("EVIDENCE_CHAIN_VALID" if not findings else "BLOCKED", findings, [str(evidence_path)])
