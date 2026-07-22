# Provision Keystone in this project

Set up this repository to use Keystone without fetching instructions from any
other file or URL.

## Provisioning steps

1. Read any existing root `README.md`, `AGENTS.md`, `CLAUDE.md`, and durable
   architecture or project overview documents. Inspect top-level source and
   executable boundaries when the documents do not make the relevant surfaces
   clear.
2. Draft the `Feature context` section described below. It must identify what
   is being built, its distinct surfaces or runtimes, shared behavior,
   and the namespace boundaries those distinctions imply. Keep this context
   descriptive. Put essential behavior the project intends to preserve in
   normative requirements under `feature-spec/`, not only in `KEYSTONE.md`. If
   the repository does not provide enough evidence, or existing documents
   conflict, ask the user for the missing context instead of guessing.
3. Use the embedded authoring contract below to identify currently implemented
   behavior that appears essential and intentionally preserved. Keystone need
   not cover every feature.
4. Use the drafted surfaces to propose the smallest useful set of dot-namespaced
   Markdown files under `feature-spec/`. When project-wide requirements share
   one natural product boundary, propose a product-named top-level
   specification such as `Leash.md` so its requirements are inherited by
   descendants. Do not force one common root when a monorepo or system has
   independent boundaries. Keep shared behavior in the smallest natural parent
   namespace and surface-specific behavior in distinct child namespaces. Do
   not include planned, deferred, deprecated, or retired behavior.
5. Show the proposed feature context, filenames, and requirements to the user
   for confirmation before creating `KEYSTONE.md` or writing any files under
   `feature-spec/`.
6. After confirmation, create `KEYSTONE.md` in the repository root from the
   template in the `KEYSTONE.md content` section below, replacing
   `{{FEATURE_CONTEXT}}` with the confirmed feature context. Do not leave the
   placeholder in the file.
7. If a root `AGENTS.md` exists, add this line to it:

   ```text
   This project uses Keystone. Before changing a Keystone feature, read and follow `KEYSTONE.md`.
   ```

   If `AGENTS.md` does not exist, ask the user whether it should be created.
   Do not create it without explicit confirmation.
8. If a root `CLAUDE.md` exists, add the same line to it. Do not create
   `CLAUDE.md` when it is absent.
9. Write only the confirmed files under `feature-spec/`.

Do not change existing behavior while provisioning Keystone. Report any
conflict or uncertainty instead of inventing a requirement.

## `KEYSTONE.md` content

Use the following template for the new root `KEYSTONE.md`. Replace
`{{FEATURE_CONTEXT}}` with confirmed project-specific Markdown. Keep the rest
of the template unchanged:

````markdown
# Keystone agent guidance

This project uses Keystone to keep essential feature requirements separate from
their implementation. Treat the Markdown documents in `feature-spec/` as the
durable source of truth for behavior the project intentionally preserves.
Implementation and tests MUST follow the applicable feature specifications.
A mismatch between a specification and the implementation is a defect to
resolve explicitly. Missing code or tests MUST NOT be treated as permission to
remove a documented requirement.

## Feature context

{{FEATURE_CONTEXT}}

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
  Leash.Settings.md
  Leash.Owners.md
  Leash.Walkers.md
```

For work on `Leash.Walkers`, inspect only:

1. `Leash.md`, if it exists;
2. `Leash.Walkers.md`; and
3. relevant files named in the target's `Related specifications` section.

Start with filenames instead of file contents:

```sh
find feature-spec -maxdepth 1 -type f -name '*.md' -print | sort
```

Narrow candidates by namespace or feature language before opening files:

```sh
find feature-spec -maxdepth 1 -type f -name 'Leash*.md' -print | sort
rg -n -i 'walker availability|dog walker' feature-spec
```

Derive the parent chain from the selected file's dot-separated name. Open only
that chain and relevant related specifications. Use targeted searches to find
cross-cutting requirements; do not concatenate the whole directory as a
default discovery step.

If no applicable specification exists, follow the repository's other guidance.
Do not create a specification unless the user asks to preserve that behavior
through Keystone or confirms a proposal to do so.
````

## Embedded authoring contract

Apply all of these rules when proposing and writing files under
`feature-spec/`:

````markdown
# Keystone feature specification authoring contract

Version 0.1.0 (draft)

The key words `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`, and `MAY`
are normative.

A `feature-spec/` collection is the set of Markdown specification files in a
project's `feature-spec/` directory. It describes selected essential behavior
that is currently implemented, supported, and intended to remain. It need not
describe every feature in the project. Planned work, deferred ideas, and
retired behavior belong in roadmaps, issue trackers, or project history rather
than the active specifications.

## Feature context

Root `KEYSTONE.md` SHOULD describe what is being built, the distinct surfaces
or runtimes relevant to its essential features, shared behavior, and the
namespace boundaries implied by those distinctions. It MAY be self-contained
for a new project. When `README.md` or `AGENTS.md` exists, use compatible roles:
`README.md` for the
human-facing overview and setup, `AGENTS.md` for repository-wide working rules,
and `KEYSTONE.md` for durable feature context and specification navigation.

These files MUST NOT contradict one another. `KEYSTONE.md` SHOULD contain
enough context to choose a namespace without reverse-engineering system
boundaries from source files. Keep shared behavior in a shared namespace and
surface-specific behavior in separate namespaces.

Project-specific feature context in `KEYSTONE.md` is descriptive. Essential
behavior that a project intends to preserve MUST be expressed as normative
requirements in an applicable file under `feature-spec/`, not only as prose in
`KEYSTONE.md`. This keeps project and namespace navigation separate from the
requirements inherited by implementations and tests.

## Repository layout

Every Markdown file directly inside `feature-spec/` defines one specification.
Specifications MUST use a flat directory. Dots in the filename express the
namespace. Directories MUST NOT encode specification inheritance.

## Canonical names

The canonical name is the filename without the `.md` extension. Each namespace
segment MUST contain only ASCII letters, digits, or hyphens and MUST begin with
an ASCII letter. Names are case-sensitive.

A specification's first heading MUST be an H1 whose text exactly matches its
canonical name:

```markdown
# Leash.Walkers
```

Requirements, tests, change descriptions, and related specifications SHOULD
reference canonical names instead of arbitrary feature identifiers.

## Parent inheritance

A specification inherits every normative requirement from each existing parent
prefix, ordered from least specific to most specific. The effective
specification for `Leash.Walkers.Availability` is:

1. `Leash.md`, when present; and
2. `Leash.Walkers.md`, when present; and
3. `Leash.Walkers.Availability.md`.

Intermediate parents MAY be absent. Every parent that exists still applies. A
child MAY add requirements or make an inherited requirement stricter. It MUST
NOT silently weaken or contradict an inherited requirement and MUST declare a
justified exception when its behavior cannot satisfy one.

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

## Document structure

A specification SHOULD use these sections when applicable:

```markdown
# Leash.Walkers.Availability

One-paragraph purpose and scope.

## Requirements

- Every walker profile MUST identify the walker and their service area.

## Exceptions

### Pending-verification walkers cannot receive new assignments

Source: `Leash.Walkers`

Exception: A walker whose verification is pending cannot be assigned a new
walk.

Rationale: The app must verify a walker before promising an owner a walk.

## Related specifications

- `Leash.Settings`
```

Only requirements expressed with normative terms are inherited. Purpose text,
examples, and rationale remain local unless another document explicitly
references them.

## Requirements

Requirements SHOULD describe observable feature behavior and durable
constraints rather than source files, types, or implementation techniques.
Every requirement MUST describe behavior that is currently implemented,
supported, essential, and intended to remain. Requirements MUST NOT describe
planned, deferred, or retired behavior. The `feature-spec/` collection need not
be exhaustive; undocumented behavior does not automatically require a
specification.

A mismatch between the active specification and the implementation is a defect
to reconcile explicitly. Missing implementation or tests do not authorize
changing the specification. Use one requirement per list item when practical.
Requirements SHOULD be specific, observable, and testable. Do not repeat a
requirement as a separate verification instruction.

## Exceptions

Each exception MUST:

1. have its own H3 heading;
2. name an existing ancestor in a `Source:` field;
3. state the exception;
4. explain the rationale; and
5. remain narrower than the inherited policy it qualifies.

An exception MUST NOT cite a sibling, descendant, or unrelated specification.

## Related specifications

Related specifications identify non-parent feature contracts to inspect before
changing behavior. Each reference MUST resolve to an existing canonical name.
Related references do not create inheritance.

## Tests and implementation

Tests SHOULD reference the most specific applicable canonical name using a
language-appropriate comment or annotation, such as:

```swift
// Feature-Spec: Leash.Walkers.Availability
```

Repositories MAY require every specification to have referenced test coverage.
A test can reference more than one specification when it provides meaningful
evidence for each. Source paths and test filenames SHOULD NOT be the primary
mapping because they change more often than feature intent.

## Agent resolution

Before changing a documented feature, an agent SHOULD identify the most specific
affected specification; resolve and read all existing namespace parents; read
the target and related specifications; identify effective inherited
requirements; preserve or deliberately update test coverage; and record any
approved requirement change or exception in the specification.

Agents MUST NOT treat missing implementation or missing tests as evidence that
a documented capability is obsolete.

When a requested change adds a new feature or materially expands behavior that
is not covered by the applicable specifications, an agent MUST ask the user
whether the behavior should be in Keystone's scope. If the user confirms that
it should, the agent MUST propose and receive explicit confirmation of the
smallest suitable specification change before writing it. If the user declines,
the behavior remains outside the documented collection.

## Conformance

A conforming `feature-spec/` collection MUST satisfy the filename, H1,
namespace, document-section, parent-reference, related-reference, and exception
rules above. A project MAY adopt stricter conventions without changing the
meaning of Keystone's base format.
````
