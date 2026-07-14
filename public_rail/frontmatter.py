"""Deterministic front matter parser for the limited public contract format."""

from __future__ import annotations

import re
from dataclasses import dataclass


class FrontMatterError(ValueError):
    """Raised when strict document front matter is malformed."""


LINE = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):[ ](.+)$")
METADATA_NAME = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):")
CONTRACT_METADATA_KEYS = {
    "Document-Type", "Contract-Status", "Schema-Version", "Owner-Type",
    "Owner-ID", "Owner-Display-Name", "Review-Date", "Document-Conflict",
    "Selected-Modules", "Change-Surfaces", "Review-Record-ID", "Workspace-ID",
    "Manifest-Ref", "Manifest-SHA256", "Reviewer", "Decision-Owner", "Result",
    "Reviewed-At", "Valid-Until",
}


@dataclass(frozen=True)
class Document:
    metadata: dict[str, str]
    body: str


def parse(text: str) -> Document:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise FrontMatterError("Document must start with front matter delimiter.")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise FrontMatterError("Front matter closing delimiter is missing.") from exc
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        match = LINE.fullmatch(line)
        if not match:
            raise FrontMatterError(f"Front matter line is invalid: {line!r}.")
        key, value = match.groups()
        if key in metadata:
            raise FrontMatterError(f"Duplicate front matter key: {key}.")
        if not value.strip():
            raise FrontMatterError(f"Front matter value is empty: {key}.")
        metadata[key] = value.strip()
    body_lines = lines[end + 1 :]
    if any(
        match and match.group(1) in CONTRACT_METADATA_KEYS
        for line in body_lines
        if (match := METADATA_NAME.match(line))
    ):
        raise FrontMatterError("Metadata is not allowed after front matter.")
    return Document(metadata=metadata, body="\n".join(body_lines))
