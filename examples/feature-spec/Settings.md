# Settings

Defines requirements shared by every product setting.

## Status

Implemented

## Requirements

- Settings MUST use language that describes user outcomes.
- Committed changes MUST persist across application relaunch.
- Changing one setting MUST NOT reset an unrelated setting.
- Every setting MUST be keyboard accessible.
- Validation failures MUST preserve the last valid configuration.
- Validation failures MUST identify a recovery action.

## Verification

- Navigation and controls work using only a keyboard.
- Persisted changes survive a relaunch.
- Invalid changes do not replace valid configuration.
