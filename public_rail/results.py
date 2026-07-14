"""Stable public result envelopes."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Result:
    result: str
    findings: list[str] = field(default_factory=list)
    validated_artifacts: list[str] = field(default_factory=list)
    execution_authorized: bool = False
    execution_capability: bool = False
    identity_verified: bool = False

    def payload(self) -> dict[str, object]:
        return asdict(self)
