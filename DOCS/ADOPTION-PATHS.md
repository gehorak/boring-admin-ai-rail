# Adoption Paths

## How to use this guide

Choose the smallest path that matches the work you need to make explicit.
Every path remains documentation-first until the adopter supplies and audits
its own control plane. The public kit does not become an executor at any
level.

## Role-based paths

| Audience | Start with | Decide | Do not expect |
| --- | --- | --- | --- |
| Solo repository owner | [Why AI Rail?](./WHY-AI-RAIL.md), `PROJECT.md`, [security boundary](./SECURITY-HARDENING.md) | Owner, scope, do-not-touch paths, review cadence | Automatic safety or identity verification |
| Developer | [Quickstart](../QUICKSTART.md), [workflow](../WORKFLOW.md) | Proposed change, allowed surfaces, output artifacts | The CLI to apply or commit a patch |
| Architect | [How the rail works](./HOW-THE-RAIL-WORKS.md), [role model](./ROLE-MODEL.md) | Architecture authority, conflicts, module ownership | AI to own final decisions |
| DevOps/platform engineer | [module composition](../ARCHITECTURE/MODULE-COMPOSITION.md), integration templates | Infrastructure and boundary ownership | A sandbox, network policy, or secrets broker |
| Reviewer/auditor | [bootstrap reference](./BOOTSTRAP-COMPLETE.md), evidence schemas | Whether evidence and scope support a verdict | A hash to prove external correctness |
| AI-assisted team | [operational profile](./OPERATIONAL-REFERENCE-PROFILE.md), [documentation matrix](./DOCUMENTATION-MATRIX.md) | Adoption boundary and human review | Autonomous orchestration |

## Maturity levels

### 1. Documentation-only

Adopt `PROJECT.md` and the relevant specialized contracts. Name an owner,
write the boundaries, and use `DRAFT`/`ACTIVE` status deliberately. This is
useful even when no AI is involved.

### 2. Bootstrap validation

Use `python -m public_rail` to initialize, validate, freeze, and inspect the
`READY` or `BLOCKED` state. The public validator checks supplied files and
does not authorize a tool.

### 3. Request, output, and evidence validation

Bind a request and output to the frozen project mapping. Record the evidence
chain and closure for work that needs reconstruction. Keep the actual patch,
tests, and external effects under the adopter's own controls.

### 4. Model qualification evidence

If an AI actor is declared, provide a local registry and evaluation report
covering all ten public categories. The public profile checks completeness,
identity/version consistency, dates, and in-root evidence references. It does
not run the evaluation or approve deployment.

### 5. External execution plane

An adopter may add identity verification, a policy engine, tool broker,
sandbox, network and secret controls, postcondition checks, and telemetry.
Those components are outside this repository's public profile and must not be
described as included by `READY`.

## A safe next step

For a first adoption, use the [English quickstart](../QUICKSTART.md) or the
[Czech first pilot](./cs/PRVNI-PILOT.md), choose one documentation-only task,
and ask a human reviewer to inspect the result before treating the intent as
closed.
