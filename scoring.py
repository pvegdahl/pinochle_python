from typing import List, NamedTuple

from cards import Card, Suit, Rank


class Meld(NamedTuple):
    nines_of_trump: int = 0
    marriages: int = 0


def score_meld(hand: List[Card], trump: Suit) -> int:
    meld = MeldCounter(hand=hand, trump=trump).count()
    score = meld.nines_of_trump + meld.marriages * 2
    return score


class MeldCounter:
    def __init__(self, hand: List[Card], trump: Suit):
        self.hand = hand
        self.trump = trump

    def count(self) -> Meld:
        return Meld(
            nines_of_trump=self._nines_of_trump(), marriages=self._all_marriages()
        )

    def _nines_of_trump(self):
        return len([card for card in self.hand if card == Card(Rank.NINE, self.trump)])

    def _all_marriages(self):
        result = 0
        for suit in Suit:
            result += self._marriages_in_suit(suit)
        return result

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
