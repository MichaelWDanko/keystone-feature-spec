# Feature Spec Framework

This document defines the Feature Spec authoring format. The key words `MUST`,
`MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative.

## 1. Repository layout

A project adopts Feature Spec by creating a `feature-spec/` directory. Every
Markdown file directly inside that directory defines one specification.

```text
feature-spec/
  Settings.md
  Settings.Accounts.md
  Settings.Accounts.Removal.md
  Search.md
  Search.IndexManagement.md
```

Specifications MUST use a flat directory. Dots in the filename express the
namespace. Directories MUST NOT encode specification inheritance.

## 2. Canonical names

The canonical name is the filename without the `.md` extension.

```text
Settings.Accounts.md -> Settings.Accounts
```

Each namespace segment MUST contain only ASCII letters, digits, or hyphens and
MUST begin with an ASCII letter. Names are case-sensitive.

A specification's first heading MUST be an H1 whose text exactly matches its
canonical name:

```markdown
# Settings.Accounts
```

Canonical names replace arbitrary feature identifiers. Requirements, tests,
change descriptions, and related specifications SHOULD reference these names.

## 3. Parent inheritance

A specification inherits every normative requirement from each existing parent
prefix, ordered from least specific to most specific.

The effective specification for `Settings.Accounts.Removal` is:

1. `Settings.md`, when present;
2. `Settings.Accounts.md`, when present; and
3. `Settings.Accounts.Removal.md`.

Intermediate parents MAY be absent. Every parent that does exist still applies.

A child:

- MAY add requirements;
- MAY make an inherited requirement stricter;
- MUST NOT silently weaken or contradict an inherited requirement; and
- MUST declare a justified exception when its behavior cannot satisfy an
  inherited requirement.

Updating a parent immediately updates the effective requirements of every
descendant.

## 4. Document structure

A specification SHOULD use the following sections when applicable:

```markdown
# Settings.Accounts

One-paragraph purpose and scope.

## Status

Implemented

## Requirements

- The account list MUST show every configured account.

## Verification

- Mixed-provider accounts appear together.

## Exceptions

### Visible secrets are never restored

Source: `Settings`

Exception: A stored password is not repopulated into the visible field.

Rationale: The interface must not reveal a protected credential.

## Related specifications

- `Onboarding.AccountSetup`
- `Search.IndexManagement`
```

Only requirements expressed with normative terms are inherited. Purpose text,
examples, rationale, status, and verification notes remain local unless another
document explicitly references them.

## 5. Status

When present, `Status` MUST contain one of:

- `Required`: intended product behavior that may not yet be complete;
- `Implemented`: available behavior expected to remain supported;
- `Deferred`: accepted direction without a current delivery commitment;
- `Deprecated`: present behavior planned for retirement; or
- `Retired`: intentionally removed behavior retained as product history.

Removing implementation and its tests does not change a specification's status.
Retirement requires an explicit specification change and rationale.

## 6. Requirements

Requirements SHOULD describe observable product behavior and durable product
constraints rather than source files, types, or implementation techniques.

Use one requirement per list item when practical. This improves review,
referencing, future validation, and agent comprehension.

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

Related specifications identify non-parent product contracts that a maintainer
or agent should inspect before changing behavior. Each reference MUST resolve to
an existing canonical name.

Related references do not create inheritance.

## 9. Tests and implementation

Tests SHOULD reference the most specific applicable canonical name using a
language-appropriate comment or annotation:

```swift
// Product-Spec: Settings.Accounts.Removal
```

```python
# Product-Spec: Settings.Accounts.Removal
```

Repositories MAY require every `Implemented` specification to have referenced
verification coverage. A test can reference more than one specification when it
provides meaningful evidence for each.

Source paths and test filenames SHOULD NOT be maintained in the specification as
the primary mapping because they change more often than product intent.

## 10. Agent resolution

Before changing a product behavior, an agent SHOULD:

1. identify the most specific affected specification;
2. resolve and read all existing namespace parents;
3. read the target specification;
4. read its related specifications;
5. identify the effective inherited requirements;
6. preserve or deliberately update verification coverage; and
7. record any approved retirement or exception in the specification.

Agents MUST NOT treat missing implementation or missing tests as evidence that a
documented capability is obsolete.

## 11. Conformance

A conforming Feature Spec collection MUST satisfy the filename, H1, namespace,
parent-reference, related-reference, and exception rules in this document.

A project MAY adopt stricter conventions without changing the meaning of the
base format.
