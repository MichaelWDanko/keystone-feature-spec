# Keystone Feature Specification

Version 0.2.0 (draft)

This document defines the Keystone authoring format. The key words `MUST`,
`MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative.

Keystone defines the intended shape of a product in plain Markdown. A project
can define an entire product or only the features that need a durable contract.
Anything not documented remains outside Keystone by design.

Documents in `feature-spec/` have two states:

- an unprefixed Markdown file is an active Keystone specification for behavior
  that is implemented, supported, and intended to remain; and
- a `TODO.*.md` file defines intended behavior that has not been implemented
  and is not yet an active Keystone specification.

Both states keep current and intended product behavior in one discoverable
directory. Keystone does not assign, prioritize, or authorize work. A user or
repository decides what an agent may implement.

## 1. Feature context

A project SHOULD use root `KEYSTONE.md` to describe enough feature context for a
person or agent to understand what is being built before choosing a feature
namespace. The context SHOULD identify:

- the project's purpose and intended users, when relevant;
- distinct surfaces, executables, services, or runtimes;
- behavior shared across those surfaces; and
- the namespace boundaries implied by those distinctions.

`KEYSTONE.md` MAY be self-contained when a project is starting fresh. When
`README.md` or `AGENTS.md` already exists, the files have compatible roles:

- `README.md` is the human-facing overview, setup, and usage guide;
- `AGENTS.md` contains repository-wide working instructions; and
- `KEYSTONE.md` contains durable product context plus instructions for finding
  and applying feature documents.

The files MAY summarize the same facts, but they MUST NOT contradict one
another. `KEYSTONE.md` SHOULD contain enough context to choose a namespace
without requiring an agent to reverse-engineer system boundaries from source
files. It MAY link to another document for deeper operational or architectural
detail.

Project-specific context in `KEYSTONE.md` is descriptive. Defined product
behavior MUST be expressed as normative requirements in an applicable active or
TODO document under `feature-spec/`, not only as prose in `KEYSTONE.md`.

For example, a fictional dog-walking app called Leash could describe three
namespace boundaries before defining individual features:

```text
Leash.Settings.*  shared app settings and safety controls
Leash.Owners.*    behavior specific to dog owners
Leash.Walkers.*   behavior specific to dog walkers
```

## 2. Repository layout

A project adopts Keystone by creating a flat `feature-spec/` directory:

```text
feature-spec/
  Leash.Settings.md
  Leash.Owners.md
  Leash.Walkers.md
  TODO.Leash.Walkers.Scheduling.md
```

Every unprefixed Markdown file directly inside the directory defines one active
specification. Every Markdown file beginning with `TODO.` defines one
unimplemented feature document. Directories MUST NOT encode specification
inheritance or implementation state.

## 3. Feature names

An active specification's feature name is its filename without `.md`:

```text
Leash.Walkers.md -> Leash.Walkers
```

A TODO document's feature name removes both the `TODO.` prefix and `.md`:

```text
TODO.Leash.Walkers.Scheduling.md -> Leash.Walkers.Scheduling
```

`TODO.` is file-level implementation state and is not part of the target feature
namespace. Each feature-name segment MUST contain only ASCII letters, digits,
or hyphens and MUST begin with an ASCII letter. Names are case-sensitive.

The first heading MUST be an H1 whose text exactly matches the feature name:

```markdown
# Leash.Walkers.Scheduling
```

An active specification and a TODO document MAY have the same feature name.
The active file defines current behavior. The TODO file defines an intended
replacement or expansion that has not been implemented.

Requirements, tests, change descriptions, and related specifications SHOULD
reference feature names. References to TODO documents MUST include `TODO.` when
the distinction matters.

## 4. Active parent inheritance

An active specification inherits every normative requirement from each active
parent prefix, ordered from least specific to most specific.

The effective active specification for `Leash.Walkers.Availability` is:

1. `Leash.md`, when present;
2. `Leash.Walkers.md`, when present; and
3. `Leash.Walkers.Availability.md`.

TODO documents never add requirements to an active specification. Intermediate
active parents MAY be absent. Every active parent that exists still applies.

An active child:

- MAY add requirements;
- MAY make an inherited requirement stricter;
- MUST NOT silently weaken or contradict an inherited requirement; and
- MUST declare a justified exception when its behavior cannot satisfy an
  inherited requirement.

Updating an active parent immediately updates the effective requirements of
every active descendant.

### Top-level namespace specifications

A top-level active specification has a feature name with one segment, such as
`Leash`. Its normative requirements apply to every active descendant in that
namespace. It SHOULD contain only behavior shared across the whole namespace.

A project is not required to have one project-wide root. A monorepo or system
with independent boundaries MAY use several top-level namespaces, such as
`Desktop`, `Server`, and `Shared`.

## 5. TODO documents

A TODO document defines intended product behavior that is not implemented. Its
requirements do not describe the current product, do not apply to active
descendants, and do not make missing behavior a defect.

TODO documents are not backlog items. They MUST NOT require priority, schedule,
assignment, estimates, or an implementation plan. Their purpose is to define
the intended behavior clearly enough to guide implementation when that work is
chosen.

Keystone does not decide when or whether a TODO document is implemented. A user,
agent prompt, or repository policy controls that work.

Before implementing a TODO document, a person or agent SHOULD read:

1. the applicable active parent chain;
2. an active specification with the same feature name, when present;
3. applicable TODO parents from least specific to most specific;
4. the target TODO document; and
5. its related documents.

The implementation MUST reconcile conflicts between current active behavior and
the intended TODO behavior explicitly. Once the behavior is implemented and
verified, the TODO document MUST be reconciled with any matching active
specification and renamed without `TODO.`. Only then does it become an active
Keystone specification and participate in active inheritance.

Active specifications MUST NOT depend on TODO documents through related
references or exception sources. TODO documents MAY reference active or TODO
documents.

## 6. Document structure

An active specification or TODO document SHOULD use the following sections when
applicable:

```markdown
# Leash.Walkers.Availability

One-paragraph purpose and scope.

## Requirements

- Every walker profile MUST identify the walker and their service area.

## Exceptions

### Unavailable walkers cannot receive new assignments

Source: `Leash.Walkers`

Exception: An unavailable walker cannot be assigned a new walk.

Rationale: The app must not promise an owner a walk that the walker cannot
accept.

## Related specifications

- `Leash.Settings`
```

Only requirements expressed with normative terms are inherited. Purpose text,
examples, and rationale remain local unless another document explicitly
references them.

## 7. Requirements

Requirements SHOULD describe observable product behavior and durable
constraints rather than source files, types, or implementation techniques.

In an active specification, every requirement MUST describe behavior that is
implemented, supported, and intended to remain. A mismatch between an active
specification and the implementation is a defect to reconcile explicitly.
Missing implementation or tests do not authorize changing an active
specification.

In a TODO document, requirements define the behavior that an implementation
MUST satisfy before the document can become active. They remain normative for
that intended implementation even though they do not constrain the current
product.

Use one requirement per list item when practical. Requirements SHOULD be
specific, observable, and testable where practical. A document MUST NOT repeat
a requirement as a separate verification instruction.

## 8. Exceptions

Exceptions are escape hatches, not overrides.

Each exception MUST:

1. have its own H3 heading;
2. name an applicable existing ancestor in a `Source:` field;
3. state the exception;
4. explain the rationale; and
5. remain narrower than the inherited policy it qualifies.

An active exception MUST cite an active ancestor. A TODO exception MAY cite an
active ancestor or a TODO ancestor. An exception MUST NOT cite a sibling,
descendant, or unrelated document.

## 9. Related specifications

Related specifications identify non-parent feature contracts that a maintainer
or agent should inspect before changing behavior. Each reference MUST resolve
to an existing active specification or TODO document.

An active specification MUST NOT reference a TODO document. A TODO document MAY
reference either state. Related references do not create inheritance.

## 10. Tests and implementation

Tests SHOULD reference the most specific applicable active feature name using a
language-appropriate comment or annotation:

```swift
// Feature-Spec: Leash.Walkers.Availability
```

```python
# Feature-Spec: Leash.Walkers.Availability
```

Repositories MAY require every active specification to have referenced test
coverage. TODO documents do not imply that implementation or tests exist.

Source paths and test filenames SHOULD NOT be maintained in a specification as
the primary mapping because they change more often than product intent.

## 11. Agent resolution

For work on current behavior, an agent SHOULD ignore unrelated TODO documents
and resolve the applicable active specification chain.

For work that implements or plans future behavior, an agent SHOULD inspect
matching TODO documents and their active and TODO context as described in
section 5.

Keystone defines product intent and implementation state. It does not grant or
withhold permission to implement anything. Agents follow the user's request and
the repository's operating instructions.

When work adds behavior that is not documented, an agent SHOULD ask whether the
behavior belongs in Keystone. With confirmation, it SHOULD create the smallest
suitable TODO document before implementation or active specification after
implementation.

## 12. Conformance

A conforming Keystone collection MUST satisfy the filename, H1, namespace,
document-section, parent-reference, related-reference, and exception rules in
this document. A conforming setup MUST also provide enough feature context to
distinguish its top-level namespaces.

A project MAY adopt stricter conventions without changing the meaning of the
base format.
