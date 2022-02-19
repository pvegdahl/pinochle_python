from dataclasses import dataclass
from enum import Enum, unique, auto, IntEnum


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
