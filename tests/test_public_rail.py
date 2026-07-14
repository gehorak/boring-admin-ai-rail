"""Offline acceptance coverage for the Bootstrap-Complete public CLI."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from public_rail.authorization import scope_hash
from public_rail.bootstrap import freeze, status
from public_rail.cli import init
from public_rail.documents import AUTHORITATIVE_DOCUMENTS, DOCUMENT_TYPES, sha256
from public_rail.evidence import validate_evidence
from public_rail.frontmatter import parse
from public_rail.requests import validate_output, validate_request


class PublicRailTests(unittest.TestCase):
    def root(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return Path(directory.name) / "docs" / "ai-rail"

    def write_json(self, path: Path, value: object) -> None:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def write_document(self, root: Path, name: str, metadata: dict[str, str], body: str = "contract body") -> None:
        lines = ["---", *(f"{key}: {value}" for key, value in metadata.items()), "---", body, ""]
        (root / name).write_text("\n".join(lines), encoding="utf-8")

    def ready_root(self) -> Path:
        root = self.root()
        self.assertEqual(0, init(root, False).execution_capability)
        self.write_json(root / "WORKSPACE.json", {
            "workspace_id": "lantern-notes", "repository_name": "lantern-notes",
            "contract_root": "docs/ai-rail", "allowed_repository_root": ".", "binding_version": "v1",
        })
        for name in AUTHORITATIVE_DOCUMENTS:
            metadata = {
                "Document-Type": DOCUMENT_TYPES[name], "Contract-Status": "ACTIVE", "Schema-Version": "v0.5.0",
                "Owner-Type": "human", "Owner-ID": "github:lantern-owner", "Owner-Display-Name": "Lantern Owner",
                "Review-Date": "2099-10-01", "Document-Conflict": "NONE",
            }
            if name == "PROJECT.md":
                metadata["Selected-Modules"] = "development"
                metadata["Change-Surfaces"] = "application_code"
            self.write_document(root, name, metadata)
        self.assertEqual("MAPPED", status(root).result)
        self.assertEqual("STRUCTURALLY_VALID", freeze(root).result)
        manifest_hash = sha256(root / "BOOTSTRAP-MANIFEST.json")
        review = {
            "Document-Type": "bootstrap_review", "Contract-Status": "ACTIVE", "Schema-Version": "v0.5.0",
            "Owner-Type": "human", "Owner-ID": "github:reviewer", "Owner-Display-Name": "Reviewer",
            "Review-Date": "2099-10-01", "Document-Conflict": "NONE", "Review-Record-ID": "review-001",
            "Workspace-ID": "lantern-notes", "Manifest-Ref": "BOOTSTRAP-MANIFEST.json", "Manifest-SHA256": manifest_hash,
            "Reviewer": "Reviewer", "Decision-Owner": "Lantern Owner", "Result": "READY",
            "Reviewed-At": "2026-07-14T10:00:00Z", "Valid-Until": "2099-10-01",
        }
        self.write_document(root, "BOOTSTRAP-REVIEW.md", review)
        ready_state = status(root)
        self.assertEqual("READY", ready_state.result, ready_state.findings)
        return root

    def valid_request(self, root: Path) -> Path:
        scope = {"repository_root": ".", "allowed_paths": ["**"], "denied_paths": [".git/**", "**/.env", "**/secrets/**"], "allowed_change_kinds": ["documentation"]}
        authorization = {
            "authorization_id": "auth-001", "intent_id": "intent-001", "workspace_id": "lantern-notes",
            "decision_owner_ref": "PROJECT.md#decision-owner", "scope_hash": scope_hash(scope),
            "bootstrap_manifest_sha256": sha256(root / "BOOTSTRAP-MANIFEST.json"), "decision": "AUTHORIZED",
            "authorized_actions": ["propose_changes"], "issued_at": "2026-07-14T10:00:00Z", "expires_at": "2099-07-15T10:00:00Z",
        }
        self.write_json(root / "AUTHORIZATION.json", authorization)
        request = {
            "request_id": "request-001", "intent_id": "intent-001", "workspace_id": "lantern-notes",
            "role": "Senior Developer", "action_mode": "propose_changes", "scope": scope,
            "bootstrap_manifest_sha256": sha256(root / "BOOTSTRAP-MANIFEST.json"), "authorization_ref": "AUTHORIZATION.json",
            "selected_modules": ["development"], "change_surfaces": ["application_code"],
            "authority_sources": [{"path": "PROJECT.md", "kind": "project_contract"}], "execution_capability": False,
        }
        path = root / "request.json"
        self.write_json(path, request)
        return path

    def test_init_is_unpacked_and_refuses_overwrite(self) -> None:
        root = self.root()
        self.assertEqual("UNPACKED", init(root, False).result)
        self.assertEqual("UNPACKED", status(root).result)
        self.assertEqual("BLOCKED", init(root, False).result)

    def test_ready_is_derived_and_document_change_blocks_it(self) -> None:
        root = self.ready_root()
        (root / "PROJECT.md").write_text((root / "PROJECT.md").read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
        self.assertEqual("BLOCKED", status(root).result)

    def test_expired_review_blocks_ready(self) -> None:
        root = self.ready_root()
        text = (root / "BOOTSTRAP-REVIEW.md").read_text(encoding="utf-8").replace("Valid-Until: 2099-10-01", "Valid-Until: 2020-01-01")
        (root / "BOOTSTRAP-REVIEW.md").write_text(text, encoding="utf-8")
        self.assertEqual("BLOCKED", status(root).result)

    def test_front_matter_rejects_duplicate_and_body_metadata(self) -> None:
        root = self.ready_root()
        text = (root / "PROJECT.md").read_text(encoding="utf-8").replace("Owner-ID: github:lantern-owner", "Owner-ID: github:lantern-owner\nOwner-ID: duplicate")
        (root / "PROJECT.md").write_text(text, encoding="utf-8")
        self.assertEqual("BLOCKED", status(root).result)

        root = self.ready_root()
        (root / "PROJECT.md").write_text((root / "PROJECT.md").read_text(encoding="utf-8") + "Owner-ID: body\n", encoding="utf-8")
        self.assertEqual("BLOCKED", status(root).result)

    def test_operational_templates_allow_body_labels(self) -> None:
        template_root = Path(__file__).resolve().parent.parent / "templates" / "operational"
        for path in template_root.glob("*.md"):
            with self.subTest(path=path.name):
                document = parse(path.read_text(encoding="utf-8"))
                self.assertEqual("DRAFT", document.metadata["Contract-Status"])

    def test_request_and_output_scope_checks(self) -> None:
        root = self.ready_root()
        request_path = self.valid_request(root)
        self.assertEqual("AUTHORIZATION_RECORD_CONSISTENT", validate_request(root, request_path).result)
        output_path = root / "output.json"
        self.write_json(output_path, {"request_id": "request-001", "intent_id": "intent-001", "workspace_id": "lantern-notes", "role": "Senior Developer", "action_mode": "propose_changes", "execution_capability": False, "artifacts": [{"path": "PROJECT.md", "change_kind": "documentation"}]})
        self.assertEqual("STRUCTURALLY_VALID", validate_output(root, request_path, output_path).result)
        output = json.loads(output_path.read_text(encoding="utf-8"))
        output["artifacts"] = [{"path": ".git/config", "change_kind": "documentation"}]
        self.write_json(output_path, output)
        self.assertEqual("BLOCKED", validate_output(root, request_path, output_path).result)
        output["artifacts"] = [{"path": "../escape.md", "change_kind": "documentation"}]
        self.write_json(output_path, output)
        self.assertEqual("BLOCKED", validate_output(root, request_path, output_path).result)

    def test_symlink_and_authorization_expiry_block_validation(self) -> None:
        root = self.ready_root()
        link = root / "linked-project.md"
        try:
            link.symlink_to(root / "PROJECT.md")
        except OSError as exc:
            self.skipTest(f"Symlink creation is unavailable: {exc}")
        self.assertEqual("BLOCKED", status(root).result)
        link.unlink()
        request_path = self.valid_request(root)
        authorization = json.loads((root / "AUTHORIZATION.json").read_text(encoding="utf-8"))
        authorization["expires_at"] = "2020-01-01T00:00:00Z"
        self.write_json(root / "AUTHORIZATION.json", authorization)
        self.assertEqual("BLOCKED", validate_request(root, request_path).result)

    def test_authorization_and_authority_binding_failures(self) -> None:
        root = self.ready_root()
        request_path = self.valid_request(root)
        request = json.loads(request_path.read_text(encoding="utf-8"))
        request["authority_sources"] = [{"path": "README.md", "kind": "project_contract"}]
        self.write_json(request_path, request)
        self.assertEqual("BLOCKED", validate_request(root, request_path).result)

    def test_cli_enforces_strict_json_contracts(self) -> None:
        root = self.ready_root()
        request_path = self.valid_request(root)
        request = json.loads(request_path.read_text(encoding="utf-8"))
        request["unexpected"] = True
        self.write_json(request_path, request)
        result = validate_request(root, request_path)
        self.assertEqual("BLOCKED", result.result)
        self.assertIn("request: unexpected property 'unexpected'.", result.findings)

        request.pop("unexpected")
        request["selected_modules"] = ["unknown-module"]
        self.write_json(request_path, request)
        self.assertEqual("BLOCKED", validate_request(root, request_path).result)

        request["selected_modules"] = ["development"]
        request["extensions"] = {"future": "allowed"}
        self.write_json(request_path, request)
        self.assertEqual("AUTHORIZATION_RECORD_CONSISTENT", validate_request(root, request_path).result)

        authorization_path = root / "AUTHORIZATION.json"
        authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
        authorization["unexpected"] = True
        self.write_json(authorization_path, authorization)
        result = validate_request(root, request_path)
        self.assertEqual("BLOCKED", result.result)
        self.assertIn("AUTHORIZATION.json: unexpected property 'unexpected'.", result.findings)
        authorization.pop("unexpected")
        self.write_json(authorization_path, authorization)

        output_path = root / "output.json"
        self.write_json(output_path, {"request_id": "request-001", "intent_id": "intent-001", "workspace_id": "lantern-notes", "role": "Senior Developer", "action_mode": "propose_changes", "execution_capability": False, "artifacts": [], "unexpected": True})
        result = validate_output(root, request_path, output_path)
        self.assertEqual("BLOCKED", result.result)
        self.assertIn("output: unexpected property 'unexpected'.", result.findings)

        evidence_path = root / "evidence.json"
        self.write_json(evidence_path, {"manifest_id": "evidence-001", "intent_id": "intent-001", "workspace_id": "lantern-notes", "records": [], "unexpected": True})
        result = validate_evidence(root, evidence_path)
        self.assertEqual("BLOCKED", result.result)
        self.assertIn("evidence: unexpected property 'unexpected'.", result.findings)

        manifest_path = root / "BOOTSTRAP-MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["unexpected"] = True
        self.write_json(manifest_path, manifest)
        result = status(root)
        self.assertEqual("BLOCKED", result.result)
        self.assertIn("BOOTSTRAP-MANIFEST.json: unexpected property 'unexpected'.", result.findings)
        manifest.pop("unexpected")
        self.write_json(manifest_path, manifest)

        workspace_path = root / "WORKSPACE.json"
        workspace = json.loads(workspace_path.read_text(encoding="utf-8"))
        workspace["unexpected"] = True
        self.write_json(workspace_path, workspace)
        result = status(root)
        self.assertEqual("UNPACKED", result.result)
        self.assertIn("WORKSPACE.json: unexpected property 'unexpected'.", result.findings)
        request["authority_sources"] = [{"path": "PROJECT.md", "kind": "project_contract"}]
        request["intent_id"] = "other-intent"
        self.write_json(request_path, request)
        self.assertEqual("BLOCKED", validate_request(root, request_path).result)

    def test_evidence_chain_accepts_and_rejects_broken_links(self) -> None:
        root = self.ready_root()
        records = []
        previous = None
        for index, record_type in enumerate(("intent", "authorization", "proposed_output", "review_result", "closure")):
            artifact = root / f"{record_type}.md"
            artifact.write_text(record_type, encoding="utf-8")
            record_id = f"record-{index}"
            records.append({"record_id": record_id, "record_type": record_type, "intent_id": "intent-001", "workspace_id": "lantern-notes", "previous_record_id": previous, "artifact_path": artifact.name, "artifact_sha256": sha256(artifact)})
            previous = record_id
        evidence_path = root / "evidence.json"
        self.write_json(evidence_path, {"manifest_id": "evidence-001", "intent_id": "intent-001", "workspace_id": "lantern-notes", "records": records})
        self.assertEqual("EVIDENCE_CHAIN_VALID", validate_evidence(root, evidence_path).result)
        records[2]["previous_record_id"] = "wrong"
        self.write_json(evidence_path, {"manifest_id": "evidence-001", "intent_id": "intent-001", "workspace_id": "lantern-notes", "records": records})
        self.assertEqual("BLOCKED", validate_evidence(root, evidence_path).result)

    def test_public_schemas_are_strict_with_extensions_only(self) -> None:
        schema_root = Path(__file__).resolve().parent.parent / "schemas"
        for path in schema_root.glob("*.schema.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            self.assertFalse(schema["additionalProperties"], path.name)
            self.assertIn("extensions", schema["properties"], path.name)


if __name__ == "__main__":
    unittest.main()
