# Why AI Rail?

## Purpose and audience

This explanation is for people who use an AI assistant around a software
repository but still need human decisions, bounded changes, and a traceable
record. It is not a model-selection guide and it does not describe a private
execution platform.

## The practical problem

An AI assistant can produce a plausible answer while missing the repository's
implicit constraints. A request such as “update the CI documentation” may
quietly expand into changing workflows, credentials, release policy, or a
provider integration. The assistant may also see a README, an issue, a stale
design note, and a current project contract that disagree.

The problem is not solved by asking the model to be more confident. The host
project needs an explicit decision owner, authoritative documents, a bounded
`scope`, and a reviewable record of what was proposed.

## Why prompts are not enough

A system prompt or `AGENTS.md` can provide useful instructions, but neither is
automatically a complete authority model. Prompts do not by themselves prove
which document is current, whether a reviewer is independent, whether a path
is in scope, or whether a proposed output corresponds to the original
`intent`. They are also not an identity service or a postcondition check.

AI Rail therefore treats repository content and model-generated text as data
until a human-owned contract classifies it. The public profile records and
validates that structure; it does not call a model or execute a tool.

## A small example

Suppose a maintainer asks an assistant to add a section to `README.md`. The
assistant finds an old issue asking for a deployment change and a README note
that says “print the environment for debugging.” Without a rail, the next
step depends on chat context and the assistant's interpretation. With a rail:

1. the human records one `intent` and a narrow `scope`;
2. `PROJECT.md` and adopted contracts identify the authority sources;
3. `.env`, deployment files, and unrelated paths are denied explicitly;
4. a proposal names its artifacts and change kinds;
5. an independent reviewer can reject scope expansion; and
6. `evidence` connects the intent, authorization record, output, review, and
   `closure`.

The rail does not decide whether the README wording is good. It makes the
decision boundary and the resulting record easier to inspect.

## What the rail separates

- **Human authority:** the person who owns the final project decision.
- **Project truth:** active, owned documents and their frozen manifest.
- **Proposal:** a request or output that may still be rejected.
- **Review:** an independent assessment of the proposed result.
- **Evidence:** structured links and hashes that make the sequence
  reconstructable.

A role name is not an identity. A valid JSON document is not automatically a
true statement. A matching hash proves byte integrity, not correctness. A
`READY` bootstrap is not permission to execute work.

## Why constrain the work?

The public profile focuses on reducing the blast radius of a mistake: fewer
paths, fewer change kinds, explicit owners, and a reviewable sequence. This is
often more useful than trying to make a probabilistic model “perfectly smart.”
The same approach helps a person who maintains one repository. A small project
can use only `PROJECT.md`, a narrow scope, and a human review; it does not need
an autonomous agent or a private platform to benefit from explicit boundaries.

## Read next

- [How the rail works](./HOW-THE-RAIL-WORKS.md) for the contract flow and
  states.
- [Quickstart](../QUICKSTART.md) for an offline adoption walkthrough.
- [Security hardening](./SECURITY-HARDENING.md) for public guarantees and
  internal responsibilities.
- [Documentation matrix](./DOCUMENTATION-MATRIX.md) for English and Czech
  coverage.
