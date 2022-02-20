import functools
import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


@functools.total_ordering
class Suit(Enum):
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"

    def __lt__(self, other: "Suit") -> bool:
        order = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
        return order.index(self) < order.index(other)


@functools.total_ordering
class Rank(Enum):
    NINE = "Nine"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"
    TEN = "Ten"
    ACE = "Ace"

    def __lt__(self, other: "Rank") -> bool:
        order = [Rank.NINE, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.TEN, Rank.ACE]
        return order.index(self) < order.index(other)


@functools.total_ordering
@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    def __lt__(self, other: "Card") -> bool:
        if self.suit == other.suit:
            return self.rank < other.rank
        return self.suit < other.suit


class CardDeck:
    cards: List[Card]

    def __init__(self) -> None:
        self.cards = [Card(suit=suit, rank=rank) for suit in Suit for rank in Rank] * 2

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self) -> Tuple[List[Card], ...]:
        return self.cards[:12], self.cards[12:24], self.cards[24:36], self.cards[36:]
