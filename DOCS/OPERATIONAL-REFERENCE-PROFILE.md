# Public Operational Reference Profile

Kit-Version: v0.2.2
Profile: optional operational reference

## Purpose

This profile extends the compact Adoption Reference Kit with a portable
documentation-first model for bootstrap, bounded work, roles, module
ownership, and reconstructable evidence. It helps a host repository describe
how AI-assisted work should be prepared and reviewed.

It is optional. The small Adoption Kit remains a valid entry layer when a team
only needs project-local contracts.

## Included

- bootstrap states and review criteria;
- a simplified workflow and four public roles;
- a five-module change-surface ownership map;
- a bootstrap review template and minimum host-repository assembly guide;
- request, output, and evidence data contracts.

## Excluded

This profile includes no request gate, output gate, tool gate, sandbox,
executor, provider adapter, telemetry, operational logging, or model
qualification runtime. JSON Schema files in `schemas/` describe data, and
`python -m public_rail` validates supplied artifacts only; it neither grants
authorization nor executes work. It can check the consistency of a supplied
model registry and evaluation report, but does not run those evaluations.

## Authority

The human System Architect remains the decision owner. AI may assist only in
the bounded Architect-AI, Senior Developer, or Reviewer / Auditor roles. A
role name does not grant approval authority or permission to execute tools.

## Adoption boundary

Copy only the documents and templates a host project adopts. Before delivery
work, the host project must record its local owner, selected modules, active
change surfaces, boundaries, and a `READY` bootstrap review result. The host
project remains responsible for any implementation, security controls, and
execution environment.

## Relationship to later work

The included CLI checks portable contract invariants and derives only
`UNPACKED`, `SEEDED`, `MAPPED`, `READY`, or `BLOCKED`. Any future runtime may
consume these data contracts, but it must not redefine their documented
authority or bootstrap rules.

For adoption choices, see [Adoption Paths](./ADOPTION-PATHS.md). The public
boundary and non-runtime claims are summarized in
[Security Hardening](./SECURITY-HARDENING.md).
