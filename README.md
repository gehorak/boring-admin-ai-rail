# BORING-ADMIN-AI-RAIL

## Bootstrap-Complete Public Profile

BORING-ADMIN-AI-RAIL is a contract-first reference for bounded AI-assisted
technical work. It helps a host repository record who decides, what is in
scope, which local rules apply, and which evidence supports a proposed result.

This public v0.2.2 kit is for:

- a person meeting the framework for the first time;
- a developer or operator preparing a first pilot;
- a reviewer checking authority, scope, ownership, and evidence;
- a documentation author separating portable contracts from private
  project knowledge.

It contains neutral templates, a five-module operational reference, strict
data contracts, a fictional example, and an offline CLI. It does not call a
model, authorize tools, execute changes, verify human identity, or provide a
provider adapter, sandbox, executor, telemetry, or model qualification runtime.

Kit-Version: v0.2.2
Template-Schema-Version: v0.5.0

## Recommended reading

1. [QUICKSTART.md](./QUICKSTART.md) — English adoption path.
2. [Czech public documentation](./DOCS/cs/README.md) — onboarding, FAQ,
   glossary, use cases, and traceability.
3. [DOCS/BOOTSTRAP-COMPLETE.md](./DOCS/BOOTSTRAP-COMPLETE.md) — the v0.2.2
   boundary and offline commands.
4. [DOCS/OPERATIONAL-REFERENCE-PROFILE.md](./DOCS/OPERATIONAL-REFERENCE-PROFILE.md)
   — roles, modules, workflow, and contract boundaries.

## Offline CLI

```text
python -m public_rail init --target docs/ai-rail
python -m public_rail validate --root docs/ai-rail
python -m public_rail freeze --root docs/ai-rail
python -m public_rail status --root docs/ai-rail
python -m public_rail validate-request request.json --root docs/ai-rail
python -m public_rail validate-output request.json output.json --root docs/ai-rail
python -m public_rail validate-evidence evidence.json --root .
```

The CLI checks supplied documentation and data only. Its result envelope never
claims execution authorization, identity verification, or execution capability.

The full license is in [LICENSE](./LICENSE). User-visible changes are listed
in [CHANGELOG.md](./CHANGELOG.md), and package maintenance is described in
[MAINTENANCE.md](./MAINTENANCE.md).
