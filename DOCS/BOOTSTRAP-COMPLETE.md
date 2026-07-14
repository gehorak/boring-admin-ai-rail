# Bootstrap-Complete Public Profile

## Boundary

Public Rail proves local structural consistency: project documents, human
ownership declarations, scope, bootstrap review, hashes, authorization-record
binding, and evidence-chain order. It never calls a model, enables a tool,
executes a change, verifies real identity, or issues a capability.

## Offline workflow

```text
python -m public_rail init --target docs/ai-rail
python -m public_rail validate --root docs/ai-rail
python -m public_rail freeze --root docs/ai-rail
python -m public_rail status --root docs/ai-rail
python -m public_rail validate-request request.json --root docs/ai-rail
python -m public_rail validate-output request.json output.json --root docs/ai-rail
python -m public_rail validate-evidence evidence.json --root .
```

`init` copies neutral operational templates only and refuses overwrites unless
`--force` is explicit. `freeze` hashes authoritative active documents. `READY`
is derived from the active documents, frozen manifest, and current bootstrap
review; it is invalidated when a frozen document changes.

## Results

The CLI returns only `UNPACKED`, `SEEDED`, `MAPPED`, `READY`, `BLOCKED`,
`STRUCTURALLY_VALID`, `AUTHORIZATION_RECORD_CONSISTENT`, or
`EVIDENCE_CHAIN_VALID`. Its JSON envelope always reports that execution,
identity verification, and execution capability are false.

## Authority and scope

Authority documents must be inside the contract root, use active strict front
matter, have a human owner, current review date, no conflict, and a matching
bootstrap-manifest hash. Authorization records are checked for local
consistency only; they are not proof of a human identity or organizational
authority. Structured scopes reject traversal, absolute paths, denied paths,
and out-of-scope output artifacts.
