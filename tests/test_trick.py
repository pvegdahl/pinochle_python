import pytest

from cards import Card, Rank, Suit
from trick import get_trick_winner


@pytest.mark.parametrize("cards, expected", [
    ((Card(Rank.KING, Suit.DIAMONDS), Card(Rank.ACE, Suit.DIAMONDS)), Card(Rank.ACE, Suit.DIAMONDS)),
    ((Card(Rank.ACE, Suit.SPADES), Card(Rank.QUEEN, Suit.SPADES)), Card(Rank.ACE, Suit.SPADES)),
    ((Card(Rank.KING, Suit.DIAMONDS), Card(Rank.ACE, Suit.HEARTS)), Card(Rank.KING, Suit.DIAMONDS)),
])
def test_highest_card_in_led_suit_wins(cards, expected):
    assert get_trick_winner(cards=cards) == expected


# TODO
# - Trump beats non trump
# - Higher trump wins
# - Off suit not trump always loses
# - First of duplicate cards wins
