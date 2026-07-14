# PROJECT CONTRACT

Project: <host-project-name>
Component: project-layer-template
Contract-Status: DRAFT
Template-Schema-Version: v0.3.1
Date: <YYYY-MM-DD>
Review-Date: <YYYY-MM-DD>
Owner: <human document owner>

## 1. Project Identity

- repository: <name>
- decision owner: <human decision owner>
- project state: <active / bootstrap / archived>

## 2. Project Purpose

- <why this repository exists>

## 3. System Boundaries

- in scope: <boundary>
- out of scope: <boundary>

## 4. Architectural Canon

Canonical source: `./ARCHITECTURE-CANON.md`

Summary:
- <one or two project-level boundary rules>

## 5. Codebase Voice

Canonical source when adopted: `./CODEBASE-VOICE.md`

If this contract is not adopted, record `N/A` and keep the summary below
within the active project contract.

Summary:
- <one or two project-level conventions>

## 6. Approved Integration Points

Canonical source when adopted: `./INTEGRATION-POINTS.md`

If this contract is not adopted, record `N/A` and keep the summary below
within the active project contract.

Summary:
- <one or two approved boundary categories>

## 7. Do-Not-Touch Areas

- <restricted area>

## 8. Local Exceptions

- <none | explicit bounded exception>

## 9. Selected Modules

Use this optional section only for modules that the adopting project defines.
This kit does not provide a module catalog or module ownership model.

- <module-name | N/A>

## 10. Review Focus

- <highest-risk local review focus>

## 11. Contract Precedence

- this document is the top-level index and project contract;
- an active specialized contract overrides its summary in this document when
  that contract is adopted;
- a disagreement between documents is a validation failure and must be resolved
  by the human decision owner before implementation.
