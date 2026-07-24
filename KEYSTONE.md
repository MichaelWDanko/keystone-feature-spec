# Keystone agent guidance

This project uses Keystone to define intended product behavior beside the code.
The Markdown files in `feature-spec/` are the durable source of truth for the
parts of the product the project chooses to define.

Unprefixed files are active Keystone specifications. They describe implemented,
supported behavior. Implementation and tests MUST follow their applicable
requirements. A mismatch is a defect to resolve explicitly.

Files prefixed with `TODO.` define intended behavior that has not been
implemented. They are not active specifications and do not constrain the
current product. When work implements a TODO document, its requirements define
what the completed feature must do.

## Feature context

Keystone is a Markdown-native framework for defining the intended shape of a
whole product or selected features. This repository contains the framework
contract, reusable agent guidance, a validator, examples, and the static
documentation site.

The repository has three distinct surfaces:

- `KEYSTONE.md` gives agents durable product context and navigation guidance;
- `feature-spec/` collections define current and intended behavior through
  flat, dot-namespaced Markdown files; and
- the validator and rendered documentation explain and check the framework
  without becoming another source of product requirements.

Use `README.md` for the human-facing project overview and setup instructions.
Use `AGENTS.md` for repository-wide working rules. Keep enough context here for
an agent to choose the right feature namespace without inferring the product
shape from source files.

Product context in this file is descriptive. Normative product behavior belongs
in active or TODO documents under `feature-spec/`.

## Before changing implemented behavior

An agent MUST:

1. list the filenames in `feature-spec/`;
2. ignore unrelated `TODO.*.md` files;
3. identify the most specific active specification affected by the work;
4. read its active namespace parents from least specific to most specific;
5. read the target and its active related specifications;
6. identify inherited requirements and declared exceptions;
7. make implementation and tests conform to the effective active
   specification; and
8. report conflicts instead of silently weakening or removing a requirement.

## When working on unimplemented behavior

When a task concerns future behavior, inspect matching `TODO.*.md` files. Before
implementing a TODO document, read:

1. its applicable active parent chain;
2. an active specification with the same feature name, when present;
3. applicable TODO parents from least specific to most specific;
4. the target TODO document; and
5. its related documents.

Reconcile conflicts between the current active behavior and intended TODO
behavior explicitly. Once the behavior is implemented and verified, reconcile
the TODO document with any active specification that has the same feature name,
then remove the `TODO.` prefix. The resulting active specification must describe
the behavior that now exists.

Keystone does not decide what an agent may implement. Follow the user's request
and the repository's operating instructions. Do not implement a TODO document
merely because it exists unless the task or local guidance calls for that work.

When work defines new product behavior, ask whether it belongs in Keystone. If
it does and is not yet implemented, propose the smallest suitable TODO document.
If it is already implemented, propose an active specification. Get confirmation
before writing either.

## Navigate `feature-spec/` efficiently

Start with filenames instead of loading every document:

```sh
find feature-spec -maxdepth 1 -type f -name '*.md' -print | sort
```

For current work on `Leash.Walkers`, inspect active files in that parent chain
and active related specifications. For future scheduling work, also inspect:

```text
feature-spec/
  Leash.Walkers.md
  TODO.Leash.Walkers.Scheduling.md
```

The `TODO.` prefix records implementation state. Remove it before deriving the
target feature name and parent chain. Use targeted searches to find relevant
cross-cutting requirements; do not concatenate the whole directory by default.
