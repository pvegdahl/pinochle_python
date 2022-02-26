from typing import NamedTuple, Tuple, Optional


class InvalidBid(Exception):
    pass


class BiddingState(NamedTuple):
    current_bid: int
    active_players: Tuple[str, ...]
    current_player_index: int = 0

    def new_bid(self, bid: int, player: str) -> "BiddingState":
        self._validate_bid(bid, player)

        return self._replace(current_bid=bid, current_player_index=self._get_next_bidder_index())

    def _validate_bid(self, bid, player):
        self._validate_player_can_bid(player=player)

        if bid <= self.current_bid:
            raise InvalidBid(f"New bid of {bid} did not exceed the current bid of {self.current_bid}")

    def _validate_player_can_bid(self, player: str) -> None:
        if len(self.active_players) == 1:
            raise InvalidBid("Bidding is over")

        if player != self.current_player():
            raise InvalidBid(f"{player} cannot take actions on {self.current_player()}'s turn")

    def _get_next_bidder_index(self):
        return (self.current_player_index + 1) % len(self.active_players)

    def current_player(self) -> str:
        return self.active_players[self.current_player_index]

    def pass_bidding(self, player: str) -> "BiddingState":
        self._validate_player_can_bid(player=player)

        return self._replace(
            active_players=tuple(p for p in self.active_players if p != player),
            current_player_index=self._get_next_bidder_index_when_passing(),
        )

    def _get_next_bidder_index_when_passing(self):
        new_active_players_size = len(self.active_players) - 1
        return self.current_player_index % new_active_players_size

    def get_winner(self) -> Optional[str]:
        if len(self.active_players) == 1:
            return self.active_players[0]
        return None
