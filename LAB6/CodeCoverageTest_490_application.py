
import pytest

from recycling_rewards import (
    reward_points,
    collection_accepted,
    slot_status,
)


# Reward points: normal cases and validation
def test_paper_below_minimum():
    assert reward_points("paper", 3, False) == 0


def test_paper_above_minimum():
    assert reward_points("paper", 7, False) == 12


def test_plastic_with_bonus():
    assert reward_points("plastic", 3, True) == 6


def test_metal_reward():
    assert reward_points("metal", 5, False) == 36


def test_reward_unknown_material():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)


def test_reward_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)


def test_metal_bonus_does_not_reduce_minimum():
    assert reward_points("metal", 2, True) == 0


def test_large_weight_reward_rate():
    assert reward_points("paper", 30, False) == 250


# Collection acceptance
def test_collection_accepted_normal():
    assert collection_accepted(20, 2, False) is True


def test_hazardous_collection_within_limit():
    assert collection_accepted(5, 10, True) is True


def test_hazardous_collection_over_limit():
    assert collection_accepted(6, 1, True) is False


def test_collection_over_weight_limit():
    assert collection_accepted(51, 2, False) is False


def test_collection_too_many_bags():
    assert collection_accepted(20, 4, False) is False


# Pickup slot status
def test_morning_slot_open():
    assert slot_status(20, True, False) == "open"


def test_evening_slot_open():
    assert slot_status(10, False, False) == "open"


def test_morning_slot_late():
    assert slot_status(10, True, False) == "late"


def test_evening_slot_missed():
   assert slot_status(-6, False, False) == "missed"


def test_holiday_slot_open():
    assert slot_status(35, True, True) == "open"


def test_holiday_slot_late():
    assert slot_status(20, True, True) == "late"


def test_holiday_slot_missed():
    assert slot_status(-6, False, False) == "missed"
