# PROJECT CONTRACT

Project: <host-project-name>
Component: project-layer-template
Status: DRAFT
Template-Schema-Version: v0.3.0
Date: <YYYY-MM-DD>
Review-Date: <YYYY-MM-DD>

## 1. Project Identity

- repository: <name>
- owner: <human decision owner>
- status: <active / bootstrap / archived>

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

Canonical source: `./CODEBASE-VOICE.md`

Summary:
- <one or two project-level conventions>

## 6. Approved Integration Points

Canonical source: `./INTEGRATION-POINTS.md`

Summary:
- <one or two approved boundary categories>

## 7. Do-Not-Touch Areas

- <restricted area>

## 8. Local Exceptions

- <none | explicit bounded exception>

## 9. Selected Modules

- <module-name>
- <module-name>

## 10. Review Focus

- <highest-risk local review focus>

## 11. Contract Precedence

- this document is the top-level index and project contract;
- a specialized contract overrides its summary in this document;
- a disagreement between documents is a validation failure and must be resolved
  by the human decision owner before implementation.
