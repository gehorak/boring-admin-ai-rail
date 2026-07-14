# Public Role Model

Contract-Status: REFERENCE
Template-Schema-Version: v0.4.1

## Principle

Responsibility must be explicit. The four roles below are a reduced public
model for host-project adoption; they do not reproduce the full internal role
axis.

## Roles

| Role | Responsibility | May not do |
| --- | --- | --- |
| System Architect | Own final human decisions and authorization boundaries. | Delegate decision ownership to AI or hide it in implementation. |
| Architect-AI | Review boundaries, identify conflicts, and request clarification. | Approve work, redefine scope, or implement it. |
| Senior Developer | Perform explicitly authorized repository work. | Change architecture, expand scope, or select modules implicitly. |
| Reviewer / Auditor | Check compliance and declare `OK`, `READY`, or `BLOCKED`. | Grant approval authority or implement corrective changes. |

AI may assist in the last three roles only when a human has assigned the
bounded task. AI execution remains delegated assistance, not authority.

## Separation rules

- Every final decision has one human System Architect owner.
- A role may advise another role but may not silently assume its authority.
- A reviewer result is independent from authorization.
- A role name is not a tool permission or execution capability.

See `ROLES/` for the compact role cards used by this profile.
