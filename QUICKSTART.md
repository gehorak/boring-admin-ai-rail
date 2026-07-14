# Quickstart: a small offline pilot

This tutorial prepares one bounded documentation proposal in an existing
repository. It does not call a model, execute a tool, apply a patch, or grant
execution permission.

## 1. Choose a small task

Use a sentence such as: “Add a short explanation of the existing local test
command to `README.md`.” Choose one human `decision owner`. Put application
code, CI workflow, deployment, credentials, `.env`, and unrelated paths out of
scope.

## 2. Initialize the contract root

From the adopting repository, run:

```text
python -m public_rail init --target docs/ai-rail
```

The command copies the six operational templates and creates `WORKSPACE.json`,
a placeholder bootstrap manifest, and `evidence/`. The initial state is
`UNPACKED`. It refuses to overwrite a non-empty target unless `--force` is
explicit.

## 3. Write project truth

Replace placeholders in `WORKSPACE.json` with the repository and workspace
identity. Complete `PROJECT.md`, `PROJECT-CONTEXT.md`, and
`ARCHITECTURE-CANON.md`; add `CODEBASE-VOICE.md` and
`INTEGRATION-POINTS.md` when the task needs them.

Every active document needs a human owner, `Contract-Status: ACTIVE`, a future
`Review-Date`, and `Document-Conflict: NONE`. `PROJECT.md` must state the
selected modules and change surfaces used by the host project.

Check the first findings:

```text
python -m public_rail validate --root docs/ai-rail
python -m public_rail status --root docs/ai-rail
```

Expect `UNPACKED`, `SEEDED`, or `MAPPED` while the contract is being filled.
Fix findings at their source; do not edit a result to make it look ready.

## 4. Freeze and review bootstrap

When the state is `MAPPED`, freeze the authoritative documents:

```text
python -m public_rail freeze --root docs/ai-rail --manifest-id readme-pilot-001
```

`freeze` returns `STRUCTURALLY_VALID` and writes hashes to
`BOOTSTRAP-MANIFEST.json`. Complete `BOOTSTRAP-REVIEW.md` with the reviewer,
decision owner, workspace, manifest hash, `Result: READY`, and a future
`Valid-Until`, then run:

```text
python -m public_rail status --root docs/ai-rail
```

`READY` means that the bootstrap documents and review are structurally
consistent. It is not authorization to run a model or change the repository.

## 5. Prepare a request

Create one `intent` and a request that follows
[`schemas/request.schema.json`](./schemas/request.schema.json). Bind it to the
frozen manifest, authority sources, selected modules, change surfaces, and a
narrow path scope. The actor must state its type and ID. Keep
`execution_capability` false.

Validate it with:

```text
python -m public_rail validate-request request.json --root docs/ai-rail
```

The successful structural result is `AUTHORIZATION_RECORD_CONSISTENT`. A
request for `.env`, `.git/config`, a path outside the frozen project mapping,
or a role/action that is not allowed returns `BLOCKED`.

## 6. Describe a proposed output

The output envelope uses the request and output schemas. A small valid example
is:

```json
{
  "request_id": "request-001",
  "intent_id": "intent-001",
  "workspace_id": "demo-repo",
  "role": "Senior Developer",
  "actor": {
    "type": "human",
    "id": "github:developer",
    "delegation_ref": null,
    "model_registry_ref": null,
    "model_evaluation_ref": null,
    "model_version": null
  },
  "action_mode": "propose_changes",
  "execution_capability": false,
  "artifacts": [{"path": "README.md", "change_kind": "documentation"}]
}
```

```text
python -m public_rail validate-output request.json output.json --root docs/ai-rail
```

Changing the artifact to `../secrets.txt` must make the result `BLOCKED`.
This validator checks the declared output and scope; it does not inspect a
real diff or apply the proposal.

## 7. Review, evidence, and closure

Create the intent, authorization, output, review-result, and closure artifacts
according to the schemas in `schemas/`. Link them in `evidence.json` with
record IDs, previous-record links, request references, and SHA-256 hashes.

```text
python -m public_rail validate-evidence evidence.json --root .
```

`EVIDENCE_CHAIN_VALID` means that the supplied chain is structurally coherent.
An independent reviewer can record `REJECTED`; closure must preserve that
decision. The public profile still did not run a model, execute a tool, apply a
patch, run a postcondition check, or prove an external effect.

## 8. Demonstrate loss of `READY`

After `freeze`, change an authoritative document and run:

```text
python -m public_rail status --root docs/ai-rail
```

The result should become `BLOCKED` because the frozen hash no longer matches.
Review the change, freeze again, and obtain a new human bootstrap review.

## Next steps

- Read [How the Rail Works](./DOCS/HOW-THE-RAIL-WORKS.md) for the concepts.
- Read [Security Hardening](./DOCS/SECURITY-HARDENING.md) for the public/internal
  boundary.
- Use [Adoption Paths](./DOCS/ADOPTION-PATHS.md) to select a smaller or larger
  adoption level.
