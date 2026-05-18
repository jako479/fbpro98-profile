# fbpro98-profile — Status

Working **read-only** library for the Front Page Sports Football Pro '98 `.prf`
coaching-profile binary format. The reader is complete; the writer is deferred.

## Working

- **Parsing** — `read_profile(path)` and `parse_profile(buffer)` decode a
  saved-layout `.prf` into a frozen, fully typed `Profile`.
- **Model** — immutable `Profile`, `Situation`, `SubstitutionSettings`,
  `SubstitutionPair`, and the `ProfileType` enum.
- **Profile data exposed:**
  - `profile_type` — OFFENSE / DEFENSE
  - `field_goal_range` — 5–50
  - `use_audibles`
  - `substitutions` — 8 position groups
  - `situations` — 2520 `Situation`
  - `pat_situations` — 60 `Situation`
  - `stop_clock_situations` — situations with the Stop-Clock bit set
- **Structural validation** — block magics and sizes, redundant F95/I95 fields
  agreeing, field ranges, trailer length and bytes, and file-size parity;
  malformed bytes raise `InvalidProfileError`.
- **Unsupported-variant detection** — stock-layout profiles and profiles saved
  with embedded game plans are rejected cleanly with `UnsupportedProfileError`.

## Tested

81 tests pass:

- `tests/test_profile_model.py` — model invariants on synthesized instances.
- `tests/test_profile_reader.py` — real, game-produced fixture `.prf` files
  pinned against expected metadata, plus structural-error paths.
