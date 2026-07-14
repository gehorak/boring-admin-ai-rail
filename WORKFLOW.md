# Operational Workflow

Contract-Status: REFERENCE
Template-Schema-Version: v0.4.1

## Purpose

This workflow keeps one AI-assisted change bounded and reconstructable. It is
a documentation contract, not an execution engine.

## Sequence

1. Record one explicit intent and scope boundary.
2. Have Architect-AI identify contract conflicts, role confusion, and scope
   expansion risks when architectural review is needed.
3. Have the human System Architect authorize, reject, or narrow the work.
4. Perform only the authorized preparation or delivery work.
5. Have Reviewer / Auditor record `OK` or `BLOCKED` with factual reasons.
6. Record the resulting evidence and closure in the host project.

One intent represents one bounded change step. A review result is not approval
authority, and an AI role never owns final human decisions.

## Bootstrap rule

For host-project delivery, the bootstrap state must be `READY`. Before then,
only bootstrap preparation, read-only discovery, mapping, and clarification
are in scope.

## Evidence minimum

Each completed step should preserve an intent identifier, scope boundary,
authorization reference, review result, and closure record. The optional
`schemas/evidence.schema.json` defines a portable data shape for that rail.

## Exclusion

This document does not authorize tools, external services, code execution, or
automation. Those capabilities require separate implementation and controls.
