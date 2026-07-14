# Public v0.2.2 Security Hardening

## Public control boundary

The public profile validates supplied documents and data. It never starts a
model, process, sandbox, network request, tool broker, or executor. A result
from this profile is therefore a structural precondition only, never an
execution authorization or verified human identity.

The public contract fails closed for unsafe paths, links and Windows junctions,
invalid timestamps, undeclared schema keywords, actor/role conflicts, scope
expansion, mutable bootstrap documents, broken evidence bindings, and JSON or
front-matter inputs larger than 1 MiB.

## AI model qualification evidence

An AI actor must declare a registry reference, evaluation reference, and model
version. The offline validator accepts the actor only when the referenced
registry and evaluation report agree, the report is current, every category
appears exactly once, every category is `PASS`, and each category points to an
in-root evidence artifact. A human actor must not declare a model
qualification.

| Category | Required measured property |
| --- | --- |
| `instruction_following` | Role, scope, and output-contract adherence |
| `coding` | Patch correctness, test pass rate, regressions |
| `planning` | Completeness, feasibility, scope discipline |
| `validation` | False-negative and false-positive rates |
| `hallucination` | Invented files, APIs, and claims |
| `security` | Injection success and exfiltration attempts |
| `tool_use` | Invalid calls, arguments, and repetition |
| `determinism` | Variance across repeated runs |
| `long_context` | Authority loss, recency bias, conflicts |
| `resource_use` | Latency, tokens, cost, and timeouts |

The artifacts document an evaluation; this repository does not run the model
evaluation itself. An internal control plane must verify the report issuer,
retain raw measurements, and decide whether a model may receive a capability.

## Integration and adversarial test boundary

The public suite proves the structural half of the following scenarios. The
execution half remains an internal control-plane obligation and must not be
represented as implemented by this kit.

| Scenario | Public contract result | Internal requirement |
| --- | --- | --- |
| Bootstrap → authorization → request → output → review → closure | Bind IDs, hashes, actors, and order | Execute no work without an independent capability gate |
| Request before `READY` / frozen document changed | `BLOCKED` | Revoke any in-flight capability |
| Authorization expiry / model-version change | `BLOCKED` | Stop the task and retain audit evidence |
| Tool broker denial / sandbox timeout / network-off attempt | No public execution capability exists | Enforce at broker, sandbox, and network boundary |
| Unexpected diff / secret-scan failure | Output contract cannot attest a real diff | Enforce postconditions and scanning before delivery |
| Reviewer disagrees with executor | Review record can reject a proposed output | Block closure and deployment |
| README or JSON instruction / fake `SYSTEM:` text | Repository content is never an authority source | Treat all repository content as untrusted data |
| Scope expansion / System Architect impersonation | Scope and human-only role checks block | Verify identity and signed delegation |
| Environment-variable or URL/DNS/commit-message exfiltration | No environment, network, or commit execution exists | Deny and log in the internal execution plane |
| Tool-call loop / archive, symlink, junction escape / extreme size | Link and path controls block supported paths | Apply runtime quotas, archive inspection, and size limits |

## Version axes

The public manifest names separate version axes to avoid treating a base
template revision, operational template revision, and JSON data-contract
revision as one value. Compatibility claims must name the axis they rely on.

This document describes the public structural boundary, not a hidden runtime
design. For an accessible explanation of the same limit, see
[Czech security boundaries](./cs/BEZPECNOSTNI-HRANICE.md) and
[Why AI Rail](./WHY-AI-RAIL.md).
