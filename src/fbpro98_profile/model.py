"""In-memory data model for FbPro98 .prf coaching profile files.

Defines the immutable types that the reader produces and the writer consumes:
ProfileType, SubstitutionPair, SubstitutionSettings, Situation, and the
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
    """One position group's `out` / `in` substitution thresholds (each 0-100, out <= in)."""

    out_percent: int
    in_percent: int

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
    quarterbacks: SubstitutionPair
    running_backs: SubstitutionPair
    receivers: SubstitutionPair
    defensive_linemen: SubstitutionPair
    linebackers: SubstitutionPair
    defensive_backs: SubstitutionPair
    kickers: SubstitutionPair

    @classmethod
    def default(cls) -> SubstitutionSettings:
        """Return a SubstitutionSettings with every pair at the game's default 80/90."""
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
class Situation:
    """One situation: three weighted play-category picks plus the Stop-Clock flag.

    `weightN` values are in [0, 10]. Only `weight1` carries the Stop-Clock bit
    (bit 7) at the byte level; in this model it is broken out into the separate
    `stop_clock` field. `play_categoryN` values are in [0x00, 0x1A] regardless
    of the parent Profile's side; see `OFFENSE_DISPLAY_CATEGORIES` /
    `DEFENSE_DISPLAY_CATEGORIES` for which codes the game UI labels per side.
    """

    play_category1: int
    weight1: int
    stop_clock: bool
    play_category2: int
    weight2: int
    play_category3: int
    weight3: int

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
    """Full in-memory representation of a `.prf` coaching profile file."""

    NUMBER_SITUATIONS: ClassVar[int] = 2520
    NUMBER_PAT_SITUATIONS: ClassVar[int] = 60
    FIELD_GOAL_RANGE_MIN: ClassVar[int] = 5
    FIELD_GOAL_RANGE_MAX: ClassVar[int] = 50

    profile_type: ProfileType
    substitutions: SubstitutionSettings
    situations: tuple[Situation, ...]
    pat_situations: tuple[Situation, ...]
    field_goal_range: int
    use_audibles: bool

    def __post_init__(self) -> None:
        if len(self.situations) != self.NUMBER_SITUATIONS:
            raise ValueError(
                f"situations must have exactly {self.NUMBER_SITUATIONS} entries, got {len(self.situations)}"
            )
        if len(self.pat_situations) != self.NUMBER_PAT_SITUATIONS:
            raise ValueError(
                f"pat_situations must have exactly {self.NUMBER_PAT_SITUATIONS} entries, got {len(self.pat_situations)}"
            )
        if not self.FIELD_GOAL_RANGE_MIN <= self.field_goal_range <= self.FIELD_GOAL_RANGE_MAX:
            raise ValueError(
                f"field_goal_range must be in [{self.FIELD_GOAL_RANGE_MIN}, {self.FIELD_GOAL_RANGE_MAX}], "
                f"got {self.field_goal_range}"
            )

    @property
    def is_offense(self) -> bool:
        return self.profile_type == ProfileType.OFFENSE

    @property
    def is_defense(self) -> bool:
        return self.profile_type == ProfileType.DEFENSE

    @property
    def stop_clock_situations(self) -> tuple[tuple[int, Situation], ...]:
        """Return `(index, Situation)` pairs for every situation with the Stop-Clock bit set.

        Indexes refer to positions within `self.situations` (the 2520 game-state
        situations). PAT situations are not included.
        """
        return tuple((index, situation) for index, situation in enumerate(self.situations) if situation.stop_clock)
