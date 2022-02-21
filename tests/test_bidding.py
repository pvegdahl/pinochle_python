import pytest

from bidding import BiddingState, InvalidBid


@pytest.fixture(scope="function")
def bid():
    return BiddingState(current_bid=25)


def test_bid_updates_current_bid(bid):
    bid = bid.new_bid(26)
    assert bid.current_bid == 26


def test_reject_lower_bids(bid):
    with pytest.raises(InvalidBid) as e:
        bid.new_bid(24)
    assert e.match("New bid of 24 did not exceed the current bid of 25")


def test_reject_equal_bids(bid):
    with pytest.raises(InvalidBid) as e:
        bid.new_bid(25)
    assert e.match("New bid of 25 did not exceed the current bid of 25")


