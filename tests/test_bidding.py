from typing import Tuple

import pytest

from bidding import BiddingState, InvalidBid


@pytest.fixture(scope="session")
def players() -> Tuple[str, ...]:
    return "a", "b", "c", "d"


@pytest.fixture(scope="session")
def bidding_state(players: Tuple[str, ...]) -> BiddingState:
    return BiddingState(current_bid=25, players=players)


def test_bid_updates_current_bid(bidding_state: BiddingState) -> None:
    bidding_state = bidding_state.new_bid(bid=26, player="a")
    assert bidding_state.current_bid == 26


def test_reject_lower_bids(bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.new_bid(bid=24, player="a")
    assert e.match("New bid of 24 did not exceed the current bid of 25")


def test_reject_equal_bids(bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.new_bid(bid=25, player="a")
    assert e.match("New bid of 25 did not exceed the current bid of 25")


def test_update_current_bidder(bidding_state: BiddingState) -> None:
    for expected_bidder in ["a", "b", "c", "d", "a"]:
        assert bidding_state.current_bidder() == expected_bidder
        bidding_state = bidding_state.new_bid(bid=bidding_state.current_bid+1, player=bidding_state.current_bidder())


def test_reject_bids_by_wrong_player(bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.new_bid(bid=26, player="b")


@pytest.mark.parametrize("bidder_name, expected", [
    ("a", ("b", "c", "d")),
    ("b", ("a", "c", "d")),
    ("c", ("a", "b", "d")),
    ("d", ("a", "b", "c")),
])
def test_player_can_pass_and_is_removed_from_bidding(bidder_name: str, expected: Tuple[str, ...], players: Tuple[str, ...]) -> None:
    bidding_state = BiddingState(current_bid=25, players=players, current_bidder_index=players.index(bidder_name))
    bidding_state = bidding_state.pass_bidding(bidder_name)
    assert bidding_state.players == expected


# Bidding ends when there is only one bidder
# Winning bidder is the last one standing
# Only current bidder can pass
# Bidder who passes is the one actually removed