"""Workspace, manifest, and derived bootstrap-state validation."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from .documents import AUTHORITATIVE_DOCUMENTS, comma_values, sha256, validate_active_document
from .paths import reject_links
from .results import Result
from .schema import validate as validate_schema

MAX_JSON_BYTES = 1_048_576


def load_json(path: Path) -> dict[str, Any]:
    try:
        if path.stat().st_size > MAX_JSON_BYTES:
            raise ValueError(f"{path.name}: JSON input exceeds {MAX_JSON_BYTES} bytes.")
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.name}: top-level value must be an object.")
    return value


def workspace(root: Path) -> tuple[dict[str, Any] | None, list[str]]:
    path = root / "WORKSPACE.json"
    if not path.is_file():
        return None, ["Missing WORKSPACE.json."]
    try:
        value = load_json(path)
    except ValueError as exc:
        return None, [str(exc)]
    findings = [
        f"WORKSPACE.json: {finding.removeprefix('workspace-binding: ')}"
        for finding in validate_schema("workspace-binding", value)
    ]
    for key in ("workspace_id", "repository_name", "contract_root", "allowed_repository_root", "binding_version"):
        if not isinstance(value.get(key), str) or not value[key] or value[key].startswith("<"):
            findings.append(f"WORKSPACE.json: missing or placeholder {key}.")
    if value.get("binding_version") != "v1":
        findings.append("WORKSPACE.json: binding_version must be v1.")
    if value.get("allowed_repository_root") != ".":
        findings.append("WORKSPACE.json: allowed_repository_root must be '.'.")
    return value, findings


def mapped(project) -> list[str]:
    modules = comma_values(project, "Selected-Modules")
    surfaces = comma_values(project, "Change-Surfaces")
    findings: list[str] = []
    if not modules:
        findings.append("PROJECT.md: Selected-Modules are not explicit.")
    if not surfaces:
        findings.append("PROJECT.md: Change-Surfaces are not explicit.")
    if surfaces and len(surfaces) != len(set(surfaces)):
        findings.append("PROJECT.md: Change-Surfaces contain duplicates.")
    return findings


def manifest(root: Path, expected_workspace: str) -> tuple[dict[str, Any] | None, list[str]]:
    path = root / "BOOTSTRAP-MANIFEST.json"
    if not path.is_file():
        return None, ["Missing BOOTSTRAP-MANIFEST.json."]
    try:
        value = load_json(path)
    except ValueError as exc:
        return None, [str(exc)]
    findings = [
        f"BOOTSTRAP-MANIFEST.json: {finding.removeprefix('bootstrap-manifest: ')}"
        for finding in validate_schema("bootstrap-manifest", value)
    ]
    if value.get("workspace_id") != expected_workspace:
        findings.append("BOOTSTRAP-MANIFEST.json: workspace_id mismatch.")
    documents = value.get("documents")
    if not isinstance(documents, list):
        return value, [*findings, "BOOTSTRAP-MANIFEST.json: documents must be a list."]
    expected = set(AUTHORITATIVE_DOCUMENTS)
    seen = set()
    for item in documents:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            findings.append("BOOTSTRAP-MANIFEST.json: invalid document entry.")
            continue
        name = item["path"]
        seen.add(name)
        document_path = root / name
        if name not in expected or not document_path.is_file():
            findings.append(f"BOOTSTRAP-MANIFEST.json: invalid document path {name}.")
        elif item.get("sha256") != sha256(document_path):
            findings.append(f"BOOTSTRAP-MANIFEST.json: hash mismatch for {name}.")
    if seen != expected:
        findings.append("BOOTSTRAP-MANIFEST.json: authoritative document set is incomplete.")
    return value, findings


def status(root: Path, today: date | None = None) -> Result:
    today = today or date.today()
    link_paths = reject_links(root) if root.is_dir() else []
    if link_paths:
        return Result("BLOCKED", [f"Symbolic link or junction: {path}." for path in link_paths])
    try:
        root = root.resolve(strict=True)
    except OSError as exc:
        return Result("BLOCKED", [f"Cannot resolve contract root: {exc}."])
    binding, binding_findings = workspace(root)
    if binding is None or binding_findings:
        return Result("UNPACKED", binding_findings)
    documents = {}
    active_findings: list[str] = []
    for name in AUTHORITATIVE_DOCUMENTS:
        document, findings = validate_active_document(root / name, today)
        if document is not None:
            documents[name] = document
        active_findings.extend(findings)
    if active_findings:
        project = documents.get("PROJECT.md")
        result = "BLOCKED" if (root / "BOOTSTRAP-MANIFEST.json").is_file() and not ((root / "BOOTSTRAP-MANIFEST.json").read_text(encoding="utf-8").find('"documents": []') >= 0) else "UNPACKED"
        if project is not None and project.metadata.get("Contract-Status") == "ACTIVE":
            result = "BLOCKED"
        return Result(result, active_findings, sorted(documents))
    mapping_findings = mapped(documents["PROJECT.md"])
    if mapping_findings:
        return Result("SEEDED", mapping_findings, sorted(documents))
    manifest_value, manifest_findings = manifest(root, binding["workspace_id"])
    if manifest_findings:
        generated_placeholder = manifest_value is not None and manifest_value.get("documents") == []
        result = "MAPPED" if generated_placeholder or not (root / "BOOTSTRAP-MANIFEST.json").is_file() else "BLOCKED"
        return Result(result, manifest_findings, sorted(documents))
    review, review_findings = validate_active_document(root / "BOOTSTRAP-REVIEW.md", today)
    if review is None or review_findings:
        result = "BLOCKED" if (root / "BOOTSTRAP-REVIEW.md").is_file() else "MAPPED"
        return Result(result, review_findings, sorted(documents))
    review_metadata = review.metadata
    required_review_fields = ("Review-Record-ID", "Workspace-ID", "Manifest-Ref", "Manifest-SHA256", "Reviewer", "Decision-Owner", "Result", "Reviewed-At", "Valid-Until")
    missing_review_fields = [field for field in required_review_fields if not review_metadata.get(field)]
    if missing_review_fields:
        return Result("BLOCKED", [f"BOOTSTRAP-REVIEW.md: missing {field}." for field in missing_review_fields], sorted(documents))
    if review_metadata.get("Result") != "READY":
        return Result("MAPPED", ["BOOTSTRAP-REVIEW.md: Result must be READY."], sorted(documents))
    if review_metadata.get("Workspace-ID") != binding["workspace_id"]:
        return Result("BLOCKED", ["BOOTSTRAP-REVIEW.md: Workspace-ID mismatch."], sorted(documents))
    manifest_path = root / "BOOTSTRAP-MANIFEST.json"
    if review_metadata.get("Manifest-Ref") != "BOOTSTRAP-MANIFEST.json" or review_metadata.get("Manifest-SHA256") != sha256(manifest_path):
        return Result("BLOCKED", ["BOOTSTRAP-REVIEW.md: manifest reference or hash mismatch."], sorted(documents))
    try:
        if date.fromisoformat(review_metadata["Valid-Until"]) < today:
            return Result("BLOCKED", ["BOOTSTRAP-REVIEW.md: Valid-Until is expired."], sorted(documents))
    except ValueError:
        return Result("BLOCKED", ["BOOTSTRAP-REVIEW.md: Valid-Until must use YYYY-MM-DD."], sorted(documents))
    return Result("READY", [], sorted(documents) + ["BOOTSTRAP-REVIEW.md", "BOOTSTRAP-MANIFEST.json"])


def freeze(root: Path, manifest_id: str | None = None) -> Result:
    state = status(root)
    if state.result not in {"MAPPED", "READY"}:
        return Result("BLOCKED", state.findings, state.validated_artifacts)
    binding, findings = workspace(root)
    if binding is None or findings:
        return Result("BLOCKED", findings)
    documents = [
        {"path": name, "kind": "project_contract" if name == "PROJECT.md" else "adopted_contract", "sha256": sha256(root / name)}
        for name in AUTHORITATIVE_DOCUMENTS
    ]
    value = {"manifest_id": manifest_id or f"bootstrap-{binding['workspace_id']}", "workspace_id": binding["workspace_id"], "project_state": "bootstrap", "documents": documents}
    (root / "BOOTSTRAP-MANIFEST.json").write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return Result("STRUCTURALLY_VALID", [], [item["path"] for item in documents] + ["BOOTSTRAP-MANIFEST.json"])
