# fbpro98-profile — Status

**Status: Tests Complete**

Library for reading and writing Front Page Sports Football Pro '98 coaching profile (`.prf`) files via a typed in-memory model.

## Implemented

- Reading — parse a saved-layout `.prf` from disk or buffer into a frozen, fully typed `Profile`.
- Writing — serialize a `Profile` back to `.prf` bytes; supports both updating an existing file (open, modify, save to same path) and writing a brand-new profile constructed in code.
- Typed model — immutable `Profile`, `Situation`, `PatSituation`, `CategoryWeights`, `SubstitutionSettings`/`SubstitutionPair`, and profile-type / game-state enums.
- Situation-number ↔ game-state conversion (1-based), with the invalid combo (inside the DEF 5 with ≥6 yards to go) rejected.
- Structural validation — block magics, sizes, redundant F95/I95 field agreement, field-range checks, trailer length and bytes, file-size parity. PAT records enforce a plain `weight1 ∈ [0, 10]` (no Stop-Clock bit on the PAT side).
- Unsupported-variant detection — stock-layout profiles and profiles saved with embedded game plans are rejected as `UnsupportedProfileError`.

## Not supported

- Reading or writing the stock on-disk layout used by game-shipped profiles.
- Reading or writing profiles with embedded game plans.
