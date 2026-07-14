"""Minimal offline validator for the public JSON Schema contract subset."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any


SCHEMA_NAMES = {
    "authorization",
    "bootstrap-manifest",
    "evidence",
    "output",
    "request",
    "workspace-binding",
}


@lru_cache
def load_schema(name: str) -> dict[str, Any]:
    if name not in SCHEMA_NAMES:
        raise ValueError(f"Unknown public schema: {name}.")
    path = Path(__file__).resolve().parent.parent / "schemas" / f"{name}.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def matches_type(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "null":
        return value is None
    return False


def validate(name: str, value: object) -> list[str]:
    """Return deterministic findings for the supported public schema subset."""

    findings: list[str] = []

    def visit(instance: object, schema: dict[str, Any], location: str) -> None:
        expected_type = schema.get("type")
        if isinstance(expected_type, str):
            expected_types = (expected_type,)
        elif isinstance(expected_type, list) and all(isinstance(item, str) for item in expected_type):
            expected_types = tuple(expected_type)
        else:
            expected_types = ()
        if expected_types and not any(matches_type(instance, item) for item in expected_types):
            findings.append(f"{location}: must be {', '.join(expected_types)}.")
            return
        if "const" in schema and instance != schema["const"]:
            findings.append(f"{location}: must equal {schema['const']!r}.")
        if "enum" in schema and instance not in schema["enum"]:
            findings.append(f"{location}: must be one of the declared values.")
        if isinstance(instance, str):
            if len(instance) < schema.get("minLength", 0):
                findings.append(f"{location}: must not be empty.")
            pattern = schema.get("pattern")
            if isinstance(pattern, str) and not re.fullmatch(pattern, instance):
                findings.append(f"{location}: does not match the required pattern.")
        if isinstance(instance, list):
            if len(instance) < schema.get("minItems", 0):
                findings.append(f"{location}: must contain at least {schema['minItems']} item(s).")
            item_schema = schema.get("items")
            if isinstance(item_schema, dict):
                for index, item in enumerate(instance):
                    visit(item, item_schema, f"{location}[{index}]")
        if isinstance(instance, dict):
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            for key in required:
                if key not in instance:
                    findings.append(f"{location}: missing required property {key!r}.")
            if schema.get("additionalProperties") is False:
                for key in instance:
                    if key not in properties:
                        findings.append(f"{location}: unexpected property {key!r}.")
            for key, child_schema in properties.items():
                if key in instance and isinstance(child_schema, dict):
                    visit(instance[key], child_schema, f"{location}.{key}")

    visit(value, load_schema(name), name)
    return findings
