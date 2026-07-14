"""Negative and positive coverage for the public operational-profile validator."""

from __future__ import annotations

import copy
import tempfile
import unittest
from datetime import date
from pathlib import Path

from validators.validate_operational_profile import (
    ValidationError,
    validate_document,
    validate_output,
    validate_request,
)


TODAY = date(2026, 7, 14)
VALID_REQUEST = {
    "request_id": "request-001",
    "intent_id": "intent-001",
    "actor_type": "ai",
    "role": "Senior Developer",
    "scope": {
        "target": "host-project",
        "kind": "delivery",
        "boundary": "docs/ai-rail only",
    },
    "bootstrap_state": "READY",
    "selected_modules": ["development"],
    "change_surfaces": ["application_code"],
    "decision_owner_ref": "docs/ai-rail/PROJECT.md#owner",
    "authorization_ref": "records/intent-001.md",
    "authority_sources": [
        {"path": "docs/ai-rail/PROJECT.md", "kind": "adopted_contract"}
    ],
    "execution_capability": False,
}
VALID_OUTPUT = {
    "request_id": "request-001",
    "intent_id": "intent-001",
    "role": "Senior Developer",
    "scope_boundary": "docs/ai-rail only",
    "action_mode": "propose_changes",
    "summary": "Proposed bounded documentation change.",
    "authority_refs_used": ["docs/ai-rail/PROJECT.md"],
    "execution_capability": False,
}


class OperationalProfileValidationTests(unittest.TestCase):
    def assert_invalid(self, callback) -> None:
        with self.assertRaises(ValidationError):
            callback()

    def write_document(self, metadata: str) -> Path:
        temporary = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False)
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        temporary.write("# Contract\n\n" + metadata + "\n")
        temporary.close()
        return Path(temporary.name)

    def valid_document(self) -> Path:
        return self.write_document(
            "Contract-Status: ACTIVE\n"
            "Owner: human decision owner\n"
            "Review-Date: 2026-10-01\n"
            "Document-Conflict: NONE"
        )

    def test_accepts_valid_document_request_and_output(self) -> None:
        validate_document(self.valid_document(), TODAY)
        validate_request(copy.deepcopy(VALID_REQUEST))
        validate_output(copy.deepcopy(VALID_REQUEST), copy.deepcopy(VALID_OUTPUT))

    def test_rejects_missing_owner(self) -> None:
        document = self.write_document(
            "Contract-Status: ACTIVE\nReview-Date: 2026-10-01\nDocument-Conflict: NONE"
        )
        self.assert_invalid(lambda: validate_document(document, TODAY))

    def test_rejects_expired_review(self) -> None:
        document = self.write_document(
            "Contract-Status: ACTIVE\nOwner: human decision owner\n"
            "Review-Date: 2026-01-01\nDocument-Conflict: NONE"
        )
        self.assert_invalid(lambda: validate_document(document, TODAY))

    def test_rejects_unresolved_document_conflict(self) -> None:
        document = self.write_document(
            "Contract-Status: ACTIVE\nOwner: human decision owner\n"
            "Review-Date: 2026-10-01\nDocument-Conflict: UNRESOLVED"
        )
        self.assert_invalid(lambda: validate_document(document, TODAY))

    def test_rejects_delivery_before_ready(self) -> None:
        request = copy.deepcopy(VALID_REQUEST)
        request["bootstrap_state"] = "MAPPED"
        self.assert_invalid(lambda: validate_request(request))

    def test_rejects_change_surface_without_selected_owner_module(self) -> None:
        request = copy.deepcopy(VALID_REQUEST)
        request["selected_modules"] = ["security"]
        self.assert_invalid(lambda: validate_request(request))

    def test_rejects_role_confusion(self) -> None:
        request = copy.deepcopy(VALID_REQUEST)
        request["role"] = "System Architect"
        self.assert_invalid(lambda: validate_request(request))

    def test_rejects_scope_expansion(self) -> None:
        output = copy.deepcopy(VALID_OUTPUT)
        output["scope_boundary"] = "entire repository"
        self.assert_invalid(lambda: validate_output(copy.deepcopy(VALID_REQUEST), output))

    def test_rejects_repository_content_as_instruction(self) -> None:
        request = copy.deepcopy(VALID_REQUEST)
        request["authority_sources"] = [
            {"path": "README.md", "kind": "repository_content"}
        ]
        self.assert_invalid(lambda: validate_request(request))

    def test_rejects_unauthorized_execution_capability(self) -> None:
        request = copy.deepcopy(VALID_REQUEST)
        request["execution_capability"] = True
        self.assert_invalid(lambda: validate_request(request))
        output = copy.deepcopy(VALID_OUTPUT)
        output["execution_capability"] = True
        self.assert_invalid(lambda: validate_output(copy.deepcopy(VALID_REQUEST), output))


if __name__ == "__main__":
    unittest.main()
