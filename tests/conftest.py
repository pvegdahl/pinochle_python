from typing import Tuple

import pytest

from cards import Card, Suit, Rank


@pytest.fixture(scope="session")
def all_clubs() -> Tuple[Card, ...]:
    return tuple(Card(rank, Suit.CLUBS) for rank in Rank) * 2


@pytest.fixture(scope="session")
def all_diamonds() -> Tuple[Card, ...]:
    return tuple(Card(rank, Suit.DIAMONDS) for rank in Rank) * 2


@pytest.fixture(scope="session")
def all_hearts() -> Tuple[Card, ...]:
    return tuple(Card(rank, Suit.HEARTS) for rank in Rank) * 2


@pytest.fixture(scope="session")
def all_spades() -> Tuple[Card, ...]:
    return tuple(Card(rank, Suit.SPADES) for rank in Rank) * 2


@pytest.fixture(scope="session")
def sorted_hands(all_clubs, all_diamonds, all_hearts, all_spades) -> Tuple[Tuple[Card, ...], ...]:
    return all_clubs, all_diamonds, all_hearts, all_spades
