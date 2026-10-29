
import pytest

from recycling_rewards import (
    reward_points,
    collection_accepted,
    slot_status,
)


# reward_points: validation branches
def test_unknown_material():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)


# Minimum weight and bonus branches
def test_weight_at_minimum():
    assert reward_points("paper", 5, False) == 0


def test_weight_above_minimum():
    assert reward_points("paper", 6, False) == 6


def test_bonus_for_non_metal():
    assert reward_points("paper", 5, True) == 6


def test_bonus_reduces_minimum():
    assert reward_points("plastic", 2, True) == 0


def test_metal_bonus_does_not_reduce_minimum():
    assert reward_points("metal", 3, True) == 12


# Reward rate branches
def test_metal_rate():
    assert reward_points("metal", 5, False) == 36


def test_non_metal_rate():
    assert reward_points("paper", 10, False) == 30


def test_extra_weight_at_threshold():
    assert reward_points("paper", 25, False) == 120


def test_extra_weight_above_threshold():
    assert reward_points("paper", 26, False) == 210


def test_metal_extra_weight_above_threshold():
    assert reward_points("metal", 23, False) == 378


# Collection acceptance branches
def test_hazardous_collection_accepted():
    assert collection_accepted(5, 5, True) is True


def test_hazardous_collection_rejected():
    assert collection_accepted(6, 1, True) is False


def test_normal_collection_over_weight_limit():
    assert collection_accepted(51, 1, False) is False


def test_normal_collection_too_many_bags():
    assert collection_accepted(20, 4, False) is False


def test_normal_collection_accepted():
    assert collection_accepted(50, 3, False) is True


# Slot status branches
def test_morning_open():
    assert slot_status(20, True, False) == "open"


def test_evening_open():
    assert slot_status(10, False, False) == "open"


def test_holiday_cutoff():
    assert slot_status(35, True, True) == "open"


def test_morning_late():
    assert slot_status(10, True, False) == "late"


def test_evening_late():
    assert slot_status(0, False, False) == "late"


def test_holiday_late():
    assert slot_status(20, True, True) == "late"


def test_morning_missed():
    assert slot_status(4, True, False) == "missed"


def test_evening_missed():
    assert slot_status(-6, False, False) == "missed"


def test_holiday_missed():
    assert slot_status(4, True, True) == "missed"
