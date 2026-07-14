"""Portable path handling that never follows links outside the contract root."""

from __future__ import annotations

import fnmatch
from pathlib import Path, PurePosixPath


class PathError(ValueError):
    """Raised for an unsafe or out-of-scope path."""


def is_link_or_junction(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or (callable(is_junction) and is_junction())


def reject_links(root: Path) -> list[str]:
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if is_link_or_junction(path)
    )


def normal_relative(value: object) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise PathError("Path must be a non-empty relative POSIX path.")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value == ".":
        raise PathError("Path must stay below its declared root.")
    return path.as_posix()


def resolve_below(root: Path, value: object) -> Path:
    relative = normal_relative(value)
    candidate = root / PurePosixPath(relative)
    if is_link_or_junction(candidate):
        raise PathError(f"Path is a symbolic link or junction: {relative}")
    return candidate


def in_scope(path: str, allowed: list[str], denied: list[str]) -> bool:
    normalized = normal_relative(path)
    if any(fnmatch.fnmatchcase(normalized, pattern) for pattern in denied):
        return False
    return any(fnmatch.fnmatchcase(normalized, pattern) for pattern in allowed)
