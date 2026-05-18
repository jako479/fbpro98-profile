# fbpro98-profile — Status

**Status: In Progress**

Read-only library for parsing Front Page Sports Football Pro '98 coaching profile (`.prf`) files into a typed in-memory model.

## Implemented

- Parsing — `read_profile(path)` and `parse_profile(buffer)` decode a saved-layout `.prf` into a frozen, fully typed `Profile`.
- Typed model — immutable `Profile`, `Situation`, `SubstitutionSettings`, `SubstitutionPair`, and the `ProfileType` enum.
- Profile data exposed — profile type, field-goal range, use-audibles, eight substitution position groups, 2520 situations, 60 PAT situations, and `stop_clock_situations`.
- Structural validation — block magics and sizes, agreement of redundant F95/I95 fields, field-range checks, trailer length and bytes, and file-size parity, with malformed bytes raising `InvalidProfileError`.
- Unsupported-variant detection — stock-layout profiles and profiles saved with embedded game plans are rejected cleanly with `UnsupportedProfileError`.

## Remaining

- Write/update API — bytes-out / mutation operations are intentionally not yet exposed.
- Support for the stock on-disk layout used by game-shipped profiles.
- Support for profiles saved with embedded game plans.
