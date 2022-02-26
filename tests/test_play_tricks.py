from typing import Tuple

import pytest

from cards import Card, Suit, Rank
from play_tricks import PlayTricksState


@pytest.fixture(scope="session")
def start_of_play(sorted_hands: Tuple[Tuple[Card, ...], ...]) -> PlayTricksState:
    return PlayTricksState(hands=sorted_hands)


def test_play_card_removes_card_from_hand(start_of_play: PlayTricksState) -> None:
    play_state = start_of_play.play_card(player="a", card=Card(Rank.ACE, Suit.CLUBS))
    assert sorted(play_state.hands[0]) == sorted(
        (
            Card(Rank.ACE, Suit.CLUBS),
            Card(Rank.TEN, Suit.CLUBS),
            Card(Rank.TEN, Suit.CLUBS),
            Card(Rank.KING, Suit.CLUBS),
            Card(Rank.KING, Suit.CLUBS),
            Card(Rank.QUEEN, Suit.CLUBS),
            Card(Rank.QUEEN, Suit.CLUBS),
            Card(Rank.JACK, Suit.CLUBS),
            Card(Rank.JACK, Suit.CLUBS),
            Card(Rank.NINE, Suit.CLUBS),
            Card(Rank.NINE, Suit.CLUBS),
        )
    )


# TODO
#  - Is it their turn?
#  - Check that the player has the card
#  - Check that the played card is valid
#    + Matches suit if possible
#    + Trump if not possible to match suit
#    + Higher than current winner if possible
#  - Progress play to next player
#  - When a trick is over:
#    + Who won the trick?
#    + In the event of a tie, the first player playing that card is the winner
#    + Credit the trick points correctly
#    + (Including point for last trick)
#    + Select the appropriate next player
