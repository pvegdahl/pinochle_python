from typing import NamedTuple


class InvalidBid(Exception):
    pass

class BiddingState(NamedTuple):
    current_bid: int

    def new_bid(self, bid) -> "BiddingState":
        if bid <= self.current_bid:
            raise InvalidBid(f"New bid of {bid} did not exceed the current bid of {self.current_bid}")

        return self._replace(current_bid=bid)
