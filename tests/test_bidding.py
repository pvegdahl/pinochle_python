from bidding import BiddingState


def test_bid_updates_current_bid():
    bid = BiddingState()
    bid = bid.new_bid(26)
    assert bid.current_bid == 26
