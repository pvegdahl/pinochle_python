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

    def __str__(self):
        return self.value


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

    def __str__(self):
        return self.value


@functools.total_ordering
@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    def __lt__(self, other: "Card") -> bool:
        """
        This sort function is used to sort cards in hand for players.  It is not intended to compare card values for
        calculating play outcomes.  It will lead to weird results for that.  To do that properly, you need a function
        that knows the trump suit.  See tricks.py:second_card_wins()
        """
        if self.suit == other.suit:
            return self.rank < other.rank
        return self.suit < other.suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class CardDeck:
    @staticmethod
    def _shuffle(cards: Tuple[Card]) -> Tuple[Card]:
        return tuple(random.sample(cards, k=len(cards)))

    @classmethod
    def deal(
        cls,
    ) -> Tuple[Tuple[Card, ...], Tuple[Card, ...], Tuple[Card, ...], Tuple[Card, ...]]:
        cards = cls._shuffled_cards()
        return cards[:12], cards[12:24], cards[24:36], cards[36:]

    @classmethod
    def _shuffled_cards(cls):
        cards = cls.all_cards()
        return tuple(random.sample(cards, k=len(cards)))

    @classmethod
    @functools.cache
    def all_cards(cls) -> Tuple[Card, ...]:
        return tuple(Card(suit=suit, rank=rank) for suit in Suit for rank in Rank) * 2
