"""Scope, authority, request, and output validation without execution."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .authorization import validate_authorization
from .bootstrap import load_json, manifest, status, workspace
from .documents import read_document, sha256, validate_active_document
from .paths import PathError, in_scope, normal_relative, resolve_below
from .results import Result
from .schema import validate as validate_schema


ROLE_ACTIONS = {
    "System Architect": {"authorize", "reject", "narrow_scope"},
    "Architect-AI": {"analyze", "request_clarification"},
    "Senior Developer": {"propose_changes", "record_evidence"},
    "Reviewer / Auditor": {"review", "record_evidence"},
}
MODULE_OWNERS = {
    "application_code": "development", "codebase_structure": "development",
    "pipeline_and_release_flow": "devops", "deployment_automation": "devops", "release_recoverability": "devops",
    "environment_foundation": "infrastructure", "topology_and_capacity": "infrastructure", "environment_resilience": "infrastructure",
    "identity_and_authorization": "security", "secret_and_credential_handling": "security", "privileged_exposure": "security",
    "schema_and_persistence": "data", "data_integrity": "data", "retention_backup_restore": "data",
}


def scope_findings(scope: object) -> list[str]:
    if not isinstance(scope, dict):
        return ["scope must be an object."]
    findings: list[str] = []
    if scope.get("repository_root") != ".":
        findings.append("scope.repository_root must be '.'.")
    for field in ("allowed_paths", "denied_paths", "allowed_change_kinds"):
        if not isinstance(scope.get(field), list) or not scope[field]:
            findings.append(f"scope.{field} must be a non-empty list.")
    for field in ("allowed_paths", "denied_paths"):
        for pattern in scope.get(field, []):
            try:
                normal_relative(pattern.replace("/**", "/placeholder") if isinstance(pattern, str) and pattern.endswith("/**") else pattern)
            except (AttributeError, PathError):
                findings.append(f"scope.{field} contains an unsafe path pattern.")
    return findings


def validate_request(root: Path, request_path: Path) -> Result:
    try:
        request = load_json(request_path)
    except ValueError as exc:
        return Result("BLOCKED", [str(exc)])
    findings: list[str] = validate_schema("request", request)
    for field in ("request_id", "intent_id", "workspace_id", "role", "action_mode", "authorization_ref"):
        if not isinstance(request.get(field), str) or not request[field]:
            findings.append(f"request: missing {field}.")
    if request.get("execution_capability") is not False:
        findings.append("request: execution_capability must be false.")
    if request.get("role") not in ROLE_ACTIONS:
        findings.append("request: unknown role.")
    elif request.get("action_mode") not in ROLE_ACTIONS[request["role"]]:
        findings.append("request: action is not allowed for role.")
    findings.extend(scope_findings(request.get("scope")))
    boot = status(root)
    if boot.result != "READY":
        findings.append("request: bootstrap is not READY.")
    binding, binding_findings = workspace(root)
    findings.extend(binding_findings)
    if binding and request.get("workspace_id") != binding.get("workspace_id"):
        findings.append("request: workspace_id mismatch.")
    manifest_value, manifest_findings = manifest(root, binding["workspace_id"] if binding else "")
    findings.extend(manifest_findings)
    if manifest_value and request.get("bootstrap_manifest_sha256") != sha256(root / "BOOTSTRAP-MANIFEST.json"):
        findings.append("request: bootstrap_manifest_sha256 mismatch.")
    modules = request.get("selected_modules")
    surfaces = request.get("change_surfaces")
    if not isinstance(modules, list) or not modules:
        findings.append("request: selected_modules must be non-empty.")
    if not isinstance(surfaces, list) or not surfaces:
        findings.append("request: change_surfaces must be non-empty.")
    for surface in surfaces if isinstance(surfaces, list) else []:
        if MODULE_OWNERS.get(surface) not in modules:
            findings.append(f"request: {surface} has no selected owner module.")
    authoritative = {item["path"]: item for item in manifest_value.get("documents", [])} if manifest_value else {}
    sources = request.get("authority_sources")
    if not isinstance(sources, list) or not sources:
        findings.append("request: authority_sources must be non-empty.")
    for source in sources if isinstance(sources, list) else []:
        if not isinstance(source, dict) or source.get("kind") not in {"project_contract", "adopted_contract", "decision_record"}:
            findings.append("request: invalid authority source kind.")
            continue
        try:
            path = normal_relative(source.get("path"))
            if source["kind"] != "decision_record":
                if path not in authoritative:
                    findings.append(f"request: authority document is not frozen: {path}.")
                else:
                    document_path = resolve_below(root, path)
                    _, document_findings = validate_active_document(document_path, __import__("datetime").date.today())
                    findings.extend(document_findings)
        except (PathError, ValueError) as exc:
            findings.append(f"request authority: {exc}")
    if binding:
        findings.extend(validate_authorization(root, request, binding["workspace_id"]))
    return Result("AUTHORIZATION_RECORD_CONSISTENT" if not findings else "BLOCKED", findings, boot.validated_artifacts)


def validate_output(root: Path, request_path: Path, output_path: Path) -> Result:
    request_result = validate_request(root, request_path)
    if request_result.result == "BLOCKED":
        return request_result
    request = load_json(request_path)
    try:
        output = load_json(output_path)
    except ValueError as exc:
        return Result("BLOCKED", [str(exc)])
    findings: list[str] = validate_schema("output", output)
    for key in ("request_id", "intent_id", "workspace_id", "role", "action_mode"):
        if output.get(key) != request.get(key):
            findings.append(f"output: {key} mismatch.")
    if output.get("execution_capability") is not False:
        findings.append("output: execution_capability must be false.")
    artifacts = output.get("artifacts")
    if not isinstance(artifacts, list):
        findings.append("output: artifacts must be a list.")
    else:
        scope = request["scope"]
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                findings.append("output: invalid artifact entry.")
                continue
            try:
                path = normal_relative(artifact.get("path"))
                if not in_scope(path, scope["allowed_paths"], scope["denied_paths"]):
                    findings.append(f"output: artifact outside scope: {path}.")
                if artifact.get("change_kind") not in scope["allowed_change_kinds"]:
                    findings.append(f"output: change kind not allowed: {path}.")
            except PathError as exc:
                findings.append(f"output: {exc}")
    return Result("STRUCTURALLY_VALID" if not findings else "BLOCKED", findings, request_result.validated_artifacts)
