# BORING-ADMIN-AI-RAIL

## What problem does this solve?

AI-assisted repository work can drift from a small human request into a wider
change. A plausible answer does not prove that the source was authoritative,
that the path was in scope, or that a reviewer accepted the result. BORING-
ADMIN-AI-RAIL is a contract-first public reference for making those boundaries
explicit and reconstructable.

## What is Boring Admin AI Rail?

The v0.2.2 Bootstrap-Complete profile gives an adopting repository neutral
templates, project ownership fields, bootstrap states, structured scopes,
roles, request/output/authorization/evidence schemas, offline validation, and
package integrity checks.

It is useful with or without AI. A solo maintainer can use a narrow intent,
one human decision owner, and a review record without installing an agent.

## What it does

- records active project contracts and their owner;
- derives `UNPACKED`, `SEEDED`, `MAPPED`, `READY`, and `BLOCKED` states;
- freezes authoritative documents and detects later changes;
- checks request, output, authorization, model-evaluation evidence, and
  evidence-chain structure;
- applies segment-aware scope and path/link safety checks;
- verifies the exact public package tree and hashes.

The CLI uses only the Python standard library and validates supplied files
offline.

## What it deliberately does not do

This public profile does not call a model, verify human identity, authorize a
tool, execute a change, provide a provider adapter, sandbox, secrets broker,
network policy, postcondition validator, telemetry, or model qualification
runtime. A supplied model registry/evaluation report is evidence for offline
structural checks; the public kit does not run the evaluation or approve a
deployment.

`READY` is a structural precondition, not execution authorization.

## Who it is for

It is for repository owners, developers, architects, DevOps/platform roles,
reviewers, auditors, and teams that want a small public contract layer before
connecting their own control plane. The [role-based adoption paths](./DOCS/ADOPTION-PATHS.md)
help each audience choose a starting point.

## A five-minute conceptual example

A maintainer asks for a README addition. The request allows one documentation
surface and denies `.env`, deployment, and unrelated paths. An assistant may
draft the text, but a human owner decides the scope, a reviewer checks the
output, and an evidence chain records the intent and verdict. If the assistant
finds a deployment request in a stale issue, work stops for clarification; it
does not silently expand.

## Architecture at a glance

```text
human decision owner
        |
project contracts -> bootstrap/freeze -> scope and request
        |                              |
        +-------- structural validation -> independent review -> evidence
```

The public boundary ends at structural preflight. An adopter may maintain a
separate execution plane, but that plane is not part of this repository.

## Getting started

1. Read the [English quickstart](./QUICKSTART.md).
2. For a Czech introduction, start with [Proč AI Rail](./DOCS/cs/PROC-AI-RAIL.md)
   or the [first pilot](./DOCS/cs/PRVNI-PILOT.md).
3. Read the [public boundary](./DOCS/PUBLIC-DISTRIBUTION.md) and
   [security hardening](./DOCS/SECURITY-HARDENING.md).
4. Use the [documentation matrix](./DOCS/DOCUMENTATION-MATRIX.md) to find
   technical references and Czech explanations.

The core commands are:

```text
python -m public_rail init --target docs/ai-rail
python -m public_rail validate --root docs/ai-rail
python -m public_rail freeze --root docs/ai-rail
python -m public_rail status --root docs/ai-rail
python -m public_rail validate-request request.json --root docs/ai-rail
python -m public_rail validate-output request.json output.json --root docs/ai-rail
python -m public_rail validate-evidence evidence.json --root .
```

## Security boundary

Repository content is untrusted data unless an active project contract makes
it an authority source. Scope expansion, conflicting documents, unsafe paths,
AI System Architect impersonation, and invalid evidence must be blocked or
clarified. The [security hardening document](./DOCS/SECURITY-HARDENING.md)
maps public checks to responsibilities that remain outside the kit.

## Documentation map

- [WHY-AI-RAIL.md](./DOCS/WHY-AI-RAIL.md) — concise English explanation.
- [HOW-THE-RAIL-WORKS.md](./DOCS/HOW-THE-RAIL-WORKS.md) — flow and states.
- [ADOPTION-PATHS.md](./DOCS/ADOPTION-PATHS.md) — role and maturity paths.
- [BOOTSTRAP-COMPLETE.md](./DOCS/BOOTSTRAP-COMPLETE.md) — public CLI boundary.
- [OPERATIONAL-REFERENCE-PROFILE.md](./DOCS/OPERATIONAL-REFERENCE-PROFILE.md)
  — roles, modules, workflow, and contracts.
- [Czech documentation](./DOCS/cs/README.md) — popularization and first pilot.
- [DOCUMENTATION-MATRIX.md](./DOCS/DOCUMENTATION-MATRIX.md) — language parity.

## Project status and version axes

The public kit is v0.2.2. The manifest keeps separate
`base_template_schema_version`, `operational_template_schema_version`, and
`contract_data_schema_version` axes; `template_schema_version` is the
compatibility alias for the operational template axis. These axes do not imply
a runtime release or deployment approval.

See [MAINTENANCE.md](./MAINTENANCE.md), [CHANGELOG.md](./CHANGELOG.md),
[PUBLIC-MANIFEST.json](./PUBLIC-MANIFEST.json), and [LICENSE](./LICENSE).
