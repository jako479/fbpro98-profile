"""In-memory data model for FbPro98 .prf coaching profile files.

Defines the immutable types that the reader produces and the writer consumes:
ProfileType, SubstitutionPair, SubstitutionSettings, CategoryWeights, and the
top-level Profile dataclass.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import ClassVar


class ProfileType(IntEnum):
    """Whether a profile is for defense (0) or offense (1). Encoded in I95 data."""

    DEFENSE = 0
    OFFENSE = 1


@dataclass(frozen=True, slots=True)
class SubstitutionPair:
    """One position group's `out` / `in` substitution thresholds (each 0-100, out <= in).

    See specs/prf.md section 2.2 for the on-disk layout.
    """

    out_percent: int
    """Fatigue threshold (0-100) at which a starter is pulled for a backup."""

    in_percent: int
    """Recovery threshold (0-100) at which the starter returns. Must be >= out_percent."""

    def __post_init__(self) -> None:
        if not 0 <= self.out_percent <= 100:
            raise ValueError(f"out_percent must be in [0, 100], got {self.out_percent}")
        if not 0 <= self.in_percent <= 100:
            raise ValueError(f"in_percent must be in [0, 100], got {self.in_percent}")
        if self.out_percent > self.in_percent:
            raise ValueError(f"out_percent ({self.out_percent}) must be <= in_percent ({self.in_percent})")


@dataclass(frozen=True, slots=True)
class SubstitutionSettings:
    """All eight position groups' substitution thresholds.

    All eight pairs are physically present in both offense and defense profiles.
    The game UI exposes only the five offensive groups (OL, QB, RB, WR, K) when
    editing an offense profile and the three defensive groups (DL, LB, DB) when
    editing a defense profile; the rest hold the game's `80/90` default.
    """

    offensive_linemen: SubstitutionPair
    """OL substitution thresholds. Editable in the offense profile UI."""

    quarterbacks: SubstitutionPair
    """QB substitution thresholds. Editable in the offense profile UI."""

    running_backs: SubstitutionPair
    """RB substitution thresholds. Editable in the offense profile UI."""

    receivers: SubstitutionPair
    """WR substitution thresholds. Editable in the offense profile UI."""

    defensive_linemen: SubstitutionPair
    """DL substitution thresholds. Editable in the defense profile UI."""

    linebackers: SubstitutionPair
    """LB substitution thresholds. Editable in the defense profile UI."""

    defensive_backs: SubstitutionPair
    """DB substitution thresholds. Editable in the defense profile UI."""

    kickers: SubstitutionPair
    """K substitution thresholds. Editable in the offense profile UI."""

    @classmethod
    def default(cls) -> SubstitutionSettings:
        """Return a SubstitutionSettings with every pair at the game's default 80/90.

        Returns:
            A SubstitutionSettings whose every pair is `SubstitutionPair(80, 90)`.
        """
        default = SubstitutionPair(out_percent=80, in_percent=90)
        return cls(
            offensive_linemen=default,
            quarterbacks=default,
            running_backs=default,
            receivers=default,
            defensive_linemen=default,
            linebackers=default,
            defensive_backs=default,
            kickers=default,
        )


# Display-name lookup sets per specs/prf.md section 2.3.2. These describe which
# play_category values the in-game UI labels under each side; they are NOT a
# wire-format constraint, so neither the model nor the reader rejects bytes
# from outside the side's set. Defense covers 0x00-0x15 (the directional pass
# codes 0x07-0x0F all collapse to PASS_LONG/MEDIUM/SHORT in the defense UI);
# 0x16-0x1A are unused on defense. Exposed for downstream consumers that
# want to surface "this code isn't user-facing for this profile type" hints.
OFFENSE_DISPLAY_CATEGORIES: frozenset[int] = frozenset(range(0x00, 0x1B))
DEFENSE_DISPLAY_CATEGORIES: frozenset[int] = frozenset(range(0x00, 0x16))


@dataclass(frozen=True, slots=True)
class CategoryWeights:
    """Play-calling rule for one situation: three weighted play-category picks plus the Stop-Clock flag.

    Each Profile holds one CategoryWeights record per game situation (indexed by
    the game's internal situation number). `weightN` values are in [0, 10]. Only
    `weight1` carries the Stop-Clock bit (bit 7) at the byte level; in this
    model it is broken out into the separate `stop_clock` field. `play_categoryN`
    values are in [0x00, 0x1A] regardless of the parent Profile's side; see
    `OFFENSE_DISPLAY_CATEGORIES` / `DEFENSE_DISPLAY_CATEGORIES` for which codes
    the game UI labels per side.
    """

    play_category1: int
    """Primary play category code (0x00-0x1A)."""

    weight1: int
    """Weight of the primary pick (0-10). The Stop-Clock bit (bit 7) that
    coexists in this byte on disk is broken out into `stop_clock`."""

    stop_clock: bool
    """Whether the Stop-Clock flag is set for this situation (bit 7 of the
    first weight byte on disk)."""

    play_category2: int
    """Secondary play category code (0x00-0x1A)."""

    weight2: int
    """Weight of the secondary pick (0-10)."""

    play_category3: int
    """Tertiary play category code (0x00-0x1A)."""

    weight3: int
    """Weight of the tertiary pick (0-10)."""

    def __post_init__(self) -> None:
        for label, value in (
            ("play_category1", self.play_category1),
            ("play_category2", self.play_category2),
            ("play_category3", self.play_category3),
        ):
            if not 0x00 <= value <= 0x1A:
                raise ValueError(f"{label} must be in [0x00, 0x1A], got 0x{value:02X}")
        for label, value in (
            ("weight1", self.weight1),
            ("weight2", self.weight2),
            ("weight3", self.weight3),
        ):
            if not 0 <= value <= 10:
                raise ValueError(f"{label} must be in [0, 10], got {value}")


@dataclass(frozen=True, slots=True)
class Profile:
    """Full in-memory representation of a `.prf` coaching profile file.

    See specs/prf.md for the on-disk binary format. Construction validates
    structural invariants (record counts and field-goal range) via
    __post_init__; ValueError is raised for any violation.
    """

    NUMBER_SITUATIONS: ClassVar[int] = 2520
    """Number of regular game-state situations."""

    NUMBER_PAT_SITUATIONS: ClassVar[int] = 60
    """Number of point-after-touchdown situations."""

    FIELD_GOAL_RANGE_MIN: ClassVar[int] = 5
    """Minimum allowed field-goal range (yards)."""

    FIELD_GOAL_RANGE_MAX: ClassVar[int] = 50
    """Maximum allowed field-goal range (yards)."""

    profile_type: ProfileType
    """Whether this profile is for offense or defense. Determines trailer length
    and file-size parity."""

    substitutions: SubstitutionSettings
    """The eight position groups' substitution thresholds."""

    category_weights: tuple[CategoryWeights, ...]
    """Play-calling rules indexed by the game's situation number; 2520 entries,
    one per regular game-state situation."""

    pat_category_weights: tuple[CategoryWeights, ...]
    """Play-calling rules indexed by the game's PAT situation number; 60 entries,
    one per point-after-touchdown situation."""

    field_goal_range: int
    """Field-goal attempt range in yards. Bounded by FIELD_GOAL_RANGE_MIN and
    FIELD_GOAL_RANGE_MAX."""

    use_audibles: bool
    """Whether the audibles feature is enabled."""

    def __post_init__(self) -> None:
        if len(self.category_weights) != self.NUMBER_SITUATIONS:
            raise ValueError(
                f"category_weights must have exactly {self.NUMBER_SITUATIONS} entries, got {len(self.category_weights)}"
            )
        if len(self.pat_category_weights) != self.NUMBER_PAT_SITUATIONS:
            raise ValueError(
                f"pat_category_weights must have exactly {self.NUMBER_PAT_SITUATIONS} entries, "
                f"got {len(self.pat_category_weights)}"
            )
        if not self.FIELD_GOAL_RANGE_MIN <= self.field_goal_range <= self.FIELD_GOAL_RANGE_MAX:
            raise ValueError(
                f"field_goal_range must be in [{self.FIELD_GOAL_RANGE_MIN}, {self.FIELD_GOAL_RANGE_MAX}], "
                f"got {self.field_goal_range}"
            )

    @property
    def is_offense(self) -> bool:
        """True if this profile is for offense."""
        return self.profile_type == ProfileType.OFFENSE

    @property
    def is_defense(self) -> bool:
        """True if this profile is for defense."""
        return self.profile_type == ProfileType.DEFENSE

    @property
    def stop_clock_situations(self) -> tuple[tuple[int, CategoryWeights], ...]:
        """Return `(situation_index, CategoryWeights)` pairs for every situation whose record has Stop-Clock set.

        Indexes refer to positions within `self.category_weights` (the 2520
        regular game-state situations). PAT situations are not included.

        Returns:
            Tuple of `(situation_index, CategoryWeights)` pairs for situations
            where `stop_clock` is True, in ascending index order.
        """
        return tuple((index, weights) for index, weights in enumerate(self.category_weights) if weights.stop_clock)
