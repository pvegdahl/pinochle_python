from enum import Enum
from typing import NamedTuple, Tuple, Optional

from pinochle.bidding import BiddingState
from pinochle.cards import Card, CardDeck, Suit


class GameState(Enum):
    BIDDING = "Bidding"
    PASSING_TO_BID_WINNER = "PassingToBidWinner"

    def __str__(self):
        return self.value


class IllegalPass(Exception):
    pass


class PinochleGame(NamedTuple):
    state: GameState
    players: Tuple[str, str, str, str]
    hands: Tuple[Tuple[Card, ...], Tuple[Card, ...], Tuple[Card, ...], Tuple[Card, ...]]
    bidding: BiddingState
    trump: Optional[Suit]

    @classmethod
    def new_game(cls, players: Tuple[str, str, str, str]) -> "PinochleGame":
        return PinochleGame(
            state=GameState.BIDDING,
            players=players,
            hands=CardDeck.deal(),
            bidding=BiddingState(current_bid=24, active_players=players),
            trump=None,
        )

    def select_trump(self, player: str, trump: Suit) -> "PinochleGame":
        return self._replace(trump=trump, state=GameState.PASSING_TO_BID_WINNER)

    def _get_bid_winner(self) -> str:
        return self.bidding.get_winner()

    def _get_bid_winner_partner(self) -> str:
        bid_winner_index = self.players.index(self._get_bid_winner())
        partner_index = (bid_winner_index + 2) % 4
        return self.players[partner_index]
