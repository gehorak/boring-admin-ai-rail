"""Command-line interface for public bootstrap preflight."""

from __future__ import annotations

import argparse
import json
import sys
from importlib.resources import files
from pathlib import Path

from .bootstrap import freeze, status
from .evidence import validate_evidence
from .paths import is_link_or_junction
from .requests import validate_output, validate_request
from .results import Result


TEMPLATE_NAMES = (
    "PROJECT.md", "PROJECT-CONTEXT.md", "ARCHITECTURE-CANON.md",
    "CODEBASE-VOICE.md", "INTEGRATION-POINTS.md", "BOOTSTRAP-REVIEW.md",
)


def template_root():
    return files("public_rail").joinpath("resources", "templates", "operational")


def emit(result: Result, text_only: bool = False) -> int:
    if text_only:
        print(result.result)
    else:
        print(json.dumps(result.payload(), indent=2, sort_keys=True))
    return 0 if result.result not in {"BLOCKED"} else 1


def _unsafe_init_path(path: Path) -> Path | None:
    """Return a target that is itself a link or junction."""

    path = Path(path)
    return path if is_link_or_junction(path) else None


def init(target: Path, force: bool) -> Result:
    target = target.absolute()
    destinations = [
        *(target / name for name in TEMPLATE_NAMES),
        target / "evidence",
        target / "WORKSPACE.json",
        target / "BOOTSTRAP-MANIFEST.json",
    ]
    for destination in (target, *destinations):
        unsafe = _unsafe_init_path(destination)
        if unsafe is not None:
            return Result("BLOCKED", [f"Refusing to initialize through symbolic link or junction: {unsafe}"])
    if target.exists() and any(target.iterdir()) and not force:
        return Result("BLOCKED", ["Target is not empty; use --force only for explicit overwrite."])
    target.mkdir(parents=True, exist_ok=True)
    for name in TEMPLATE_NAMES:
        destination = target / name
        if destination.exists() and not force:
            return Result("BLOCKED", [f"Refusing to overwrite {name} without --force."])
        destination.write_text(
            template_root().joinpath(name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    (target / "evidence").mkdir(exist_ok=True)
    workspace = {
        "workspace_id": "<workspace-id>", "repository_name": "<repository-name>",
        "contract_root": target.as_posix(), "allowed_repository_root": ".", "binding_version": "v1",
    }
    (target / "WORKSPACE.json").write_text(json.dumps(workspace, indent=2) + "\n", encoding="utf-8")
    (target / "BOOTSTRAP-MANIFEST.json").write_text(json.dumps({"manifest_id": "<manifest-id>", "workspace_id": "<workspace-id>", "project_state": "bootstrap", "documents": []}, indent=2) + "\n", encoding="utf-8")
    return Result("UNPACKED", [], [name for name in TEMPLATE_NAMES] + ["WORKSPACE.json", "BOOTSTRAP-MANIFEST.json", "evidence/"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="public_rail")
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--target", type=Path, required=True)
    init_parser.add_argument("--force", action="store_true")
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--root", type=Path, required=True)
    freeze_parser = subparsers.add_parser("freeze")
    freeze_parser.add_argument("--root", type=Path, required=True)
    freeze_parser.add_argument("--manifest-id")
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--root", type=Path, required=True)
    request_parser = subparsers.add_parser("validate-request")
    request_parser.add_argument("request", type=Path)
    request_parser.add_argument("--root", type=Path, required=True)
    output_parser = subparsers.add_parser("validate-output")
    output_parser.add_argument("request", type=Path)
    output_parser.add_argument("output", type=Path)
    output_parser.add_argument("--root", type=Path, required=True)
    evidence_parser = subparsers.add_parser("validate-evidence")
    evidence_parser.add_argument("evidence", type=Path)
    evidence_parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            return emit(init(args.target, args.force))
        if args.command == "validate":
            state = status(args.root)
            result = Result("STRUCTURALLY_VALID" if state.result in {"MAPPED", "READY"} else state.result, state.findings, state.validated_artifacts)
            return emit(result)
        if args.command == "freeze":
            return emit(freeze(args.root, args.manifest_id))
        if args.command == "status":
            return emit(status(args.root), text_only=True)
        if args.command == "validate-request":
            return emit(validate_request(args.root, args.request))
        if args.command == "validate-output":
            return emit(validate_output(args.root, args.request, args.output))
        return emit(validate_evidence(args.root, args.evidence))
    except Exception:
        return emit(Result("BLOCKED", ["Invalid input or validation failure."]))
