"""Provider-neutral, type-aware evidence-chain validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .bootstrap import load_json, status
from .documents import sha256
from .paths import PathError, resolve_below
from .requests import validate_output
from .results import Result
from .schema import validate as validate_schema


def _load_artifact(root: Path, record: dict[str, Any], findings: list[str]) -> tuple[Path | None, dict[str, Any] | None]:
    record_id = record.get("record_id")
    try:
        artifact = resolve_below(root, record.get("artifact_path"))
        if not artifact.is_file() or record.get("artifact_sha256") != sha256(artifact):
            findings.append(f"evidence: artifact missing or hash mismatch at {record_id}.")
            return None, None
        return artifact, load_json(artifact)
    except (PathError, ValueError) as exc:
        findings.append(f"evidence: {exc}")
        return None, None


def _validate_artifact_schema(name: str, value: dict[str, Any], record_id: object, findings: list[str]) -> None:
    findings.extend(
        f"evidence: {name} artifact at {record_id}: {finding.removeprefix(f'{name}: ')}"
        for finding in validate_schema(name, value)
    )


def validate_evidence(root: Path, evidence_path: Path) -> Result:
    root = Path(root)
    try:
        evidence_path = resolve_below(root, evidence_path.relative_to(root).as_posix())
    except (PathError, ValueError) as exc:
        return Result("BLOCKED", [f"evidence: {exc}"])
    try:
        evidence = load_json(evidence_path)
    except ValueError as exc:
        return Result("BLOCKED", [str(exc)])
    findings: list[str] = validate_schema("evidence", evidence)
    bootstrap = status(root)
    if bootstrap.result != "READY":
        findings.append("evidence: bootstrap is not READY.")
    else:
        try:
            bootstrap_manifest = load_json(root / "BOOTSTRAP-MANIFEST.json")
            if evidence.get("manifest_id") != bootstrap_manifest.get("manifest_id"):
                findings.append("evidence: manifest_id does not match BOOTSTRAP-MANIFEST.json.")
        except ValueError as exc:
            findings.append(f"evidence: {exc}")
    records = evidence.get("records")
    if not isinstance(records, list) or not records:
        return Result("BLOCKED", [*findings, "evidence: records must be a non-empty list."])
    intent_id = evidence.get("intent_id")
    workspace_id = evidence.get("workspace_id")
    ids: set[str] = set()
    expected_types = ["intent", "authorization", "proposed_output", "review_result", "closure"]
    actual_types = [record.get("record_type") for record in records if isinstance(record, dict)]
    if len(actual_types) > 1 and actual_types[1] == "architect_review":
        expected_types.insert(1, "architect_review")
    expected_index = 0
    previous: str | None = None
    artifacts: dict[str, tuple[Path, dict[str, Any]]] = {}
    proposed_request_ref: str | None = None

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
        artifact, value = _load_artifact(root, record, findings)
        if artifact is None or value is None or not isinstance(record_type, str):
            continue
        artifacts[record_type] = (artifact, value)

        if record_type == "intent":
            _validate_artifact_schema("intent", value, record_id, findings)
            if value.get("intent_id") != intent_id or value.get("workspace_id") != workspace_id:
                findings.append("evidence: intent artifact identity mismatch.")
        elif record_type == "authorization":
            _validate_artifact_schema("authorization", value, record_id, findings)
            if value.get("intent_id") != intent_id or value.get("workspace_id") != workspace_id:
                findings.append("evidence: authorization artifact identity mismatch.")
        elif record_type == "proposed_output":
            request_ref = record.get("request_ref")
            if not isinstance(request_ref, str) or not request_ref:
                findings.append("evidence: proposed_output requires request_ref.")
                continue
            try:
                request_path = resolve_below(root, request_ref)
                output_result = validate_output(root, request_path, artifact)
                if output_result.result != "STRUCTURALLY_VALID":
                    findings.extend(f"evidence: proposed_output {finding}" for finding in output_result.findings)
                request = load_json(request_path)
                if request.get("intent_id") != intent_id or request.get("workspace_id") != workspace_id:
                    findings.append("evidence: proposed_output request identity mismatch.")
                proposed_request_ref = request_ref
            except (PathError, ValueError) as exc:
                findings.append(f"evidence: proposed_output {exc}")
        elif record_type == "review_result":
            _validate_artifact_schema("review-result", value, record_id, findings)
            if value.get("intent_id") != intent_id or value.get("workspace_id") != workspace_id:
                findings.append("evidence: review_result artifact identity mismatch.")
            if record.get("request_ref") != proposed_request_ref:
                findings.append("evidence: review_result does not reference the proposed output request.")
            output = artifacts.get("proposed_output")
            if output is None or value.get("output_sha256") != sha256(output[0]):
                findings.append("evidence: review_result does not bind the proposed output hash.")
            if proposed_request_ref:
                try:
                    request = load_json(resolve_below(root, proposed_request_ref))
                    if value.get("request_id") != request.get("request_id"):
                        findings.append("evidence: review_result request_id mismatch.")
                except (PathError, ValueError) as exc:
                    findings.append(f"evidence: review_result {exc}")
        elif record_type == "closure":
            _validate_artifact_schema("closure", value, record_id, findings)
            if value.get("intent_id") != intent_id or value.get("workspace_id") != workspace_id:
                findings.append("evidence: closure artifact identity mismatch.")
            review = artifacts.get("review_result")
            if review is None or value.get("review_result_sha256") != sha256(review[0]):
                findings.append("evidence: closure does not bind the review result hash.")
            elif value.get("decision") != review[1].get("decision"):
                findings.append("evidence: closure decision does not match review result.")

    required = {"intent", "authorization", "proposed_output", "review_result", "closure"}
    types = {record.get("record_type") for record in records if isinstance(record, dict)}
    final_type = records[-1].get("record_type") if isinstance(records[-1], dict) else None
    if not required <= types or final_type != "closure":
        findings.append("evidence: required chain or final closure is missing.")
    return Result("EVIDENCE_CHAIN_VALID" if not findings else "BLOCKED", findings, [str(evidence_path)])
