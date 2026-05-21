# fbpro98-profile — Status

**Status: In Progress**

Library for reading and writing Front Page Sports Football Pro '98 coaching profile (`.prf`) files via a typed in-memory model.

## Implemented

- Parsing — `read_profile(path)` and `parse_profile(buffer)` decode a saved-layout `.prf` into a frozen, fully typed `Profile`.
- Typed model — immutable `Profile`, `Situation`, `PatSituation`, `CategoryWeights`, `SubstitutionSettings`, `SubstitutionPair`, and the `ProfileType` enum.
- Situation bucket enums — `MinutesRemaining`, `Down`, `YardsToGo`, `FieldPosition`, `PointSpread` for regular situations; `PatMinutesRemaining` and `PatPointSpread` for PAT.
- Situation index decoding — `Situation` and `PatSituation` carry `from_index` / `dimensions_from_index` / `index_from_dimensions` helpers that map between the file's situation number and the bucket-dimension tuple, with the structural gap (no `INSIDE_DEF_5` × `>=6` yards-to-go) enforced.
- Profile data exposed — profile type, field-goal range, use-audibles, eight substitution position groups, 2520 `Situation` records (bucket dimensions + `stop_clock` + `CategoryWeights`), 60 `PatSituation` records (bucket dimensions + `CategoryWeights`), and `stop_clock_situations`.
- Structural validation — block magics and sizes, agreement of redundant F95/I95 fields, field-range checks, trailer length and bytes, and file-size parity, with malformed bytes raising `InvalidProfileError`. PAT records enforce `weight1 ∈ [0, 10]` (no Stop-Clock bit on PAT side).
- Unsupported-variant detection — stock-layout profiles and profiles saved with embedded game plans are rejected cleanly with `UnsupportedProfileError`.

## Remaining

- Write/update API — bytes-out / mutation operations are not yet exposed.
- Support for the stock on-disk layout used by game-shipped profiles.
- Support for profiles saved with embedded game plans.
