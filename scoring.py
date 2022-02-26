from typing import List, NamedTuple

from cards import Card, Suit, Rank


class Meld(NamedTuple):
    nines_of_trump: int
    non_trump_marriages: int
    trump_marriages: int
    jacks_around: int
    queens_around: int
    kings_around: int
    aces_around: int
    runs_in_trump: int
    pinochles: int

    def score(self) -> int:
        return (
            self.nines_of_trump
            + self._score_marriages()
            + self._score_jacks_around()
            + self._score_queens_around()
            + self._score_kings_around()
            + self._score_aces_around()
            + self._score_runs_in_trump()
            + self._score_pinochle()
        )

    def _score_marriages(self) -> int:
        return self.non_trump_marriages * 2 + self.trump_marriages * 4

    def _score_jacks_around(self) -> int:
        return self._score_with_10x_for_double(self.jacks_around, 4)

    @staticmethod
    def _score_with_10x_for_double(count: int, base_score: int) -> int:
        if count == 0:
            return 0
        elif count == 1:
            return base_score
        elif count == 2:
            return 10 * base_score
        else:
            raise Exception(f"Count should always be 0, 1, or 2.  Got {count}")

    def _score_queens_around(self) -> int:
        return self._score_with_10x_for_double(self.queens_around, 6)

    def _score_kings_around(self) -> int:
        return self._score_with_10x_for_double(self.kings_around, 8)

    def _score_aces_around(self) -> int:
        return self._score_with_10x_for_double(self.aces_around, 10)

    def _score_runs_in_trump(self) -> int:
        return self._score_with_10x_for_double(self.runs_in_trump, 15)

    def _score_pinochle(self) -> int:
        if self.pinochles == 0:
            return 0
        elif self.pinochles == 1:
            return 4
        elif self.pinochles == 2:
            return 30
        else:
            raise Exception(f"Pinochles should always be 0, 1, or 2.  Got {self.pinochles}")


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
            runs_in_trump=self._runs_in_trump(),
            pinochles=self._pinochles(),
        )

    def _nines_of_trump(self) -> int:
        return self.hand.count(Card(Rank.NINE, self.trump))

    def _non_trump_marriages(self) -> int:
        return sum(self._marriages_in_suit(suit) for suit in self._non_trump_suits())

    def _non_trump_suits(self) -> List[Suit]:
        return [suit for suit in Suit if suit != self.trump]

    def _marriages_in_suit(self, suit: Suit) -> int:
        return self._count_combinations([Card(Rank.QUEEN, suit), Card(Rank.KING, suit)])

    def _count_combinations(self, target_cards):
        card_counts = [self.hand.count(card) for card in target_cards]
        return min(card_counts)

    def _trump_marriages(self) -> int:
        return self._marriages_in_suit(self.trump) - self._runs_in_trump()

    def _count_around(self, rank: Rank) -> int:
        return self._count_combinations([Card(rank, suit) for suit in Suit])

    def _runs_in_trump(self) -> int:
        return self._count_combinations([Card(rank, self.trump) for rank in Rank if rank != Rank.NINE])

    def _pinochles(self) -> int:
        return self._count_combinations([Card(Rank.JACK, Suit.DIAMONDS), Card(Rank.QUEEN, Suit.SPADES)])
