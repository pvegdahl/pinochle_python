from typing import List, NamedTuple

from cards import Card, Suit, Rank


class Meld(NamedTuple):
    nines_of_trump: int = 0
    non_trump_marriages: int = 0
    trump_marriages: int = 0
    jacks_around: int = 0
    queens_around: int = 0
    kings_around: int = 0
    aces_around: int = 0

    def score(self) -> int:
        return (
            self.nines_of_trump
            + self._score_marriages()
            + self._score_jacks_around()
            + self._score_queens_around()
            + self._score_kings_around()
            + self._score_aces_around()
        )

    def _score_marriages(self) -> int:
        return self.non_trump_marriages * 2 + self.trump_marriages * 4

    def _score_jacks_around(self):
        return self._score_around(self.jacks_around, 4)

    def _score_queens_around(self):
        return self._score_around(self.queens_around, 6)

    def _score_kings_around(self):
        return self._score_around(self.kings_around, 8)

    def _score_around(self, count, base_score):
        match count:
            case 0:
                return 0
            case 1:
                return base_score
            case 2:
                return base_score * 10

    def _score_aces_around(self):
        return self._score_around(self.aces_around, 10)


def score_meld(hand: List[Card], trump: Suit) -> int:
    meld = MeldCounter(hand=hand, trump=trump).count()
    return meld.score()


class MeldCounter:
    def __init__(self, hand: List[Card], trump: Suit):
        self.hand = hand
        self.trump = trump

    def count(self) -> Meld:
        return Meld(
            nines_of_trump=self._nines_of_trump(),
            non_trump_marriages=self._non_trump_marriages(),
            trump_marriages=self._trump_marriages(),
            jacks_around=self._count_around(Rank.JACK),
            queens_around=self._count_around(Rank.QUEEN),
            kings_around=self._count_around(Rank.KING),
            aces_around=self._count_around(Rank.ACE),
        )

    def _nines_of_trump(self) -> int:
        return len([card for card in self.hand if card == Card(Rank.NINE, self.trump)])

    def _non_trump_marriages(self) -> int:
        result = 0
        for suit in self._non_trump_suits():
            result += self._marriages_in_suit(suit)
        return result

    def _non_trump_suits(self) -> List[Suit]:
        return [suit for suit in Suit if suit != self.trump]

    def _marriages_in_suit(self, suit: Suit) -> int:
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

    def _trump_marriages(self) -> int:
        return self._marriages_in_suit(self.trump)

    def _count_around(self, rank: Rank) -> int:
        matching_cards = [card for card in self.hand if card.rank == rank]
        if len(matching_cards) == 8:
            return 2
        suits = set(card.suit for card in matching_cards)
        if len(suits) == 4:
            return 1
        return 0
