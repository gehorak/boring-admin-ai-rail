#!/usr/bin/env python3
"""Verify the exact public adoption package tree and file hashes."""

from __future__ import annotations

import hashlib
import json
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


def validate_relative_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        fail("PUBLIC-MANIFEST.json contains an invalid file path.")

    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        fail(f"PUBLIC-MANIFEST.json contains an unsafe path: {value}")
    return path.as_posix()


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

    files = manifest.get("files")
    if manifest.get("version") != "v0.1.0" or not isinstance(files, list):
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

    print("PASS: public adoption package integrity")


if __name__ == "__main__":
    main()
