from typing import Tuple, NamedTuple

import pytest

from cards import Card, Suit, Rank
from play_tricks import PlayTricksState, InvalidPlay


@pytest.fixture(scope="session")
def start_of_play_a(players: Tuple[str, str, str, str], sorted_hands: Tuple[Tuple[Card, ...], ...]) -> PlayTricksState:
    return PlayTricksState(hands=sorted_hands, players=players, next_player="a")


@pytest.fixture(scope="session")
def players() -> Tuple[str, str, str, str]:
    return "a", "b", "c", "d"


@pytest.fixture(scope="session", params=["a", "b", "c", "d"])
def start_of_play(
    request, players: Tuple[str, str, str, str], sorted_hands: Tuple[Tuple[Card, ...], ...]
) -> PlayTricksState:
    return PlayTricksState(hands=sorted_hands, players=players, next_player=request.param)


def test_play_card_removes_card_from_hand(start_of_play: PlayTricksState) -> None:
    player = start_of_play.next_player
    player_index = start_of_play.players.index(player)
    player_suit = start_of_play.hands[player_index][0].suit
    play_state = start_of_play.play_card(player=start_of_play.next_player, card=Card(Rank.ACE, player_suit))
    assert sorted(play_state.hands[player_index]) == sorted(
        (
            Card(Rank.ACE, player_suit),
            Card(Rank.TEN, player_suit),
            Card(Rank.TEN, player_suit),
            Card(Rank.KING, player_suit),
            Card(Rank.KING, player_suit),
            Card(Rank.QUEEN, player_suit),
            Card(Rank.QUEEN, player_suit),
            Card(Rank.JACK, player_suit),
            Card(Rank.JACK, player_suit),
            Card(Rank.NINE, player_suit),
            Card(Rank.NINE, player_suit),
        )
    )


@pytest.mark.parametrize(
    "player, card",
    [
        ("b", Card(Rank.ACE, Suit.DIAMONDS)),
        ("c", Card(Rank.ACE, Suit.HEARTS)),
        ("d", Card(Rank.ACE, Suit.SPADES)),
    ],
)
def test_cannot_play_out_of_turn(player: str, card: Card, start_of_play_a: PlayTricksState) -> None:
    with pytest.raises(InvalidPlay) as e:
        start_of_play_a.play_card(player=player, card=card)
    assert e.value.args[0] == f"{player} cannot play on a's turn"


def test_cannot_play_card_not_in_hand(start_of_play_a: PlayTricksState) -> None:
    with pytest.raises(InvalidPlay) as e:
        start_of_play_a.play_card(player="a", card=Card(Rank.JACK, Suit.DIAMONDS))
    assert e.value.args[0] == "a does not have a Jack of Diamonds in hand"


# TODO
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
