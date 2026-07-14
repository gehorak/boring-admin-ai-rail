# Module Composition

Contract-Status: REFERENCE
Template-Schema-Version: v0.4.1

## Purpose

Modules provide a portable vocabulary for change-surface ownership. They are
selected only when a host project uses their surfaces; this kit does not force
adoption of all five.

## Reduced module map

| Module | Owns change surfaces |
| --- | --- |
| `development` | application code, codebase structure |
| `devops` | pipeline and release flow, deployment automation, recoverability |
| `infrastructure` | environment foundation, topology and capacity, resilience |
| `security` | identity and authorization, credentials, privileged exposure |
| `data` | schema and persistence, data integrity, retention and recovery |

## Composition rule

For every active change surface, the host project records one owning selected
module. Multiple modules may participate in one change, but they do not share
ownership of the same surface. Unknown, unowned, or reassigned surfaces are a
reason to clarify, split, or block the work.

The host project may narrow how a surface appears locally. It must not use a
local document to silently reassign ownership.

## Boundary

This is a reference map. It does not contain a runtime resolver, a request
gate, or an automated enforcement mechanism.
