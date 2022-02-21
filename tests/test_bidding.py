import pytest

from bidding import BiddingState, InvalidBid


@pytest.fixture(scope="function")
def bidding_state() -> BiddingState:
    return BiddingState(current_bid=25, players=("a", "b", "c", "d"))


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


def test_reject_bids_by_wrong_player(bidding_state):
    with pytest.raises(InvalidBid) as e:
        bidding_state.new_bid(bid=26, player="b")
