# Versioning Keystone

Keystone uses [Semantic Versioning](https://semver.org/) for published versions
of the framework contract.

The current version is **0.2.0**. Versions below `1.0.0` are drafts. They are
usable, but the contract can still change as the format is tested and refined.

- A patch release, such as `0.1.1`, fixes errors or clarifies the contract
  without intending to change its meaning.
- A minor release, such as `0.2.0`, adds to or changes the contract. Projects
  may need to update their feature specifications or tooling.
- `1.0.0` will mark the first stable contract. After that point, breaking
  contract changes require a new major version.

The root [`VERSION`](VERSION) file records the current version. The version in
`README.md`, `SPEC.md`, the standalone `agent-prompt.md` contract, and the
website must match it. Each published version should also have a matching Git
tag and GitHub release, such as `v0.2.0`, so projects can link to the exact
contract they adopted.

Run `python3 -m unittest discover -s tests` after a version change. The version
tests catch public surfaces that were not updated.
