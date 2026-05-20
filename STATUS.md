# fbpro98-profile — Status

**Status: In Progress**

Library for reading and writing Front Page Sports Football Pro '98 coaching profile (`.prf`) files via a typed in-memory model.

## Implemented

- Parsing — `read_profile(path)` and `parse_profile(buffer)` decode a saved-layout `.prf` into a frozen, fully typed `Profile`.
- Typed model — immutable `Profile`, `CategoryWeights`, `SubstitutionSettings`, `SubstitutionPair`, and the `ProfileType` enum.
- Profile data exposed — profile type, field-goal range, use-audibles, eight substitution position groups, 2520 category-weights records (one per regular situation), 60 PAT category-weights records, and `stop_clock_situations`.
- Structural validation — block magics and sizes, agreement of redundant F95/I95 fields, field-range checks, trailer length and bytes, and file-size parity, with malformed bytes raising `InvalidProfileError`.
- Unsupported-variant detection — stock-layout profiles and profiles saved with embedded game plans are rejected cleanly with `UnsupportedProfileError`.

## Remaining

- Write/update API — bytes-out / mutation operations are not yet exposed.
- Support for the stock on-disk layout used by game-shipped profiles.
- Support for profiles saved with embedded game plans.
