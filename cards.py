import functools
from dataclasses import dataclass
from enum import Enum, unique, auto, IntEnum
from typing import List


@functools.total_ordering
@unique
class Suit(Enum):
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"

    def __lt__(self, other):
        order = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        return order.index(self) < order.index(other)


@functools.total_ordering
@unique
class Rank(Enum):
    NINE = "Nine"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"
    TEN = "Ten"
    ACE = "Ace"

    def __lt__(self, other):
        order = [Rank.NINE, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.TEN, Rank.ACE]
        return order.index(self) < order.index(other)


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank


class CardDeck:
    cards: List[Card]

    def __init__(self):
        self.cards = [Card(suit=suit, rank=rank) for suit in Suit for rank in Rank] * 2
