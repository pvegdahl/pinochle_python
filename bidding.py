from typing import NamedTuple, Tuple


class InvalidBid(Exception):
    pass


class BiddingState(NamedTuple):
    current_bid: int
    players: Tuple[str, str, str, str]
    current_bidder_index: int = 0

    def new_bid(self, bid: int) -> "BiddingState":
        if bid <= self.current_bid:
            raise InvalidBid(
                f"New bid of {bid} did not exceed the current bid of {self.current_bid}"
            )

        return self._replace(current_bid=bid, current_bidder_index=self._get_next_bidder_index())

    def _get_next_bidder_index(self):
        return (self.current_bidder_index + 1) % 4

    def current_bidder(self) -> str:
        return self.players[self.current_bidder_index]