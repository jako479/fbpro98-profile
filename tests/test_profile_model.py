from __future__ import annotations

from dataclasses import replace

import pytest

from fbpro98_profile import (
    CategoryWeights,
    Profile,
    ProfileType,
    SubstitutionPair,
    SubstitutionSettings,
)


def _default_weights(*, play_category: int = 0x00, stop_clock: bool = False, weight1: int = 0) -> CategoryWeights:
    return CategoryWeights(
        play_category1=play_category,
        weight1=weight1,
        stop_clock=stop_clock,
        play_category2=play_category,
        weight2=0,
        play_category3=play_category,
        weight3=0,
    )


def _empty_weights(count: int) -> tuple[CategoryWeights, ...]:
    return tuple(_default_weights() for _ in range(count))


def _make_profile(*, profile_type: ProfileType = ProfileType.OFFENSE, **overrides) -> Profile:
    base = Profile(
        profile_type=profile_type,
        substitutions=SubstitutionSettings.default(),
        category_weights=_empty_weights(Profile.NUMBER_SITUATIONS),
        pat_category_weights=_empty_weights(Profile.NUMBER_PAT_SITUATIONS),
        field_goal_range=35,
        use_audibles=False,
    )
    return replace(base, **overrides)


# ---------- SubstitutionPair ----------


def test_substitution_pair_accepts_valid_values() -> None:
    pair = SubstitutionPair(out_percent=80, in_percent=90)
    assert pair.out_percent == 80
    assert pair.in_percent == 90


def test_substitution_pair_rejects_out_above_in() -> None:
    with pytest.raises(ValueError, match="must be <="):
        SubstitutionPair(out_percent=90, in_percent=80)


def test_substitution_pair_rejects_out_below_zero() -> None:
    with pytest.raises(ValueError, match="out_percent must be in"):
        SubstitutionPair(out_percent=-1, in_percent=50)


def test_substitution_pair_rejects_in_above_100() -> None:
    with pytest.raises(ValueError, match="in_percent must be in"):
        SubstitutionPair(out_percent=50, in_percent=101)


def test_substitution_pair_accepts_equal_values() -> None:
    pair = SubstitutionPair(out_percent=50, in_percent=50)
    assert pair.out_percent == pair.in_percent


# ---------- SubstitutionSettings ----------


def test_substitution_settings_default_uses_80_90() -> None:
    settings = SubstitutionSettings.default()
    for group in (
        settings.offensive_linemen,
        settings.quarterbacks,
        settings.running_backs,
        settings.receivers,
        settings.defensive_linemen,
        settings.linebackers,
        settings.defensive_backs,
        settings.kickers,
    ):
        assert group.out_percent == 80
        assert group.in_percent == 90


# ---------- CategoryWeights ----------


def test_category_weights_accepts_valid_values() -> None:
    weights = CategoryWeights(
        play_category1=0x07,
        weight1=10,
        stop_clock=True,
        play_category2=0x10,
        weight2=5,
        play_category3=0x00,
        weight3=0,
    )
    assert weights.weight1 == 10
    assert weights.stop_clock is True


def test_category_weights_rejects_play_category_above_max() -> None:
    with pytest.raises(ValueError, match="play_category1"):
        CategoryWeights(
            play_category1=0x1B,
            weight1=0,
            stop_clock=False,
            play_category2=0x00,
            weight2=0,
            play_category3=0x00,
            weight3=0,
        )


def test_category_weights_rejects_weight_above_10() -> None:
    with pytest.raises(ValueError, match="weight2"):
        CategoryWeights(
            play_category1=0x00,
            weight1=0,
            stop_clock=False,
            play_category2=0x00,
            weight2=11,
            play_category3=0x00,
            weight3=0,
        )


def test_category_weights_rejects_negative_weight() -> None:
    with pytest.raises(ValueError, match="weight3"):
        CategoryWeights(
            play_category1=0x00,
            weight1=0,
            stop_clock=False,
            play_category2=0x00,
            weight2=0,
            play_category3=0x00,
            weight3=-1,
        )


# ---------- Profile invariants ----------


def test_profile_accepts_valid_offense_construction() -> None:
    profile = _make_profile()
    assert profile.is_offense is True
    assert profile.is_defense is False


def test_profile_accepts_valid_defense_construction() -> None:
    profile = _make_profile(profile_type=ProfileType.DEFENSE)
    assert profile.is_defense is True
    assert profile.is_offense is False


def test_profile_category_weights_wrong_length_raises() -> None:
    with pytest.raises(ValueError, match="category_weights must have exactly"):
        _make_profile(category_weights=_empty_weights(10))


def test_profile_pat_category_weights_wrong_length_raises() -> None:
    with pytest.raises(ValueError, match="pat_category_weights must have exactly"):
        _make_profile(pat_category_weights=_empty_weights(5))


@pytest.mark.parametrize("value", [0, 4, 51, 100])
def test_profile_field_goal_range_out_of_bounds_raises(value: int) -> None:
    with pytest.raises(ValueError, match="field_goal_range"):
        _make_profile(field_goal_range=value)


@pytest.mark.parametrize("value", [5, 25, 50])
def test_profile_field_goal_range_at_bounds_accepted(value: int) -> None:
    profile = _make_profile(field_goal_range=value)
    assert profile.field_goal_range == value


# ---------- stop_clock_situations property ----------


def test_stop_clock_situations_empty_when_no_flags_set() -> None:
    profile = _make_profile()
    assert profile.stop_clock_situations == ()


def test_stop_clock_situations_returns_only_flagged_entries() -> None:
    base = list(_empty_weights(Profile.NUMBER_SITUATIONS))
    base[5] = _default_weights(stop_clock=True, weight1=3)
    base[100] = _default_weights(stop_clock=True, weight1=7)
    base[2519] = _default_weights(stop_clock=True, weight1=10)

    profile = _make_profile(category_weights=tuple(base))
    indices = [index for index, _ in profile.stop_clock_situations]
    assert indices == [5, 100, 2519]


def test_stop_clock_situations_yields_index_situation_pairs() -> None:
    base = list(_empty_weights(Profile.NUMBER_SITUATIONS))
    base[42] = _default_weights(stop_clock=True, weight1=4)
    profile = _make_profile(category_weights=tuple(base))
    pairs = profile.stop_clock_situations
    assert len(pairs) == 1
    index, situation = pairs[0]
    assert index == 42
    assert situation.stop_clock is True
    assert situation.weight1 == 4


def test_stop_clock_situations_excludes_pat_situations() -> None:
    """The property only inspects `category_weights`, not `pat_category_weights`."""
    pats = list(_empty_weights(Profile.NUMBER_PAT_SITUATIONS))
    pats[0] = _default_weights(stop_clock=True, weight1=4)
    profile = _make_profile(pat_category_weights=tuple(pats))
    assert profile.stop_clock_situations == ()
