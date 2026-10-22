"""Logica dei tiri PbtA, indipendente da Discord."""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum


class Mode(str, Enum):
    NORMAL = "normale"
    ADVANTAGE = "vantaggio"
    DISADVANTAGE = "svantaggio"


class Outcome(str, Enum):
    STRONG_HIT = "Successo pieno"
    WEAK_HIT = "Successo parziale"
    MISS = "Fallimento"


MIN_MODIFIER = -10
MAX_MODIFIER = 10


@dataclass(frozen=True)
class RollResult:
    dice: tuple[int, ...]
    kept: tuple[int, ...]
    modifier: int
    mode: Mode

    @property
    def total(self) -> int:
        return sum(self.kept) + self.modifier

    @property
    def outcome(self) -> Outcome:
        return outcome_for(self.total)


def outcome_for(total: int) -> Outcome:
    if total >= 10:
        return Outcome.STRONG_HIT
    if total >= 7:
        return Outcome.WEAK_HIT
    return Outcome.MISS


def roll(modifier: int = 0, mode: Mode = Mode.NORMAL, rng: random.Random | None = None) -> RollResult:
    """Tira 2d6 + modificatore; con vantaggio/svantaggio tira 3d6 e tiene i due migliori/peggiori."""
    if not MIN_MODIFIER <= modifier <= MAX_MODIFIER:
        raise ValueError(f"Il modificatore deve essere tra {MIN_MODIFIER} e {MAX_MODIFIER}")
    rng = rng or random.SystemRandom()
    count = 2 if mode is Mode.NORMAL else 3
    dice = tuple(rng.randint(1, 6) for _ in range(count))
    ordered = sorted(dice, reverse=True)
    if mode is Mode.DISADVANTAGE:
        kept = tuple(ordered[-2:])
    else:
        kept = tuple(ordered[:2])
    return RollResult(dice=dice, kept=kept, modifier=modifier, mode=mode)
