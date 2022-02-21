import functools
import random
from dataclasses import dataclass
from enum import Enum
from typing import Tuple


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
    @staticmethod
    def shuffle(cards: Tuple[Card]) -> Tuple[Card]:
        return tuple(random.sample(cards, k=len(cards)))

    @classmethod
    def deal(
        cls, shuffle: bool = True
    ) -> Tuple[Tuple[Card, ...], Tuple[Card, ...], Tuple[Card, ...], Tuple[Card, ...]]:
        cards = cls.generate_cards()
        if shuffle:
            cards = cls.shuffle(cards)
        return cards[:12], cards[12:24], cards[24:36], cards[36:]

    @staticmethod
    def generate_cards() -> Tuple[Card, ...]:
        return tuple(Card(suit=suit, rank=rank) for suit in Suit for rank in Rank) * 2
