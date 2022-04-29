from typing import Tuple, NamedTuple

import pytest

from cards import Card, Suit, Rank
from play_tricks import PlayTricksState, InvalidPlay


PLAYERS = ("a", "b", "c", "d")


@pytest.fixture(scope="session")
def start_of_play_a(sorted_hands: Tuple[Tuple[Card, ...], ...]) -> PlayTricksState:
    return PlayTricksState(hands=sorted_hands, players=PLAYERS, player_index=0, trump=Suit.SPADES)


@pytest.fixture(scope="session", params=range(4))
def start_of_play(request, sorted_hands: Tuple[Tuple[Card, ...], ...]) -> PlayTricksState:
    return PlayTricksState(hands=sorted_hands, players=PLAYERS, player_index=request.param, trump=Suit.SPADES)


@pytest.fixture(scope="session")
def middle_of_play() -> PlayTricksState:
    hands = (
        (Card(Rank.JACK, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
        (Card(Rank.QUEEN, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)),
        (Card(Rank.JACK, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS)),
        (Card(Rank.TEN, Suit.SPADES), Card(Rank.ACE, Suit.SPADES)),
    )
    return PlayTricksState(hands=hands, players=PLAYERS, player_index=0, trump=Suit.SPADES)


def test_play_card_removes_card_from_hand(start_of_play: PlayTricksState) -> None:
    player_suit = _get_player_suit(start_of_play)
    play_state = start_of_play.play_card(player=start_of_play.current_player(), card=Card(Rank.ACE, player_suit))
    assert sorted(play_state.hands[_get_player_index(start_of_play)]) == sorted(
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


def _get_player_index(play_state: PlayTricksState) -> int:
    return play_state.player_index


def _get_player_suit(play_state: PlayTricksState) -> Suit:
    return play_state.hands[_get_player_index(play_state)][0].suit


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
    assert e.value.args[0] == "Invalid card played"


def test_play_progresses_to_next_player(start_of_play: PlayTricksState) -> None:
    play_state = start_of_play.play_card(
        player=start_of_play.current_player(), card=Card(Rank.NINE, _get_player_suit(start_of_play))
    )
    assert play_state.current_player() == _get_next_player(start_of_play.current_player())


def _get_next_player(player: str) -> str:
    return {"a": "b", "b": "c", "c": "d", "d": "a"}[player]


def test_valid_plays_do_not_raise_exception(middle_of_play: PlayTricksState) -> None:
    play_state = middle_of_play.play_card(player="a", card=Card(Rank.JACK, Suit.CLUBS))

    # No exceptions thrown because...
    # Matches suit and greater
    play_state = play_state.play_card(player="b", card=Card(Rank.QUEEN, Suit.CLUBS))

    # Matches suit and cannot be greater
    play_state = play_state.play_card(player="c", card=Card(Rank.JACK, Suit.CLUBS))

    # Cannot match suit so doesn't
    play_state.play_card(player="d", card=Card(Rank.TEN, Suit.SPADES))


def test_played_card_throws_exception_if_suit_not_matched(middle_of_play: PlayTricksState):
    play_state = middle_of_play.play_card(player="a", card=Card(Rank.JACK, Suit.CLUBS))

    # No exception
    play_state.play_card(player="b", card=Card(Rank.QUEEN, Suit.CLUBS))

    with pytest.raises(InvalidPlay) as e:
        play_state.play_card(player="b", card=Card(Rank.ACE, Suit.DIAMONDS))
    assert e.value.args[0] == "Invalid card played"


def test_played_card_must_beat_trick_if_possible() -> None:
    hands = (
        (Card(Rank.JACK, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
        (Card(Rank.NINE, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
    )
    play_state = PlayTricksState(hands=hands, players=PLAYERS, player_index=0, trump=Suit.SPADES).play_card(
        player="a", card=Card(Rank.JACK, Suit.CLUBS)
    )

    # No exception
    play_state.play_card(player="b", card=Card(Rank.ACE, Suit.CLUBS))

    with pytest.raises(InvalidPlay) as e:
        play_state.play_card(player="b", card=Card(Rank.NINE, Suit.CLUBS))
    assert e.value.args[0] == "Invalid card played"


def test_must_win_with_trump_if_cannot_match_suit() -> None:
    hands = (
        (Card(Rank.JACK, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
        (Card(Rank.NINE, Suit.SPADES), Card(Rank.ACE, Suit.HEARTS)),
    )
    play_state = PlayTricksState(hands=hands, players=PLAYERS, player_index=0, trump=Suit.HEARTS).play_card(
        "a", Card(Rank.ACE, Suit.CLUBS)
    )

    # No exception
    play_state.play_card(player="b", card=Card(Rank.ACE, Suit.HEARTS))

    with pytest.raises(InvalidPlay) as e:
        play_state.play_card(player="b", card=Card(Rank.NINE, Suit.SPADES))
    assert e.value.args[0] == "Invalid card played"


def test_must_play_trump_if_cannot_match_even_if_that_trump_loses() -> None:
    hands = (
        (Card(Rank.JACK, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
        (Card(Rank.NINE, Suit.SPADES), Card(Rank.ACE, Suit.HEARTS)),
        (Card(Rank.NINE, Suit.SPADES), Card(Rank.JACK, Suit.HEARTS)),
    )

    play_state = (
        PlayTricksState(hands=hands, players=PLAYERS, player_index=0, trump=Suit.HEARTS)
        .play_card("a", Card(Rank.ACE, Suit.CLUBS))
        .play_card("b", Card(Rank.ACE, Suit.HEARTS))
    )

    # No exception
    play_state.play_card(player="c", card=Card(Rank.JACK, Suit.HEARTS))

    with pytest.raises(InvalidPlay) as e:
        play_state.play_card(player="c", card=Card(Rank.NINE, Suit.SPADES))
    assert e.value.args[0] == "Invalid card played"


def test_cannot_play_trump_if_matching_suit_available() -> None:
    hands = (
        (Card(Rank.JACK, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
        (Card(Rank.ACE, Suit.CLUBS), Card(Rank.NINE, Suit.HEARTS)),
    )
    play_state = PlayTricksState(hands=hands, players=PLAYERS, player_index=0, trump=Suit.HEARTS).play_card(
        "a", Card(Rank.ACE, Suit.CLUBS)
    )

    # No exception
    play_state.play_card(player="b", card=Card(Rank.ACE, Suit.CLUBS))

    with pytest.raises(InvalidPlay) as e:
        play_state.play_card(player="b", card=Card(Rank.NINE, Suit.HEARTS))
    assert e.value.args[0] == "Invalid card played"


def test_must_play_winning_trump_if_possible() -> None:
    hands = (
        (Card(Rank.JACK, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
        (Card(Rank.NINE, Suit.SPADES), Card(Rank.KING, Suit.HEARTS)),
        (Card(Rank.NINE, Suit.HEARTS), Card(Rank.ACE, Suit.HEARTS)),
    )

    play_state = (
        PlayTricksState(hands=hands, players=PLAYERS, player_index=0, trump=Suit.HEARTS)
        .play_card("a", Card(Rank.ACE, Suit.CLUBS))
        .play_card("b", Card(Rank.KING, Suit.HEARTS))
    )

    # No exception
    play_state.play_card(player="c", card=Card(Rank.ACE, Suit.HEARTS))

    with pytest.raises(InvalidPlay) as e:
        play_state.play_card(player="c", card=Card(Rank.NINE, Suit.HEARTS))
    assert e.value.args[0] == "Invalid card played"


def test_can_play_lower_in_suit_card_if_trump_is_winning():
    hands = (
        (Card(Rank.KING, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
        (Card(Rank.NINE, Suit.SPADES), Card(Rank.NINE, Suit.HEARTS)),
        (Card(Rank.QUEEN, Suit.CLUBS), Card(Rank.TEN, Suit.CLUBS)),
    )
    play_state = PlayTricksState(hands=hands, players=PLAYERS, player_index=0, trump=Suit.HEARTS).play_card(
        "a", Card(Rank.KING, Suit.CLUBS)
    ).play_card("b", Card(Rank.NINE, Suit.HEARTS))

    # No exception
    play_state.play_card(player="c", card=Card(Rank.QUEEN, Suit.CLUBS))


def test_can_play_lower_in_suit_card_if_only_able_to_match():
    hands = (
        (Card(Rank.KING, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
        (Card(Rank.QUEEN, Suit.CLUBS), Card(Rank.ACE, Suit.CLUBS)),
    )
    play_state = PlayTricksState(hands=hands, players=PLAYERS, player_index=0, trump=Suit.HEARTS).play_card(
        "a", Card(Rank.ACE, Suit.CLUBS)
    )

    # No exception
    play_state.play_card(player="b", card=Card(Rank.QUEEN, Suit.CLUBS))


@pytest.mark.parametrize(
    "trick, final_player_index, expected",
    [
        (
            (
                Card(Rank.ACE, Suit.CLUBS),
                Card(Rank.TEN, Suit.CLUBS),
                Card(Rank.KING, Suit.CLUBS),
                Card(Rank.QUEEN, Suit.CLUBS),
            ),
            3,
            0,
        ),
        (
                (
                        Card(Rank.TEN, Suit.CLUBS),
                        Card(Rank.KING, Suit.CLUBS),
                        Card(Rank.ACE, Suit.CLUBS),
                        Card(Rank.QUEEN, Suit.CLUBS),
                ),
                3,
                2,
        ),
        (
                (
                        Card(Rank.TEN, Suit.CLUBS),
                        Card(Rank.KING, Suit.CLUBS),
                        Card(Rank.ACE, Suit.CLUBS),
                        Card(Rank.QUEEN, Suit.CLUBS),
                ),
                2,
                1,
        ),
        (
                (
                        Card(Rank.TEN, Suit.DIAMONDS),
                        Card(Rank.KING, Suit.DIAMONDS),
                        Card(Rank.JACK, Suit.DIAMONDS),
                        Card(Rank.QUEEN, Suit.DIAMONDS),
                ),
                2,
                1,
        ),
    ],
)
def test_index_of_trick_winner(trick, final_player_index, expected) -> None:
    first_3_cards = trick[:3]
    last_card = trick[3]
    hands = ((),) * final_player_index + ((last_card,),) + ((),) * (3 - final_player_index)
    play_state = PlayTricksState(player_index=final_player_index, current_trick=first_3_cards, players=PLAYERS, trump=Suit.CLUBS, hands=hands)
    assert play_state.play_card(PLAYERS[final_player_index], last_card).player_index == expected


# TODO
#  - When a trick is over:
#    + Who won the trick?
#    + In the event of a tie, the first player playing that card is the winner
#    + Credit the trick points correctly
#    + (Including point for last trick)
#    + Select the appropriate next player
#    + Reset trick
