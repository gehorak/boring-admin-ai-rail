"""Portable path and scope handling that fail closed outside a contract root."""

from __future__ import annotations

import fnmatch
from functools import lru_cache
from pathlib import Path


class PathError(ValueError):
    """Raised for an unsafe, invalid, or out-of-scope path."""


WINDOWS_RESERVED = frozenset('<>:"|?*')


def is_link_or_junction(path: Path) -> bool:
    """Return whether *path* is a symlink or a Windows junction."""

    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or (callable(is_junction) and is_junction())


def reject_links(root: Path) -> list[str]:
    """Return every link below root, including root itself when applicable."""

    findings: list[str] = []
    if is_link_or_junction(root):
        findings.append(".")
        return findings
    if not root.is_dir():
        return findings
    findings.extend(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if is_link_or_junction(path)
    )
    return sorted(findings)


def _parts(value: object, *, allow_glob: bool) -> tuple[str, ...]:
    if not isinstance(value, str) or not value:
        raise PathError("Path must be a non-empty relative POSIX path.")
    if "\x00" in value or "\\" in value:
        raise PathError("Path contains an invalid character.")
    if value.startswith("/") or value.endswith("/"):
        raise PathError("Path must be a normalized relative POSIX path.")
    parts = tuple(value.split("/"))
    if any(part in {"", ".", ".."} for part in parts):
        raise PathError("Path must stay below its declared root.")
    for part in parts:
        if any(character in WINDOWS_RESERVED for character in part):
            if not allow_glob or any(character not in {"*"} for character in part if character in WINDOWS_RESERVED):
                raise PathError("Path contains an invalid path character.")
            if "**" in part and part != "**":
                raise PathError("Double-star must occupy a whole path segment.")
    return parts


def normal_relative(value: object) -> str:
    """Validate an actual path; wildcard characters are never valid here."""

    return "/".join(_parts(value, allow_glob=False))


def normal_glob(value: object) -> str:
    """Validate the intentionally small, segment-based public glob grammar."""

    return "/".join(_parts(value, allow_glob=True))


def resolve_below(root: Path, value: object) -> Path:
    """Return an unresolved path only when every existing component is safe.

    Checking each existing component before canonical resolution prevents a
    regular final file beneath a symlinked parent from escaping the root.
    """

    relative = normal_relative(value)
    root = Path(root)
    if not root.is_dir():
        raise PathError("Contract root must be an existing directory.")
    if is_link_or_junction(root):
        raise PathError("Contract root is a symbolic link or junction.")
    candidate = root.joinpath(*relative.split("/"))
    current = root
    for component in relative.split("/"):
        current = current / component
        if current.exists() or current.is_symlink():
            if is_link_or_junction(current):
                raise PathError(f"Path contains a symbolic link or junction: {relative}")
    try:
        resolved_root = root.resolve(strict=True)
        resolved_candidate = candidate.resolve(strict=False)
    except OSError as exc:
        raise PathError(f"Cannot resolve path safely: {relative}") from exc
    if not resolved_candidate.is_relative_to(resolved_root):
        raise PathError(f"Path escapes its declared root: {relative}")
    return candidate


def _segment_match(value: str, pattern: str) -> bool:
    """Match a single segment; fnmatch never receives a slash-containing path."""

    return fnmatch.fnmatchcase(value, pattern)


def glob_match(path: object, pattern: object) -> bool:
    """Match the documented POSIX-like segment glob grammar.

    ``*`` stays inside a segment.  A complete ``**`` segment matches zero or
    more segments, so ``**/.env`` deliberately includes a root-level ``.env``.
    """

    path_parts = normal_relative(path).split("/")
    pattern_parts = normal_glob(pattern).split("/")

    @lru_cache
    def visit(path_index: int, pattern_index: int) -> bool:
        if pattern_index == len(pattern_parts):
            return path_index == len(path_parts)
        part = pattern_parts[pattern_index]
        if part == "**":
            return visit(path_index, pattern_index + 1) or (
                path_index < len(path_parts) and visit(path_index + 1, pattern_index)
            )
        return (
            path_index < len(path_parts)
            and _segment_match(path_parts[path_index], part)
            and visit(path_index + 1, pattern_index + 1)
        )

    return visit(0, 0)


def in_scope(path: str, allowed: list[str], denied: list[str]) -> bool:
    """Return scope membership with deny rules taking unconditional priority."""

    normalized = normal_relative(path)
    if any(glob_match(normalized, pattern) for pattern in denied):
        return False
    return any(glob_match(normalized, pattern) for pattern in allowed)
