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
        ] * 2 + [
            Card(Rank.JACK, Suit.SPADES),
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.HEARTS),
        ] * 2
        assert score_meld(hand=hand, trump=Suit.SPADES) == 0

    def test_nine_of_trump(self):
        assert score_meld(hand=[Card(Rank.NINE, Suit.HEARTS)], trump=Suit.HEARTS) == 1

    def test_2x_nine_of_trump(self):
        assert (
            score_meld(hand=[Card(Rank.NINE, Suit.HEARTS)] * 2, trump=Suit.HEARTS) == 2
        )
