import pytest

from cards import Card, Rank, Suit
from trick import get_trick_winning_card, get_trick_winner_index


@pytest.mark.parametrize("cards, expected_card", [
    ((Card(Rank.KING, Suit.DIAMONDS), Card(Rank.ACE, Suit.DIAMONDS)), Card(Rank.ACE, Suit.DIAMONDS)),
    ((Card(Rank.ACE, Suit.SPADES), Card(Rank.QUEEN, Suit.SPADES)), Card(Rank.ACE, Suit.SPADES)),
    ((Card(Rank.KING, Suit.DIAMONDS), Card(Rank.ACE, Suit.HEARTS)), Card(Rank.KING, Suit.DIAMONDS)),
])
def test_highest_card_in_led_suit_wins(cards, expected_card):
    assert get_trick_winning_card(cards=cards, trump=Suit.CLUBS) == expected_card


@pytest.mark.parametrize("cards, expected_card", [
    ((Card(Rank.ACE, Suit.SPADES), Card(Rank.NINE, Suit.CLUBS)), Card(Rank.NINE, Suit.CLUBS)),
    ((Card(Rank.ACE, Suit.SPADES), Card(Rank.TEN, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)), Card(Rank.ACE, Suit.CLUBS)),
])
def test_trump_beats_non_trump(cards, expected_card):
    assert get_trick_winning_card(cards=cards, trump=Suit.CLUBS) == expected_card


@pytest.mark.parametrize("cards, expected_index", [
    ((Card(Rank.KING, Suit.DIAMONDS), Card(Rank.ACE, Suit.DIAMONDS)), 1),
    ((Card(Rank.ACE, Suit.SPADES), Card(Rank.QUEEN, Suit.SPADES)), 0),
    ((Card(Rank.KING, Suit.DIAMONDS), Card(Rank.ACE, Suit.HEARTS)), 0),
    ((Card(Rank.ACE, Suit.SPADES), Card(Rank.NINE, Suit.CLUBS)), 1),
    ((Card(Rank.ACE, Suit.SPADES), Card(Rank.TEN, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)), 2),
    ((Card(Rank.KING, Suit.DIAMONDS), Card(Rank.ACE, Suit.DIAMONDS), Card(Rank.ACE, Suit.DIAMONDS)), 1),
])
def test_get_trick_winner_index(cards, expected_index):
    assert get_trick_winner_index(cards=cards, trump=Suit.CLUBS) == expected_index
