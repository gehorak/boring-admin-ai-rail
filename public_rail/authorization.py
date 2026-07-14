"""Local consistency checks for public authorization records."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .bootstrap import load_json
from .documents import sha256
from .paths import resolve_below
from .schema import validate as validate_schema


def scope_hash(scope: object) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(scope, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


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
    manifest = root / "BOOTSTRAP-MANIFEST.json"
    if record.get("bootstrap_manifest_sha256") != sha256(manifest):
        findings.append("AUTHORIZATION.json: bootstrap manifest hash mismatch.")
    if record.get("decision") != "AUTHORIZED":
        findings.append("AUTHORIZATION.json: decision must be AUTHORIZED.")
    actions = record.get("authorized_actions")
    if not isinstance(actions, list) or request.get("action_mode") not in actions:
        findings.append("AUTHORIZATION.json: requested action is not authorized.")
    try:
        expires = datetime.fromisoformat(str(record.get("expires_at", "")).replace("Z", "+00:00"))
        if expires < datetime.now(timezone.utc):
            findings.append("AUTHORIZATION.json: authorization is expired.")
    except ValueError:
        findings.append("AUTHORIZATION.json: expires_at must use ISO-8601.")
    return findings
