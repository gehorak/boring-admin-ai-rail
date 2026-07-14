# Public Operational Reference Profile

Kit-Version: v0.2.1
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
qualification runtime. JSON Schema files in `contracts/` describe data, and
`validators/validate_operational_profile.py` validates supplied artifacts only;
neither grants authorization or executes work.

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

The included validator checks portable contract invariants. Any future runtime
may consume these data contracts, but it must not redefine their documented
authority or bootstrap rules.
