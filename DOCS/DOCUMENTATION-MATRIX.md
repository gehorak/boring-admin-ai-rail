# Documentation Matrix

This matrix separates normative English references from explanatory Czech
guides. Czech documents improve approachability; they do not override
schemas, templates, validator behavior, or an adopted host-project contract.

| Topic | English authority/reference | Czech counterpart | Parity type | Meaning that must remain aligned |
| --- | --- | --- | --- | --- |
| Public distribution boundary | `DOCS/PUBLIC-DISTRIBUTION.md` | `DOCS/cs/BEZPECNOSTNI-HRANICE.md` | Semantic parity | Public validates supplied data only; runtime capabilities are excluded. |
| Bootstrap states | `ARCHITECTURE/BOOTSTRAP-WORKFLOW.md` | `DOCS/cs/JAK-TO-FUNGUJE.md` | Normative + semantic parity | `UNPACKED`, `SEEDED`, `MAPPED`, `READY`, and `BLOCKED` keep their contract meaning. |
| Role model | `DOCS/ROLE-MODEL.md` | `DOCS/cs/PRO-KOHO-JE-RAIL.md` | Semantic parity | System Architect remains human-only; role is not identity. |
| Module ownership | `ARCHITECTURE/MODULE-COMPOSITION.md` | `DOCS/cs/JAK-TO-FUNGUJE.md` | Functional parity | Each active change surface has one owning selected module. |
| Request/output/evidence flow | `WORKFLOW.md`, schemas | `DOCS/cs/JAK-TO-FUNGUJE.md`, `DOCS/cs/PRVNI-PILOT.md` | Normative + functional parity | IDs, scope, hashes, review, and closure remain bound and ordered. |
| Model qualification evidence | `DOCS/SECURITY-HARDENING.md`, model schemas | `DOCS/cs/BEZPECNOSTNI-HRANICE.md` | Semantic parity | Ten categories are evidence checks, not a model runtime or deployment approval. |
| Security hardening | `DOCS/SECURITY-HARDENING.md` | `DOCS/cs/BEZPECNOSTNI-HRANICE.md` | Semantic parity | Injection, path, identity, execution, and external-effect limits stay explicit. |
| First adoption | `QUICKSTART.md` | `DOCS/cs/PRVNI-PILOT.md` | Functional parity | Both paths use the actual offline CLI and do not claim to run a model. |
| Terminology | Schemas, templates, `DOCS/GLOSSARY.md` | `DOCS/cs/GLOSSARY.md` | Terminology parity | Contract values such as `scope`, `intent`, `READY`, and `BLOCKED` stay unchanged. |
| Troubleshooting | `DOCS/BOOTSTRAP-COMPLETE.md`, CLI behavior | `DOCS/cs/CASTE-CHYBY-A-RESENI.md` | Functional parity | Findings are repaired or escalated; validation is not bypassed. |

## Parity vocabulary

- **Normative parity:** both documents describe the same contract rule; the
  English contract or schema remains authoritative.
- **Semantic parity:** the explanation preserves the same meaning without
  translating every example or paragraph.
- **Functional parity:** a reader can reach the same supported public action,
  command, or validation outcome.
- **Terminology parity:** structured names and states remain in their contract
  form while the surrounding explanation is localized.

When implementation and explanation disagree, inspect the code, schema,
template, and tests, then record and resolve the discrepancy with the project
owner. This matrix is navigation, not an approval record.
