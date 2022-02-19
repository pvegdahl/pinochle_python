from typing import List, NamedTuple

from cards import Card, Suit, Rank


class Meld(NamedTuple):
    nines_of_trump: int = 0
    non_trump_marriages: int = 0
    trump_marriages: int = 0


def score_meld(hand: List[Card], trump: Suit) -> int:
    meld = MeldCounter(hand=hand, trump=trump).count()
    score = (
        meld.nines_of_trump + meld.non_trump_marriages * 2 + meld.trump_marriages * 4
    )
    return score


class MeldCounter:
    def __init__(self, hand: List[Card], trump: Suit):
        self.hand = hand
        self.trump = trump

    def count(self) -> Meld:
        return Meld(
            nines_of_trump=self._nines_of_trump(),
            non_trump_marriages=self._non_trump_marriages(),
            trump_marriages=self._trump_marriages(),
        )

    def _nines_of_trump(self):
        return len([card for card in self.hand if card == Card(Rank.NINE, self.trump)])

    def _non_trump_marriages(self):
        result = 0
        for suit in self._non_trump_suits():
            result += self._marriages_in_suit(suit)
        return result

    def _non_trump_suits(self):
        return [suit for suit in Suit if suit != self.trump]

    def _marriages_in_suit(self, suit: Suit):
        queen_count = len(
            [
                card
                for card in self.hand
                if card.rank == Rank.QUEEN and card.suit == suit
            ]
        )
        king_count = len(
            [card for card in self.hand if card.rank == Rank.KING and card.suit == suit]
        )
        if queen_count and king_count:
            return int((queen_count + king_count) / 2)
        return 0

    def _trump_marriages(self):
        return self._marriages_in_suit(self.trump)
