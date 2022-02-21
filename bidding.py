from typing import NamedTuple


class BiddingState(NamedTuple):
    current_bid: int = 0

    def new_bid(self, bid) -> "BiddingState":
        return self._replace(current_bid=bid)
