from typing import NamedTuple, Tuple


class InvalidBid(Exception):
    pass


class BiddingState(NamedTuple):
    current_bid: int
    players: Tuple[str, ...]
    current_player_index: int = 0

    def new_bid(self, bid: int, player: str) -> "BiddingState":
        self._validate_current_player(
            player=player,
            message=f"Player {player} cannot bid on {self.current_player()}'s turn",
        )

        if bid <= self.current_bid:
            raise InvalidBid(
                f"New bid of {bid} did not exceed the current bid of {self.current_bid}"
            )

        return self._replace(
            current_bid=bid, current_player_index=self._get_next_bidder_index()
        )

    def _validate_current_player(self, player: str, message: str) -> None:
        if player != self.current_player():
            raise InvalidBid(message)

    def _get_next_bidder_index(self):
        return (self.current_player_index + 1) % 4

    def current_player(self) -> str:
        return self.players[self.current_player_index]

    def pass_bidding(self, player: str) -> "BiddingState":
        self._validate_current_player(
            player=player,
            message=f"Player {player} cannot pass on {self.current_player()}'s turn",
        )
        return self._replace(players=tuple(p for p in self.players if p != player))
