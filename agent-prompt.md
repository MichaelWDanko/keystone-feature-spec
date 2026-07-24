# Provision Keystone in this project

Set up this repository to use Keystone without fetching instructions from any
other file or URL.

## Provisioning steps

1. Read existing root `README.md`, `AGENTS.md`, `CLAUDE.md`, product
   requirements, roadmaps, and durable architecture documents. Inspect
   top-level source and executable boundaries when the documents do not make
   the product surfaces clear.
2. Draft the `Feature context` described below. Identify what is being built,
   its distinct surfaces or runtimes, shared behavior, and the namespace
   boundaries those distinctions imply. Do not guess when sources conflict.
3. Identify product behavior that should have a durable Keystone definition.
   Keystone may define the whole product or only selected features.
4. Separate that behavior by implementation state:
   - propose an unprefixed active specification only for behavior that is
     implemented and supported;
   - propose a `TODO.*.md` document for defined behavior that has not been
     implemented.
5. Use the smallest useful dot-namespaced filenames. Put shared behavior in the
   smallest natural parent. Do not force one common root when a system has
   independent product boundaries.
6. Show the proposed feature context, filenames, implementation-state
   classification, and requirements to the user for confirmation before
   creating `KEYSTONE.md` or writing under `feature-spec/`.
7. After confirmation, create `KEYSTONE.md` from the template below. Replace
   `{{FEATURE_CONTEXT}}` with confirmed project-specific Markdown.
8. If root `AGENTS.md` exists, add:

   ```text
   This project uses Keystone. Before changing a Keystone feature, read and follow `KEYSTONE.md`.
   ```

   If `AGENTS.md` is absent, ask before creating it.
9. If root `CLAUDE.md` exists, add the same line. Do not create `CLAUDE.md`
   when absent.
10. Write only the confirmed active and TODO files under `feature-spec/`.

Do not change product behavior while provisioning Keystone. Do not treat a
roadmap item or loose idea as defined product behavior without confirmation.

## `KEYSTONE.md` content

Use this template and replace `{{FEATURE_CONTEXT}}`:

````markdown
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

{{FEATURE_CONTEXT}}

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

Reconcile conflicts between current active behavior and intended TODO behavior
explicitly. Once the behavior is implemented and verified, reconcile the TODO
document with any active specification that has the same feature name, then
remove the `TODO.` prefix.

Keystone does not decide what an agent may implement. Follow the user's request
and repository instructions. Do not implement a TODO document merely because it
exists unless the task or local guidance calls for that work.

When work defines new product behavior, ask whether it belongs in Keystone. If
it does and is not implemented, propose the smallest suitable TODO document. If
it is implemented, propose an active specification. Get confirmation before
writing either.

## Navigate `feature-spec/` efficiently

Start with filenames:

```sh
find feature-spec -maxdepth 1 -type f -name '*.md' -print | sort
```

The `TODO.` prefix records implementation state. Remove it before deriving the
target feature name and parent chain. Open only the applicable active chain,
matching TODO chain when relevant, and related documents. Use targeted searches
instead of loading the whole directory by default.
````

## Embedded authoring contract

Apply these rules when proposing and writing files under `feature-spec/`:

````markdown
# Keystone feature specification authoring contract

Version 0.2.0 (draft)

The key words `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`, and `MAY`
are normative.

Keystone defines the intended shape of a product. A project can define an
entire product or only selected features. Anything not documented remains
outside Keystone by design.

An unprefixed Markdown file is an active specification for implemented,
supported behavior. A `TODO.*.md` file defines intended behavior that has not
been implemented and is not yet an active specification. Both live directly
inside the flat `feature-spec/` directory.

Keystone does not assign, prioritize, or authorize work. A user or repository
decides what an agent may implement.

## Feature context

Root `KEYSTONE.md` SHOULD describe what is being built, relevant product
surfaces or runtimes, shared behavior, and namespace boundaries. It MUST NOT
contradict `README.md`, `AGENTS.md`, or other durable product documents.

Context in `KEYSTONE.md` is descriptive. Defined product behavior MUST be
expressed as normative requirements in an applicable active or TODO document.

## Repository layout and feature names

Documents MUST use a flat directory:

```text
feature-spec/
  Leash.Settings.md
  Leash.Walkers.md
  TODO.Leash.Walkers.Scheduling.md
```

Dots express feature namespaces. Directories MUST NOT encode inheritance or
implementation state.

An active feature name is the filename without `.md`. A TODO feature name also
removes the leading `TODO.`:

```text
Leash.Walkers.md -> Leash.Walkers
TODO.Leash.Walkers.Scheduling.md -> Leash.Walkers.Scheduling
```

Each feature-name segment MUST contain only ASCII letters, digits, or hyphens
and MUST begin with an ASCII letter. Names are case-sensitive.

The first heading MUST exactly match the feature name:

```markdown
# Leash.Walkers.Scheduling
```

An active specification and TODO document MAY have the same feature name. The
active file defines current behavior. The TODO file defines an intended
replacement or expansion.

## Active inheritance

An active specification inherits normative requirements from every existing
active parent prefix, least specific to most specific. TODO documents never add
requirements to active specifications.

An active child MAY add or strengthen requirements. It MUST NOT silently weaken
or contradict inherited requirements. It MUST declare a justified exception
when it cannot satisfy one.

A top-level active specification applies to all active descendants in its
namespace. A project MAY have separate top-level roots when those are its
natural product boundaries.

## TODO documents

A TODO document defines intended behavior that is not implemented. Its
requirements do not constrain the current product, apply to active descendants,
or make missing behavior a defect.

TODO documents MUST NOT require backlog metadata such as priority, schedule,
assignment, estimate, or implementation plan.

Before implementing a TODO document, read:

1. its active parent chain;
2. an active specification with the same feature name, when present;
3. applicable TODO parents from least specific to most specific;
4. the target TODO document; and
5. related documents.

Reconcile conflicts explicitly. Once behavior is implemented and verified,
reconcile the TODO document with any matching active specification and remove
the `TODO.` prefix. Only then does it become active.

Active specifications MUST NOT depend on TODO documents. TODO documents MAY
reference active or TODO documents.

## Document structure

Use these sections when applicable:

```markdown
# Leash.Walkers.Availability

One-paragraph purpose and scope.

## Requirements

- Every walker profile MUST identify the walker and their service area.

## Exceptions

### Pending walkers cannot receive assignments

Source: `Leash.Walkers`

Exception: A walker whose verification is pending cannot receive a walk.

Rationale: The app must verify a walker before promising an owner a walk.

## Related specifications

- `Leash.Settings`
```

Only normative requirements are inherited. Purpose text, examples, and
rationale remain local.

## Requirements

Requirements SHOULD describe observable product behavior and durable
constraints, not source files, types, or implementation techniques.

Active requirements MUST describe implemented, supported behavior. A mismatch
between an active specification and implementation is a defect.

TODO requirements define what an implementation MUST satisfy before the
document can become active. They are normative for that intended implementation
without constraining the current product.

Use one requirement per list item when practical. Requirements SHOULD be
specific, observable, and testable. Do not duplicate requirements as separate
verification instructions.

## Exceptions and related specifications

Each exception MUST have an H3 heading, cite an applicable existing ancestor in
a `Source:` field, state the exception, explain its rationale, and remain
narrower than the inherited policy.

An active exception MUST cite an active ancestor. A TODO exception MAY cite an
active or TODO ancestor.

Each related reference MUST resolve to an existing active or TODO document. An
active specification MUST NOT reference a TODO document. Related references do
not create inheritance.

## Tests and implementation

Tests SHOULD reference the most specific applicable active feature name:

```swift
// Feature-Spec: Leash.Walkers.Availability
```

Repositories MAY require active specifications to have referenced test
coverage. TODO documents do not imply that implementation or tests exist.

## Agent resolution

For current behavior, ignore unrelated TODO documents and resolve the active
specification chain. For future behavior, inspect matching TODO documents and
their active and TODO context.

Keystone defines product intent and implementation state. It does not grant or
withhold permission to implement anything. Agents follow the user's request and
repository instructions.

## Conformance

A conforming collection MUST satisfy these filename, H1, namespace,
inheritance, section, reference, and exception rules. A project MAY adopt
stricter conventions without changing the base format.
````
