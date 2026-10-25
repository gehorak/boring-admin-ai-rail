#!/usr/bin/env python3
"""Verify the standalone generated public distribution without private inputs."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
PUBLIC_MANIFEST_PATH = "PUBLIC-MANIFEST.json"
EXPORT_REPORT_PATH = "PUBLIC-EXPORT-REPORT.json"
ALLOWED_CLASSIFICATIONS = frozenset(
    {
        "PUBLIC_RUNTIME",
        "PUBLIC_RESOURCE",
        "PUBLIC_TEST",
        "PUBLIC_DOCUMENTATION",
        "PUBLIC_REPOSITORY_METADATA",
    }
)
ALLOWED_IP_CLASSIFICATIONS = frozenset({"PUBLIC_CONTRACT", "PUBLIC_REFERENCE"})
PROPRIETARY_CONTENT_MARKERS = (
    b"internal" + b"_rail",
    b"risk scoring " + b"threshold",
    b"private policy " + b"bundle",
    b"production model qualification " + b"methodology",
    b"task-routing " + b"strategy",
)


class VerificationError(ValueError):
    """Raised for an invalid or altered generated public distribution."""


def fail(message: str) -> None:
    """Write one controlled diagnostic and stop with a failing status."""

    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    """Calculate a file digest without loading an unbounded file into memory."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_link_or_junction(path: Path) -> bool:
    """Treat Windows junctions like symbolic links at the package boundary."""

    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or (callable(is_junction) and is_junction())


def safe_relative_path(value: object, label: str) -> str:
    """Validate a portable path within the public distribution root."""

    if not isinstance(value, str) or not value or "\\" in value:
        raise VerificationError(f"{label} must be a non-empty POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise VerificationError(f"{label} must remain below the distribution root: {value}")
    return path.as_posix()


def read_json(path: Path, label: str) -> Mapping[str, Any]:
    """Load a UTF-8 JSON object with a controlled public-facing error."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"{label} cannot be read as UTF-8 JSON: {error}") from error
    if not isinstance(value, Mapping):
        raise VerificationError(f"{label} must be a JSON object")
    return value


def discovered_files(root: Path) -> set[str]:
    """Enumerate ordinary files while refusing unsupported filesystem entries."""

    if is_link_or_junction(root):
        raise VerificationError("Public distribution root must not be a symbolic link or junction")
    files: set[str] = set()
    pending = [root]
    while pending:
        current = pending.pop()
        for child in current.iterdir():
            relative = child.relative_to(root).as_posix()
            if relative == ".git" or relative.startswith(".git/"):
                continue
            if is_link_or_junction(child):
                raise VerificationError(f"Public distribution contains a symbolic link or junction: {relative}")
            if child.is_dir():
                pending.append(child)
            elif child.is_file():
                files.add(relative)
            else:
                raise VerificationError(f"Public distribution contains an unsupported file type: {relative}")
    return files


def require_sha256(value: object, label: str) -> str:
    """Require one canonical lower-case SHA-256 value."""

    if not isinstance(value, str) or not SHA256_PATTERN.fullmatch(value):
        raise VerificationError(f"{label} must be a lower-case SHA-256 digest")
    return value


def require_commit(value: object, label: str) -> str:
    """Require one full immutable Git commit identifier."""

    if not isinstance(value, str) or not COMMIT_PATTERN.fullmatch(value):
        raise VerificationError(f"{label} must be a full lower-case Git commit ID")
    return value


def validate_source_identity(value: object, manifest: Mapping[str, Any]) -> None:
    """Check public provenance fields without requiring a private checkout."""

    if not isinstance(value, Mapping):
        raise VerificationError("source_identity must be an object")
    for field in ("internal_baseline_tag", "candidate_source_sha", "approved_source_status"):
        if not isinstance(value.get(field), str) or not value[field]:
            raise VerificationError(f"source_identity is missing {field}")
    require_commit(value.get("internal_baseline_commit"), "source_identity internal_baseline_commit")
    require_commit(value.get("candidate_source_sha"), "source_identity candidate_source_sha")
    if value.get("candidate_source_sha") != manifest.get("source_commit"):
        raise VerificationError("source_identity candidate_source_sha does not match source_commit")
    if value.get("internal_baseline_tag") != manifest.get("source_tag"):
        raise VerificationError("source_identity internal_baseline_tag does not match source_tag")
    if value.get("internal_baseline_commit") != manifest.get("source_baseline_commit"):
        raise VerificationError("source_identity internal_baseline_commit does not match source_baseline_commit")
    for field in ("pr_head_sha", "ci_integration_sha"):
        item = value.get(field)
        if item is not None:
            require_commit(item, f"source_identity {field}")
    if value.get("pr_head_sha") is not None and value.get("pr_head_sha") != value.get("candidate_source_sha"):
        raise VerificationError("source_identity pr_head_sha does not match candidate_source_sha")
    if value.get("approved_source_status") != "HOLD" or "approved_export_source_sha" in value:
        raise VerificationError("source_identity must preserve the external human approval HOLD")


def validate_manifest(manifest: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    """Validate source provenance and construct the exact allowed inventory."""

    required_strings = ("manifest_id", "public_repository", "source_tag", "license")
    if manifest.get("schema_version") != "public-manifest/v2":
        raise VerificationError("PUBLIC-MANIFEST.json has an unsupported schema_version")
    for field in required_strings:
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            raise VerificationError(f"PUBLIC-MANIFEST.json field {field} must be a non-empty string")
    require_commit(manifest.get("source_commit"), "PUBLIC-MANIFEST.json source_commit")
    require_commit(manifest.get("source_baseline_commit"), "PUBLIC-MANIFEST.json source_baseline_commit")
    require_sha256(manifest.get("export_configuration_sha256"), "PUBLIC-MANIFEST.json export_configuration_sha256")
    if manifest.get("license") != "MIT":
        raise VerificationError("PUBLIC-MANIFEST.json effective license must be MIT")
    validate_source_identity(manifest.get("source_identity"), manifest)
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise VerificationError("PUBLIC-MANIFEST.json files must be a non-empty array")

    records: dict[str, Mapping[str, Any]] = {}
    folded_paths: set[str] = set()
    for index, entry in enumerate(files):
        if not isinstance(entry, Mapping):
            raise VerificationError(f"PUBLIC-MANIFEST.json files[{index}] must be an object")
        path = safe_relative_path(entry.get("path"), f"PUBLIC-MANIFEST.json files[{index}].path")
        folded = path.casefold()
        if path in records or folded in folded_paths:
            raise VerificationError(f"PUBLIC-MANIFEST.json contains duplicate or colliding path: {path}")
        folded_paths.add(folded)
        if entry.get("classification") not in ALLOWED_CLASSIFICATIONS:
            raise VerificationError(f"PUBLIC-MANIFEST.json has an unsupported classification: {path}")
        if entry.get("ip_classification") not in ALLOWED_IP_CLASSIFICATIONS:
            raise VerificationError(f"PUBLIC-MANIFEST.json has an unsupported IP classification: {path}")
        require_sha256(entry.get("sha256"), f"PUBLIC-MANIFEST.json files[{index}].sha256")
        has_source = isinstance(entry.get("source_path"), str)
        has_generator = isinstance(entry.get("generated_by"), str)
        if has_source == has_generator:
            raise VerificationError(f"PUBLIC-MANIFEST.json file must have exactly one source or generator: {path}")
        records[path] = entry

    report = records.get(EXPORT_REPORT_PATH)
    if report is None or report.get("generated_by") != "export_report":
        raise VerificationError("PUBLIC-MANIFEST.json must include the generated export report")
    return records


def validate_report(report: Mapping[str, Any], manifest: Mapping[str, Any], records: Mapping[str, Mapping[str, Any]]) -> None:
    """Verify that report provenance and per-file claims match the public manifest."""

    if report.get("schema_version") != "public-export-report/v2":
        raise VerificationError("PUBLIC-EXPORT-REPORT.json has an unsupported schema_version")
    for field in ("source_commit", "source_tag", "source_baseline_commit", "public_repository", "export_configuration_sha256", "license"):
        if report.get(field) != manifest.get(field):
            raise VerificationError(f"PUBLIC-EXPORT-REPORT.json does not match PUBLIC-MANIFEST.json: {field}")
    if report.get("source_identity") != manifest.get("source_identity"):
        raise VerificationError("PUBLIC-EXPORT-REPORT.json source identity does not match PUBLIC-MANIFEST.json")
    reported_files = report.get("files")
    if not isinstance(reported_files, list) or report.get("file_count") != len(reported_files):
        raise VerificationError("PUBLIC-EXPORT-REPORT.json has an invalid file inventory")
    report_paths: set[str] = set()
    for index, entry in enumerate(reported_files):
        if not isinstance(entry, Mapping):
            raise VerificationError(f"PUBLIC-EXPORT-REPORT.json files[{index}] must be an object")
        path = safe_relative_path(entry.get("destination"), f"PUBLIC-EXPORT-REPORT.json files[{index}].destination")
        if path in report_paths or path == EXPORT_REPORT_PATH:
            raise VerificationError(f"PUBLIC-EXPORT-REPORT.json has a duplicate or invalid path: {path}")
        report_paths.add(path)
        manifest_entry = records.get(path)
        if manifest_entry is None or entry.get("sha256") != manifest_entry.get("sha256"):
            raise VerificationError(f"PUBLIC-EXPORT-REPORT.json file does not match PUBLIC-MANIFEST.json: {path}")
        if entry.get("ip_classification") != manifest_entry.get("ip_classification"):
            raise VerificationError(f"PUBLIC-EXPORT-REPORT.json IP classification does not match PUBLIC-MANIFEST.json: {path}")
    if report_paths != set(records).difference({EXPORT_REPORT_PATH}):
        raise VerificationError("PUBLIC-EXPORT-REPORT.json inventory is incomplete")

    checks = report.get("checks")
    if not isinstance(checks, Mapping):
        raise VerificationError("PUBLIC-EXPORT-REPORT.json checks must be an object")
    for name, check in checks.items():
        if not isinstance(name, str) or not isinstance(check, Mapping):
            raise VerificationError("PUBLIC-EXPORT-REPORT.json check entries must be objects")
        if check.get("status") not in {"EXECUTED", "NOT_EXECUTED"}:
            raise VerificationError(f"PUBLIC-EXPORT-REPORT.json has an invalid check status: {name}")
        if not isinstance(check.get("scope"), str) or not check["scope"].strip():
            raise VerificationError(f"PUBLIC-EXPORT-REPORT.json check is missing scope: {name}")
    publication = report.get("publication_readiness")
    if not isinstance(publication, Mapping):
        raise VerificationError("PUBLIC-EXPORT-REPORT.json is missing publication readiness")
    if publication.get("state") != "HOLD" or publication.get("automatic_approval") is not False:
        raise VerificationError("PUBLIC-EXPORT-REPORT.json must preserve the human publication HOLD")


def validate_content_markers(root: Path, records: Mapping[str, Mapping[str, Any]]) -> None:
    """Reject high-confidence private implementation references in public bytes."""

    for path in records:
        content = (root / path).read_bytes().lower()
        for marker in PROPRIETARY_CONTENT_MARKERS:
            if marker in content:
                raise VerificationError(f"Public distribution contains a proprietary-content marker: {path}")


def verify(root: Path) -> None:
    """Verify a standalone public tree and print one success result."""

    if not root.is_dir():
        raise VerificationError("Public distribution root is not a directory")
    manifest = read_json(root / PUBLIC_MANIFEST_PATH, PUBLIC_MANIFEST_PATH)
    records = validate_manifest(manifest)
    expected_paths = set(records).union({PUBLIC_MANIFEST_PATH})
    actual_paths = discovered_files(root)
    missing = sorted(expected_paths.difference(actual_paths))
    unexpected = sorted(actual_paths.difference(expected_paths))
    if missing or unexpected:
        raise VerificationError(
            "Public distribution inventory mismatch: "
            f"missing: {', '.join(missing) or 'none'}; unexpected: {', '.join(unexpected) or 'none'}"
        )
    for path, entry in records.items():
        if sha256(root / path) != entry["sha256"]:
            raise VerificationError(f"Public distribution SHA-256 mismatch: {path}")
    if (root / "LICENSE").read_text(encoding="utf-8")[:12] != "MIT License\n":
        raise VerificationError("Public distribution LICENSE is not MIT")
    if not (root / "LICENSES" / "PUBLIC-SUBSET-MIT.md").is_file():
        raise VerificationError("Public distribution is missing the MIT subset declaration")
    validate_content_markers(root, records)
    validate_report(read_json(root / EXPORT_REPORT_PATH, EXPORT_REPORT_PATH), manifest, records)


def main() -> int:
    """Run verification in the generated distribution root."""

    try:
        verify(Path(__file__).resolve().parents[1])
    except VerificationError as error:
        fail(str(error))
    print("PASS: public mirror package integrity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
