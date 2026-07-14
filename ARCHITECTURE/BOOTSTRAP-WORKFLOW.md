# Bootstrap Workflow

Contract-Status: REFERENCE
Template-Schema-Version: v0.4.1

## Purpose

Bootstrap turns copied public reference documents into an explicitly owned
host-project contract before non-trivial delivery work begins.

## Entry conditions

Bootstrap may begin when the host repository exists, a human decision owner is
known, and selected modules are known or explicitly deferred. Otherwise the
adoption state remains `UNPACKED`.

## States

1. `UNPACKED` — files are present but host-project truth is not yet written.
2. `SEEDED` — project identity, purpose, decision owner, and selected modules
   are recorded.
3. `MAPPED` — boundaries, codebase conventions, integration points,
   do-not-touch areas, and active change surfaces are explicit.
4. `READY` — a bootstrap review records that the project contract is coherent
   enough for bounded delivery work.

No state may be skipped silently. A review may return `BLOCKED` with explicit
reasons; it does not grant approval.

## Sequence

1. Create the host-project contract from `templates/PROJECT.md`.
2. Record the decision owner, project purpose, and selected modules.
3. Map architecture boundaries, codebase voice, approved integration points,
   do-not-touch areas, and local exceptions.
4. For every active change surface, record exactly one owning selected module.
5. Complete `templates/BOOTSTRAP-REVIEW.md`.

## Ready rule

Before `READY`, AI-assisted work is limited to read-only discovery, repository
mapping, and clarification. Before `READY`, the host project must not claim
that delivery work is authorized, silently select modules, or treat copied
reference content as local project truth.

`READY` requires an explicit review result, not an implied passage of time or
the presence of files.

## Re-bootstrap triggers

Repeat the affected steps when selected modules, ownership, architecture
boundaries, or local exceptions materially change.

The public rationale and a non-normative diagram are in
[How the Rail Works](../DOCS/HOW-THE-RAIL-WORKS.md). The Czech first-pilot text
is [PRVNI-PILOT.md](../DOCS/cs/PRVNI-PILOT.md).
