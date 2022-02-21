from typing import Tuple

import pytest

from bidding import BiddingState
from cards import CardDeck, Suit
from pinochle_game import PinochleGame, GameState


@pytest.fixture(scope="session")
def players() -> Tuple[str, str, str, str]:
    return "a", "b", "c", "d"


@pytest.fixture(scope="session")
def new_game(players: Tuple[str, str, str, str]) -> PinochleGame:
    return PinochleGame.new_game(players=players)


@pytest.fixture(scope="session")
def bidding_complete_game(players: Tuple[str, str, str, str]) -> PinochleGame:
    return PinochleGame(
        state=GameState.BIDDING,
        players=players,
        hands=CardDeck.deal(),
        bidding=BiddingState(active_players=("a",), current_bid=25),
        trump=None,
    )


def test_new_game_state_is_bidding(new_game) -> None:
    assert new_game.state == GameState.BIDDING
    assert new_game.bidding is not None


def test_new_game_deals_cards_to_players(new_game) -> None:
    assert len(new_game.hands) == 4


def test_no_trump_at_start(new_game) -> None:
    assert new_game.trump is None


@pytest.mark.parametrize("trump_suit", [suit for suit in Suit])
def test_set_trump_does_what_it_says(
    trump_suit: Suit, bidding_complete_game: PinochleGame
) -> None:
    game = bidding_complete_game.select_trump(player="a", trump=trump_suit)
    assert game.trump == trump_suit


def test_set_trump_advances_state_to_passing(
    bidding_complete_game: PinochleGame,
) -> None:
    game = bidding_complete_game.select_trump(player="a", trump=Suit.DIAMONDS)
    assert game.state == GameState.PASSING
