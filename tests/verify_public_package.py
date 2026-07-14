#!/usr/bin/env python3
"""Verify the exact public adoption package tree and file hashes."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


SEMVER_PATTERN = re.compile(r"^v\d+\.\d+\.\d+$")


def validate_relative_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        fail("PUBLIC-MANIFEST.json contains an invalid file path.")

    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        fail(f"PUBLIC-MANIFEST.json contains an unsafe path: {value}")
    return path.as_posix()


def is_link_or_junction(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or (callable(is_junction) and is_junction())


def main() -> None:
    candidate_root = Path(__file__).resolve().parent.parent
    manifest_path = candidate_root / "PUBLIC-MANIFEST.json"
    if not manifest_path.is_file():
        fail("PUBLIC-MANIFEST.json is missing.")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"PUBLIC-MANIFEST.json cannot be read: {exc}")

    if not isinstance(manifest, dict):
        fail("PUBLIC-MANIFEST.json must contain an object.")

    linked_paths = sorted(
        path.relative_to(candidate_root).as_posix()
        for path in candidate_root.rglob("*")
        if ".git" not in path.relative_to(candidate_root).parts
        and is_link_or_junction(path)
    )
    if linked_paths:
        fail(f"Public package contains symbolic links or junctions: {', '.join(linked_paths)}")

    files = manifest.get("distribution_files")
    control_files = manifest.get("repository_control_files")
    if (
        not isinstance(manifest.get("kit_version"), str)
        or not SEMVER_PATTERN.fullmatch(manifest["kit_version"])
        or not isinstance(manifest.get("template_schema_version"), str)
        or not SEMVER_PATTERN.fullmatch(manifest["template_schema_version"])
        or not isinstance(manifest.get("base_template_schema_version"), str)
        or not SEMVER_PATTERN.fullmatch(manifest["base_template_schema_version"])
        or not isinstance(manifest.get("operational_template_schema_version"), str)
        or not SEMVER_PATTERN.fullmatch(manifest["operational_template_schema_version"])
        or not isinstance(manifest.get("contract_data_schema_version"), str)
        or not SEMVER_PATTERN.fullmatch(manifest["contract_data_schema_version"])
        or not isinstance(files, list)
        or not isinstance(control_files, list)
    ):
        fail("PUBLIC-MANIFEST.json does not describe the expected public package.")

    expected_paths = {"PUBLIC-MANIFEST.json"}
    entries: dict[str, str] = {}
    for entry in files:
        if not isinstance(entry, dict):
            fail("PUBLIC-MANIFEST.json contains an invalid file entry.")
        relative_path = validate_relative_path(entry.get("path"))
        expected_hash = entry.get("sha256")
        if not isinstance(expected_hash, str) or len(expected_hash) != 64:
            fail(f"PUBLIC-MANIFEST.json contains an invalid SHA-256: {relative_path}")
        if relative_path in entries:
            fail(f"PUBLIC-MANIFEST.json contains a duplicate path: {relative_path}")
        entries[relative_path] = expected_hash.lower()
        expected_paths.add(relative_path)

    control_entries: dict[str, str] = {}
    for entry in control_files:
        if not isinstance(entry, dict):
            fail("PUBLIC-MANIFEST.json contains an invalid repository-control entry.")
        relative_path = validate_relative_path(entry.get("path"))
        if not relative_path.startswith(".github/"):
            fail(f"Repository-control path must be under .github/: {relative_path}")
        expected_hash = entry.get("sha256")
        if not isinstance(expected_hash, str) or len(expected_hash) != 64:
            fail(f"PUBLIC-MANIFEST.json contains an invalid repository-control SHA-256: {relative_path}")
        if relative_path in entries:
            fail(f"PUBLIC-MANIFEST.json duplicates a distribution path: {relative_path}")
        if relative_path in control_entries:
            fail(f"PUBLIC-MANIFEST.json contains a duplicate path: {relative_path}")
        control_entries[relative_path] = expected_hash.lower()
        expected_paths.add(relative_path)

    actual_paths = {
        path.relative_to(candidate_root).as_posix()
        for path in candidate_root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(candidate_root).parts
    }
    missing = sorted(expected_paths - actual_paths)
    unexpected = sorted(actual_paths - expected_paths)
    if missing or unexpected:
        fail(
            "Public package tree mismatch. "
            f"Missing: {', '.join(missing) or 'none'}; "
            f"unexpected: {', '.join(unexpected) or 'none'}"
        )

    for relative_path, expected_hash in entries.items():
        actual_hash = sha256(candidate_root / relative_path)
        if actual_hash != expected_hash:
            fail(f"Hash mismatch: {relative_path}")

    for relative_path, expected_hash in control_entries.items():
        actual_hash = sha256(candidate_root / relative_path)
        if actual_hash != expected_hash:
            fail(f"Repository-control hash mismatch: {relative_path}")

    print("PASS: public adoption package integrity")


if __name__ == "__main__":
    main()
