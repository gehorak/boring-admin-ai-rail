# Quickstart

Use this kit as a starting point for a local governance layer in an existing
repository.

1. Read [the fictional example](./examples/fictional-project/) to see the
   intended level of detail.
2. Create `docs/ai-rail/` in the adopting repository and name one human
   decision owner.
3. Copy these required templates into that directory and complete them in this
   order: `PROJECT.md`, `PROJECT-CONTEXT.md`, and
   `ARCHITECTURE-CANON.md`.
4. Add `CODEBASE-VOICE.md` when local code conventions matter, and add
   `INTEGRATION-POINTS.md` when the change can cross an external or protected
   boundary.
5. Remove every placeholder or mark it `N/A`; set `Contract-Status: ACTIVE`,
   `Owner`, and `Review-Date` only after the human decision owner approves the
   document. `Project-State` remains a separate description of the host
   project, such as `bootstrap` or `active`.
6. Before implementation, give the AI tool the active project contract and
   applicable specialized contracts. Treat any missing, conflicting, or
   `DRAFT` contract as a reason to ask the human owner rather than infer a
   decision.

Adoption is complete when the decision owner is named; in-scope,
out-of-scope, and do-not-touch areas are non-empty; relevant integration trust
boundaries are recorded; and all active documents have been human-approved.

This kit supplies a reference structure. Each adopting project remains
responsible for its own implementation, tooling, access controls, testing,
and release process.
