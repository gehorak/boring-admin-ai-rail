"""Local consistency checks for public authorization records."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .bootstrap import load_json
from .documents import read_document, sha256
from .paths import resolve_below
from .schema import validate as validate_schema


def scope_hash(scope: object) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(scope, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def parse_utc_timestamp(value: object, field: str) -> datetime:
    """Parse an ISO-8601 instant and reject timezone-less values."""

    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must use ISO-8601 with a timezone.")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field} must use ISO-8601 with a timezone.") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include Z or an explicit UTC offset.")
    return parsed.astimezone(timezone.utc)


def expected_decision_owner_ref(root: Path) -> str:
    """Return the immutable public reference for the frozen project owner."""

    project = read_document(root / "PROJECT.md")
    owner_id = project.metadata.get("Owner-ID")
    if not owner_id:
        raise ValueError("PROJECT.md: missing Owner-ID.")
    return f"PROJECT.md#owner-id:{owner_id}"


def validate_authorization(root: Path, request: dict[str, Any], workspace_id: str) -> list[str]:
    findings: list[str] = []
    try:
        path = resolve_below(root, request.get("authorization_ref"))
        record = load_json(path)
    except ValueError as exc:
        return [f"Authorization record: {exc}"]
    findings.extend(
        f"AUTHORIZATION.json: {finding.removeprefix('authorization: ')}"
        for finding in validate_schema("authorization", record)
    )
    if record.get("authorization_id") in {None, ""}:
        findings.append("AUTHORIZATION.json: missing authorization_id.")
    if record.get("intent_id") != request.get("intent_id"):
        findings.append("AUTHORIZATION.json: intent_id mismatch.")
    if record.get("workspace_id") != workspace_id:
        findings.append("AUTHORIZATION.json: workspace_id mismatch.")
    if record.get("scope_hash") != scope_hash(request.get("scope")):
        findings.append("AUTHORIZATION.json: scope_hash mismatch.")
    try:
        if record.get("decision_owner_ref") != expected_decision_owner_ref(root):
            findings.append("AUTHORIZATION.json: decision_owner_ref does not match PROJECT.md owner.")
    except ValueError as exc:
        findings.append(f"AUTHORIZATION.json: {exc}")
    manifest = root / "BOOTSTRAP-MANIFEST.json"
    if record.get("bootstrap_manifest_sha256") != sha256(manifest):
        findings.append("AUTHORIZATION.json: bootstrap manifest hash mismatch.")
    if record.get("decision") != "AUTHORIZED":
        findings.append("AUTHORIZATION.json: decision must be AUTHORIZED.")
    actions = record.get("authorized_actions")
    if not isinstance(actions, list) or request.get("action_mode") not in actions:
        findings.append("AUTHORIZATION.json: requested action is not authorized.")
    try:
        issued = parse_utc_timestamp(record.get("issued_at"), "issued_at")
        expires = parse_utc_timestamp(record.get("expires_at"), "expires_at")
        now = datetime.now(timezone.utc)
        if issued > now:
            findings.append("AUTHORIZATION.json: issued_at is in the future.")
        if expires <= issued:
            findings.append("AUTHORIZATION.json: expires_at must be later than issued_at.")
        if now >= expires:
            findings.append("AUTHORIZATION.json: authorization is expired.")
    except (TypeError, ValueError) as exc:
        findings.append(f"AUTHORIZATION.json: {exc}")
    return findings
