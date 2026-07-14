"""Validation of authoritative bootstrap documents."""

from __future__ import annotations

import hashlib
import re
from datetime import date
from pathlib import Path

from .frontmatter import Document, FrontMatterError, parse


SCHEMA_VERSION = "v0.5.0"
DOCUMENT_TYPES = {
    "PROJECT.md": "project_contract",
    "PROJECT-CONTEXT.md": "adopted_contract",
    "ARCHITECTURE-CANON.md": "adopted_contract",
    "CODEBASE-VOICE.md": "adopted_contract",
    "INTEGRATION-POINTS.md": "adopted_contract",
    "BOOTSTRAP-REVIEW.md": "bootstrap_review",
}
AUTHORITATIVE_DOCUMENTS = tuple(name for name in DOCUMENT_TYPES if name != "BOOTSTRAP-REVIEW.md")
PLACEHOLDER = re.compile(r"<[^>]+>")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_document(path: Path) -> Document:
    try:
        return parse(path.read_text(encoding="utf-8"))
    except (OSError, FrontMatterError) as exc:
        raise ValueError(f"{path.name}: {exc}") from exc


def validate_active_document(path: Path, today: date) -> tuple[Document | None, list[str]]:
    findings: list[str] = []
    if not path.is_file():
        return None, [f"Missing required document: {path.name}."]
    try:
        document = read_document(path)
    except ValueError as exc:
        return None, [str(exc)]
    metadata = document.metadata
    expected_type = DOCUMENT_TYPES.get(path.name)
    if expected_type is None or metadata.get("Document-Type") != expected_type:
        findings.append(f"{path.name}: unknown or mismatched Document-Type.")
    for field in ("Contract-Status", "Schema-Version", "Owner-Type", "Owner-ID", "Owner-Display-Name", "Review-Date", "Document-Conflict"):
        if field not in metadata:
            findings.append(f"{path.name}: missing {field}.")
    if metadata.get("Contract-Status") != "ACTIVE":
        findings.append(f"{path.name}: Contract-Status must be ACTIVE.")
    if metadata.get("Schema-Version") != SCHEMA_VERSION:
        findings.append(f"{path.name}: Schema-Version must be {SCHEMA_VERSION}.")
    if metadata.get("Owner-Type") != "human":
        findings.append(f"{path.name}: Owner-Type must be human.")
    if metadata.get("Document-Conflict") != "NONE":
        findings.append(f"{path.name}: Document-Conflict must be NONE.")
    if any(PLACEHOLDER.search(value) for value in metadata.values()) or PLACEHOLDER.search(document.body):
        findings.append(f"{path.name}: unresolved placeholder.")
    try:
        review_date = date.fromisoformat(metadata.get("Review-Date", ""))
        if review_date < today:
            findings.append(f"{path.name}: Review-Date is expired.")
    except ValueError:
        findings.append(f"{path.name}: Review-Date must use YYYY-MM-DD.")
    return document, findings


def comma_values(document: Document, key: str) -> list[str]:
    value = document.metadata.get(key, "")
    return [] if value in {"", "N/A"} else [item.strip() for item in value.split(",") if item.strip()]
