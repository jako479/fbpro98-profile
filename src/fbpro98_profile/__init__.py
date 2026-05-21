"""Library for parsing and editing a Front Page Sports Football Pro '98 coaching profile (.prf).

The write/update API is not yet exposed while the shape of mutation operations
is being designed.
"""

from fbpro98_profile.model import (
    DEFENSE_DISPLAY_CATEGORIES,
    OFFENSE_DISPLAY_CATEGORIES,
    CategoryWeights,
    Down,
    FieldPosition,
    MinutesRemaining,
    PatMinutesRemaining,
    PatPointSpread,
    PatSituation,
    PointSpread,
    Profile,
    ProfileType,
    Situation,
    SubstitutionPair,
    SubstitutionSettings,
    YardsToGo,
)
from fbpro98_profile.reader import (
    InvalidProfileError,
    UnsupportedProfileError,
    parse_profile,
    read_profile,
)

__all__ = [
    "DEFENSE_DISPLAY_CATEGORIES",
    "OFFENSE_DISPLAY_CATEGORIES",
    "CategoryWeights",
    "Down",
    "FieldPosition",
    "InvalidProfileError",
    "MinutesRemaining",
    "PatMinutesRemaining",
    "PatPointSpread",
    "PatSituation",
    "PointSpread",
    "Profile",
    "ProfileType",
    "Situation",
    "SubstitutionPair",
    "SubstitutionSettings",
    "UnsupportedProfileError",
    "YardsToGo",
    "parse_profile",
    "read_profile",
]
