from typing import NamedTuple, List

import pytest

from cards import Suit, Card, Rank
from scoring import score_meld


class TestScoreMeld:
    def test_empty_hand(self):
        assert score_meld(hand=[], trump=Suit.HEARTS) == 0

    def test_nothing_relevant(self):
        hand = [
            Card(Rank.NINE, Suit.CLUBS),
            Card(Rank.NINE, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.HEARTS),
            Card(Rank.JACK, Suit.SPADES),
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.HEARTS),
        ]
        assert score_meld(hand=hand, trump=Suit.SPADES) == 0

    def test_nine_of_trump(self):
        assert score_meld(hand=[Card(Rank.NINE, Suit.HEARTS)], trump=Suit.HEARTS) == 1

    def test_2x_nine_of_trump(self):
        assert (
            score_meld(hand=[Card(Rank.NINE, Suit.HEARTS)] * 2, trump=Suit.HEARTS) == 2
        )

    def test_one_marriage(self):
        hand = [
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
        ]
        assert score_meld(hand=hand, trump=Suit.SPADES) == 2

    def test_one_and_a_half_marriages(self):
        hand = [
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
        ]
        assert score_meld(hand=hand, trump=Suit.SPADES) == 2

    def test_two_marriages_in_different_suits(self):
        hand = [
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.HEARTS),
            Card(Rank.KING, Suit.HEARTS),
        ]
        assert score_meld(hand=hand, trump=Suit.SPADES) == 4

    def test_two_marriages_in_same_suit(self):
        hand = [
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
        ] * 2
        assert score_meld(hand=hand, trump=Suit.SPADES) == 4

    def test_one_marriage_of_trump(self):
        hand = [
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
        ]
        assert score_meld(hand=hand, trump=Suit.DIAMONDS) == 4

    def test_two_marriage_of_trump_and_one_other(self):
        hand = [
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.CLUBS),
            Card(Rank.KING, Suit.CLUBS),
        ]
        assert score_meld(hand=hand, trump=Suit.DIAMONDS) == 10

    class RankAndValue(NamedTuple):
        rank: Rank
        value: int

    @pytest.fixture(
        scope="module", params=[RankAndValue(Rank.JACK, 4), RankAndValue(Rank.QUEEN, 6), RankAndValue(Rank.KING, 8), RankAndValue(Rank.ACE, 10)]
    )
    def rank_and_value(self, request):
        return request.param

    def test_rank_around(self, rank_and_value):
        hand = [Card(rank_and_value.rank, suit) for suit in Suit]
        assert score_meld(hand=hand, trump=Suit.DIAMONDS) == rank_and_value.value

    def test_four_of_rank_but_not_around(self, rank_and_value):
        hand = [
            Card(rank_and_value.rank, Suit.DIAMONDS),
            Card(rank_and_value.rank, Suit.DIAMONDS),
            Card(rank_and_value.rank, Suit.HEARTS),
            Card(rank_and_value.rank, Suit.SPADES),
        ]
        assert score_meld(hand=hand, trump=Suit.DIAMONDS) == 0

    def test_lots_of_one_rank_but_not_around(self, rank_and_value):
        hand = [
            Card(rank_and_value.rank, Suit.DIAMONDS),
            Card(rank_and_value.rank, Suit.HEARTS),
            Card(rank_and_value.rank, Suit.SPADES),
        ] * 2
        assert score_meld(hand=hand, trump=Suit.DIAMONDS) == 0

    def test_double_rank_around(self, rank_and_value):
        hand = [Card(rank_and_value.rank, suit) for suit in Suit] * 2
        assert score_meld(hand=hand, trump=Suit.DIAMONDS) == rank_and_value.value * 10

    def test_run_in_trump(self):
        assert score_meld(hand=self._create_run(Suit.HEARTS), trump=Suit.HEARTS) == 15

    @staticmethod
    def _create_run(suit: Suit) -> List[Card]:
        return [
            Card(Rank.ACE, suit),
            Card(Rank.TEN, suit),
            Card(Rank.KING, suit),
            Card(Rank.QUEEN, suit),
            Card(Rank.JACK, suit),
        ]
