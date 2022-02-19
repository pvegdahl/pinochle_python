import pytest

from cards import Rank, CardDeck, Suit


@pytest.mark.parametrize(
    "lower, higher",
    [
        (Rank.NINE, Rank.JACK),
        (Rank.NINE, Rank.QUEEN),
        (Rank.NINE, Rank.KING),
        (Rank.NINE, Rank.TEN),
        (Rank.NINE, Rank.ACE),
        (Rank.JACK, Rank.QUEEN),
        (Rank.JACK, Rank.KING),
        (Rank.JACK, Rank.TEN),
        (Rank.JACK, Rank.ACE),
        (Rank.QUEEN, Rank.KING),
        (Rank.QUEEN, Rank.TEN),
        (Rank.QUEEN, Rank.ACE),
        (Rank.KING, Rank.TEN),
        (Rank.KING, Rank.ACE),
        (Rank.TEN, Rank.ACE),
    ],
)
def test_rank_ordering(lower, higher):
    assert lower < higher
    assert not lower >= higher


@pytest.mark.parametrize(
    "lower, higher",
    [
        (Suit.CLUBS, Suit.DIAMONDS),
        (Suit.CLUBS, Suit.HEARTS),
        (Suit.CLUBS, Suit.SPADES),
        (Suit.DIAMONDS, Suit.HEARTS),
        (Suit.DIAMONDS, Suit.SPADES),
        (Suit.HEARTS, Suit.SPADES),
    ],
)
def test_suit_ordering(lower, higher):
    assert lower < higher
    assert not lower >= higher


@pytest.mark.parametrize("suit", [pytest.param(suit, id=suit.name) for suit in Suit])
def test_twelve_of_each_suit_in_deck(suit):
    cards_of_suit = [card for card in CardDeck().cards if card.suit == suit]
    assert len(cards_of_suit) == 12


@pytest.mark.parametrize("rank", [pytest.param(rank, id=rank.name) for rank in Rank])
def test_eight_of_each_rank_in_deck(rank):
    cards_of_rank = [card for card in CardDeck().cards if card.rank == rank]
    assert len(cards_of_rank) == 8


@pytest.mark.parametrize(
    "card",
    [
        pytest.param(card, id=f"{card.rank.name} of {card.suit.name}")
        for card in set(CardDeck().cards)
    ],
)
def test_each_card_exists_exactly_twice(card):
    assert len([c for c in CardDeck().cards if c == card]) == 2
