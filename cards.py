from dataclasses import dataclass
from enum import Enum, unique, auto, IntEnum
from typing import List


@unique
class Suit(Enum):
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"


@unique
class Rank(IntEnum):
    NINE = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()
    TEN = auto()
    ACE = auto()


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank


class CardDeck:
    cards: List[Card]

    def __init__(self):
        self.cards = [Card(suit=suit, rank=rank) for suit in Suit for rank in Rank] * 2
