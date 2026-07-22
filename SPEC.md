# Feature Spec Framework

Version 0.1.0 (draft)

This document defines the Feature Spec authoring format. The key words `MUST`,
`MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative.

A Feature Spec collection describes selected essential behavior that is
currently implemented, supported, and intended to remain. It need not describe
every feature in a project. Planned work, deferred ideas, and retired behavior
belong in roadmaps, issue trackers, or project history rather than the active
specification.

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
- `KEYSTONE.md` contains durable feature context plus instructions for finding
  and applying essential feature requirements.

The files MAY summarize the same facts, but they MUST NOT contradict one
another. `KEYSTONE.md` SHOULD contain enough context to choose a namespace
without requiring an agent to reverse-engineer system boundaries from source
files. It MAY link to another document for deeper operational or architectural
detail.

Project-specific feature context in `KEYSTONE.md` is descriptive. Essential
behavior that a project intends to preserve MUST be expressed as normative
requirements in an applicable file under `feature-spec/`, not only as prose in
`KEYSTONE.md`. This keeps project and namespace navigation separate from the
requirements inherited by implementations and tests.

For example, a fictional dog-walking app called Leash could describe three
namespace boundaries before defining individual features:

```text
Leash.Settings.*  shared app settings and safety controls
Leash.Owners.*    behavior specific to dog owners
Leash.Walkers.*   behavior specific to dog walkers
```

This context keeps shared app rules separate from requirements that apply only
to dog owners or dog walkers.

## 2. Repository layout

A project adopts Feature Spec by creating a `feature-spec/` directory. Every
Markdown file directly inside that directory defines one specification.

```text
feature-spec/
  Leash.Settings.md
  Leash.Owners.md
  Leash.Walkers.md
```

Specifications MUST use a flat directory. Dots in the filename express the
namespace. Directories MUST NOT encode specification inheritance.

## 3. Canonical names

The canonical name is the filename without the `.md` extension.

```text
Leash.Walkers.md -> Leash.Walkers
```

Each namespace segment MUST contain only ASCII letters, digits, or hyphens and
MUST begin with an ASCII letter. Names are case-sensitive.

A specification's first heading MUST be an H1 whose text exactly matches its
canonical name:

```markdown
# Leash.Walkers
```

Canonical names replace arbitrary feature identifiers. Requirements, tests,
change descriptions, and related specifications SHOULD reference these names.

## 4. Parent inheritance

A specification inherits every normative requirement from each existing parent
prefix, ordered from least specific to most specific.

The effective specification for `Leash.Walkers.Availability` is:

1. `Leash.md`, when present; and
2. `Leash.Walkers.md`, when present; and
3. `Leash.Walkers.Availability.md`.

Intermediate parents MAY be absent. Every parent that does exist still applies.

A child:

- MAY add requirements;
- MAY make an inherited requirement stricter;
- MUST NOT silently weaken or contradict an inherited requirement; and
- MUST declare a justified exception when its behavior cannot satisfy an
  inherited requirement.

Updating a parent immediately updates the effective requirements of every
descendant.

### Top-level namespace specifications

A top-level specification has a canonical name with one segment, such as
`Leash`. Its normative requirements apply to every descendant in that
namespace. It SHOULD contain only essential behavior shared across that whole
namespace.

A project with one clear product boundary MAY use a product-named top-level
specification for project-wide requirements. For example, `Leash.md` can hold
requirements inherited by `Leash.Owners` and `Leash.Walkers`. `KEYSTONE.md`
would still describe Leash, its runtime surfaces, and what those namespaces
represent.

A project is not required to have one project-wide root specification. A
monorepo or system with independent boundaries MAY use several top-level
namespaces, such as `Desktop`, `Server`, and `Shared`. Choose the smallest
natural roots that match the behavior being preserved; do not add an artificial
common parent only to make every specification descend from one file.

## 5. Document structure

A specification SHOULD use the following sections when applicable:

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

## 6. Requirements

Requirements SHOULD describe observable feature behavior and durable
constraints rather than source files, types, or implementation techniques.

Every requirement MUST describe behavior that is currently implemented,
supported, essential, and intended to remain. Requirements MUST NOT describe
planned, deferred, or retired behavior. A collection need not be exhaustive;
undocumented behavior does not automatically require a specification. A
mismatch between an active specification and the implementation is a defect to
reconcile explicitly; missing implementation or tests do not by themselves
authorize changing the specification.

Use one requirement per list item when practical. This improves review,
referencing, testing, and agent comprehension. Requirements SHOULD be specific,
observable, and testable where practical. The specification MUST NOT repeat a
requirement as a separate verification instruction.

## 7. Exceptions

Exceptions are escape hatches, not overrides.

Each exception MUST:

1. have its own H3 heading;
2. name an existing ancestor in a `Source:` field;
3. state the exception;
4. explain the rationale; and
5. remain narrower than the inherited policy it qualifies.

An exception MUST NOT cite a sibling, descendant, or unrelated specification.

## 8. Related specifications

Related specifications identify non-parent feature contracts that a maintainer
or agent should inspect before changing behavior. Each reference MUST resolve to
an existing canonical name.

Related references do not create inheritance.

## 9. Tests and implementation

Tests SHOULD reference the most specific applicable canonical name using a
language-appropriate comment or annotation:

```swift
// Feature-Spec: Leash.Walkers.Availability
```

```python
# Feature-Spec: Leash.Walkers.Availability
```

Repositories MAY require every specification to have referenced test coverage.
A test can reference more than one specification when it provides meaningful
evidence for each.

Source paths and test filenames SHOULD NOT be maintained in the specification as
the primary mapping because they change more often than feature intent.

## 10. Agent resolution

Before changing a documented feature, an agent SHOULD:

1. identify the most specific affected specification;
2. resolve and read all existing namespace parents;
3. read the target specification;
4. read its related specifications;
5. identify the effective inherited requirements;
6. preserve or deliberately update test coverage; and
7. record any approved requirement change or exception in the specification.

Agents MUST NOT treat missing implementation or missing tests as evidence that a
documented capability is obsolete.

When a requested change adds a new feature or materially expands behavior that
is not covered by the applicable specifications, an agent MUST ask the user
whether the behavior should be in Keystone's scope. The agent SHOULD propose
the smallest suitable namespace, requirements, and related specifications. If
the user confirms that it should be in scope, the agent MUST receive explicit
confirmation of the proposed specification change before writing it. If the
user declines, the behavior remains outside the documented collection.

## 11. Conformance

A conforming Feature Spec collection MUST satisfy the filename, H1, namespace,
document-section, parent-reference, related-reference, and exception rules in
this document. A conforming Keystone setup MUST also give agents feature context
that is sufficient to distinguish the surfaces represented by its
top-level namespaces.

A project MAY adopt stricter conventions without changing the meaning of the
base format.
