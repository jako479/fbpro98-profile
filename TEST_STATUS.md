# fbpro98-profile — Test Status

**Test Status: Tests Complete**

## Covered by automated tests

- Model invariants — `SubstitutionPair`, `SubstitutionSettings`, `Situation`, and `Profile` construction and validation rules on synthesized instances.
- `stop_clock_situations` property — index/situation pairing, filtering of unflagged entries, and exclusion of PAT situations.
- Real-fixture parsing — the four game-produced `DEN-*.prf` files pinned against expected metadata (profile type, field-goal range, substitutions, situations, PAT situations, stop-clock counts and indices).
- Public API surface — `read_profile` / `parse_profile` equivalence and the error-class hierarchy.
- Structural error paths — bad block magics and sizes, out-of-range fields, F95/I95 mismatches, invalid trailers, file-size parity, and missing files.
- Unsupported-variant detection — stock-layout files and profiles with embedded game plans.

## Needs tests

- Nothing outstanding for the current scope.
