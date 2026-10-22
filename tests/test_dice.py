import random

import pytest

from pbotta.dice import Mode, Outcome, outcome_for, roll


@pytest.mark.parametrize(
    "total,expected",
    [(-5, Outcome.MISS), (6, Outcome.MISS), (7, Outcome.WEAK_HIT), (9, Outcome.WEAK_HIT),
     (10, Outcome.STRONG_HIT), (15, Outcome.STRONG_HIT)],
)
def test_outcome_thresholds(total, expected):
    assert outcome_for(total) is expected


class FixedRng(random.Random):
    def __init__(self, values):
        super().__init__()
        self._values = iter(values)

    def randint(self, a, b):
        return next(self._values)


def test_normal_roll_uses_two_dice():
    result = roll(2, rng=FixedRng([3, 4]))
    assert result.dice == (3, 4)
    assert result.total == 9
    assert result.outcome is Outcome.WEAK_HIT


def test_advantage_keeps_highest_two():
    result = roll(0, Mode.ADVANTAGE, FixedRng([1, 6, 4]))
    assert sorted(result.kept) == [4, 6]
    assert result.total == 10


def test_disadvantage_keeps_lowest_two():
    result = roll(1, Mode.DISADVANTAGE, FixedRng([1, 6, 4]))
    assert sorted(result.kept) == [1, 4]
    assert result.total == 6


@pytest.mark.parametrize("mode", list(Mode))
def test_random_rolls_stay_in_range(mode):
    for _ in range(500):
        result = roll(0, mode)
        assert all(1 <= d <= 6 for d in result.dice)
        assert 2 <= result.total <= 12


def test_modifier_out_of_range():
    with pytest.raises(ValueError):
        roll(11)
