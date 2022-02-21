import pytest

from bidding import BiddingState, InvalidBid


@pytest.fixture(scope="function")
def bidding_state() -> BiddingState:
    return BiddingState(current_bid=25, players=("a", "b", "c", "d"))


def test_bid_updates_current_bid(bidding_state: BiddingState) -> None:
    bidding_state = bidding_state.new_bid(26)
    assert bidding_state.current_bid == 26


def test_reject_lower_bids(bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.new_bid(24)
    assert e.match("New bid of 24 did not exceed the current bid of 25")


def test_reject_equal_bids(bidding_state: BiddingState) -> None:
    with pytest.raises(InvalidBid) as e:
        bidding_state.new_bid(25)
    assert e.match("New bid of 25 did not exceed the current bid of 25")


def test_update_current_bidder(bidding_state: BiddingState) -> None:
    assert bidding_state.current_bidder() == "a"
    bidding_state = bidding_state.new_bid(26)
    assert bidding_state.current_bidder() == "b"
    bidding_state = bidding_state.new_bid(27)
    assert bidding_state.current_bidder() == "c"
    bidding_state = bidding_state.new_bid(28)
    assert bidding_state.current_bidder() == "d"
    bidding_state = bidding_state.new_bid(29)
    assert bidding_state.current_bidder() == "a"

# def test_reject_bids_by_wrong_player()
