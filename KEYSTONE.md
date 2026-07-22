# Keystone agent guidance

This project uses Keystone to keep essential feature requirements separate from
their implementation. Treat the Markdown documents in `feature-spec/` as the
durable source of truth for behavior the project intentionally preserves.
Implementation and tests MUST follow the applicable feature specifications.
A mismatch between a specification and the implementation is a defect to
resolve explicitly. Missing code or tests MUST NOT be treated as permission to
remove a documented requirement.

## Feature context

Keystone is a Markdown-native framework for keeping selected essential feature
behavior separate from its implementation. This repository contains the
framework contract, reusable agent guidance, a validator, examples, and the
static documentation site.

The repository has three distinct surfaces:

- `KEYSTONE.md` gives agents durable feature context and instructions for
  resolving essential requirements;
- `feature-spec/` collections describe supported behavior through flat,
  dot-namespaced Markdown files; and
- the validator and rendered documentation explain and check the framework
  without becoming a second source of feature requirements.

Use `README.md` for the human-facing project overview and setup instructions.
Use `AGENTS.md` for repository-wide working rules. Keep enough feature context
in `KEYSTONE.md` for an agent to understand the relevant surfaces and choose the
right feature namespace without having to infer those boundaries from source
files.

Project-specific context in this file is descriptive. Essential behavior that
the project intends to preserve belongs in normative requirements under
`feature-spec/`. A top-level specification holds requirements shared by its
namespace descendants; repositories with independent product boundaries may
use several top-level specifications instead of one artificial common root.

## Before changing a Keystone feature

An agent MUST:

1. list the filenames in `feature-spec/` and identify the most specific
   specification affected by the work;
2. read that specification's existing namespace parents from least specific to
   most specific;
3. read the target specification and any files named in its
   `Related specifications` section;
4. identify the inherited requirements and any declared exceptions;
5. make the implementation and test coverage conform to the effective
   specification; and
6. report any conflict between the requested work and the specifications
   instead of silently weakening, bypassing, or removing a requirement.

## When adding a new feature

When a requested change adds a new feature or materially expands behavior that
is not covered by the applicable specifications, an agent MUST ask the user
whether the behavior should be in Keystone's scope. The agent SHOULD include a
short proposal for the smallest suitable namespace, requirements, and related
specifications so the user can make that decision.

If the user confirms that the behavior belongs in Keystone, the agent MUST get
explicit confirmation of the proposed specification change before creating or
updating the file, then implement and test against the approved requirements.
If the user declines, the agent MUST NOT create a specification for that
behavior and SHOULD note that it remains outside Keystone's documented scope.

Keystone is not required to describe every implemented feature. A feature with
no applicable specification is not governed by Keystone merely because it
exists. When the user chooses behavior as essential and intended to remain, add
or update the smallest suitable specification after explicit confirmation.

Change an existing feature specification only when the user explicitly
requests or confirms the change. A request to change implementation alone does
not authorize a specification change. Once behavior is documented, treat it as
essential until the user confirms otherwise.

Active specifications describe only essential behavior that is currently
implemented, supported, and intended to remain. Keep planned work, deferred
ideas, and retired behavior in the project's planning or history documents.

## Navigate `feature-spec/` efficiently

Do not load every specification into context. The flat, dot-separated
filenames form a namespace. For example:

```text
feature-spec/
  Lending.md
  Lending.Loans.md
  Lending.Loans.Returns.md
  Catalog.md
  Catalog.Availability.md
```

For work on `Lending.Loans.Returns`, inspect only:

1. `Lending.md`, if it exists;
2. `Lending.Loans.md`, if it exists;
3. `Lending.Loans.Returns.md`; and
4. relevant files named in the target's `Related specifications` section.

Start with filenames instead of file contents:

```sh
find feature-spec -maxdepth 1 -type f -name '*.md' -print | sort
```

Narrow candidates by namespace or feature language before opening files:

```sh
find feature-spec -maxdepth 1 -type f -name 'Lending*.md' -print | sort
rg -n -i 'return item|loan return' feature-spec
```

Derive the parent chain from the selected file's dot-separated name. Open only
that chain and relevant related specifications. Use targeted searches to find
cross-cutting requirements; do not concatenate the whole directory as a
default discovery step.

If no applicable specification exists, follow the repository's other guidance.
Do not create a specification unless the user asks to preserve that behavior
through Keystone or confirms a proposal to do so.
