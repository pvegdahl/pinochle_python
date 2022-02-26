from typing import Tuple

import pytest

from bidding import BiddingState, InvalidBid
from cards import Suit


@pytest.fixture(scope="session")
def players() -> Tuple[str, ...]:
    return "a", "b", "c", "d"


@pytest.fixture(scope="session")
def bidding_state(players: Tuple[str, ...]) -> BiddingState:
    return BiddingState(current_bid=25, active_players=players)


@pytest.fixture(scope="session")
def bidding_state_with_single_remaining_player():
    return BiddingState(current_bid=35, active_players=("bid_winner",))


def test_bid_updates_current_bid(bidding_state: BiddingState) -> None:
    bidding_state = bidding_state.new_bid(bid=26, player="a")
    assert bidding_state.current_bid == 26


def test_reject_lower_bids(bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.new_bid(bid=24, player="a")
    assert e.value.args[0] == "New bid of 24 did not exceed the current bid of 25"


def test_reject_equal_bids(bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.new_bid(bid=25, player="a")
    assert e.value.args[0] == "New bid of 25 did not exceed the current bid of 25"


def test_reject_bids_with_only_one_player_left(
    bidding_state_with_single_remaining_player: BiddingState,
) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state_with_single_remaining_player.new_bid(40, "bid_winner")
    assert e.value.args[0] == "Bidding is over"


def test_update_current_bidder(bidding_state: BiddingState) -> None:
    for expected_bidder in ["a", "b", "c", "d", "a"]:
        assert bidding_state.current_player() == expected_bidder
        bidding_state = bidding_state.new_bid(bid=bidding_state.current_bid + 1, player=bidding_state.current_player())


def test_reject_bids_by_wrong_player(bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.new_bid(bid=26, player="b")
    assert e.match("b cannot take actions on a's turn")


@pytest.mark.parametrize(
    "active_player, expected",
    [
        ("a", ("b", "c", "d")),
        ("b", ("a", "c", "d")),
        ("c", ("a", "b", "d")),
        ("d", ("a", "b", "c")),
    ],
)
def test_player_can_pass_and_is_removed_from_bidding(
    active_player: str, expected: Tuple[str, ...], players: Tuple[str, ...]
) -> None:
    bidding_state = _create_bidding_state_with_active_player(active_player=active_player, players=players)
    bidding_state = bidding_state.pass_bidding(active_player)
    assert bidding_state.active_players == expected


def _create_bidding_state_with_active_player(active_player: str, players: Tuple[str, ...]) -> BiddingState:
    return BiddingState(
        current_bid=25,
        active_players=players,
        current_player_index=players.index(active_player),
    )


@pytest.mark.parametrize("player", ["b", "c", "d"])
def test_only_current_bidder_can_pass(player: str, bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.pass_bidding(player)
    assert e.match(f"{player} cannot take actions on a's turn")


@pytest.mark.parametrize(
    "active_player, expected",
    [
        ("a", "b"),
        ("b", "c"),
        ("c", "d"),
        ("d", "a"),
    ],
)
def test_passing_moves_to_correct_next_player(active_player: str, expected: str, players: Tuple[str, ...]) -> None:
    bidding_state = _create_bidding_state_with_active_player(active_player=active_player, players=players)
    bidding_state = bidding_state.pass_bidding(active_player)
    assert bidding_state.current_player() == expected


def test_bidding_rotation_as_players_are_passing(bidding_state: BiddingState) -> None:
    bidding_state = bidding_state.pass_bidding("a").new_bid(26, "b").new_bid(27, "c").new_bid(28, "d")
    assert bidding_state.current_player() == "b"
    bidding_state = bidding_state.new_bid(29, "b").new_bid(30, "c").pass_bidding("d")
    assert bidding_state.current_player() == "b"
    bidding_state = bidding_state.pass_bidding("b")
    assert bidding_state.current_player() == "c"


def test_no_passing_with_only_one_player_left(
    bidding_state_with_single_remaining_player: BiddingState,
) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state_with_single_remaining_player.pass_bidding("bid_winner")
    assert e.value.args[0] == "Bidding is over"


def test_winning_bidder_is_last_player_standing(
    bidding_state_with_single_remaining_player: BiddingState,
) -> None:
    assert bidding_state_with_single_remaining_player.get_winner() == "bid_winner"


def test_no_winning_bidder_with_multiple_players_left(
    bidding_state: BiddingState,
) -> None:
    assert bidding_state.get_winner() is None


@pytest.mark.parametrize("trump", [suit for suit in Suit])
def test_set_trump_does_what_it_says(bidding_state_with_single_remaining_player: BiddingState, trump: Suit):
    winning_bidder = bidding_state_with_single_remaining_player.get_winner()
    bidding_state = bidding_state_with_single_remaining_player.set_trump(player=winning_bidder, trump=trump)
    assert bidding_state.trump == trump


@pytest.mark.parametrize("player", ["a", "b", "c", "d"])
def test_cannot_set_trump_while_bidding_still_in_progress(player: str, bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.set_trump(player=player, trump=Suit.SPADES)
    assert e.value.args[0] == "Cannot set trump while bidding is still in progress"


@pytest.mark.parametrize("player", ["alice", "bob", "charlie"])
def test_set_trump_only_available_to_bid_winner(
    player: str, bidding_state_with_single_remaining_player: BiddingState
) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state_with_single_remaining_player.set_trump(player=player, trump=Suit.SPADES)
    assert e.value.args[0] == f"{player} cannot set trump, bid_winner won the bid"


def test_cannot_set_trump_if_trump_already_set(bidding_state_with_single_remaining_player: BiddingState):
    winning_bidder = bidding_state_with_single_remaining_player.get_winner()
    bidding_state = bidding_state_with_single_remaining_player.set_trump(player=winning_bidder, trump=Suit.HEARTS)
    with pytest.raises(InvalidBid) as e:
        bidding_state.set_trump(player=winning_bidder, trump=Suit.CLUBS)
    assert e.value.args[0] == "Trump has already been set"
