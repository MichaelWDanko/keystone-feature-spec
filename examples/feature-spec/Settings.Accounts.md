# Settings.Accounts

Defines requirements for viewing and managing configured accounts.

## Status

Implemented

## Requirements

- Every configured account MUST appear exactly once.
- Each account MUST communicate its provider and usability state.
- Users MUST be able to add, edit, validate, recover, and remove accounts.
- Credentials MUST use protected platform credential storage.
- Removing one account MUST NOT modify another account.
- Account status MUST NOT rely on color alone.

## Verification

- Accounts from multiple providers can appear together.
- Validation failure does not overwrite a valid credential.
- Account removal clears only account-scoped data.

## Exceptions

### Protected credentials are not repopulated

Source: `Settings`

Exception: A stored password is not restored to the visible password field.

Rationale: The setting remains committed, but the interface must not reveal a
protected credential.

## Related specifications

- `Search.IndexManagement`
