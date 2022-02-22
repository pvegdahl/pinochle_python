from enum import Enum
from typing import NamedTuple, Tuple, Optional

from bidding import BiddingState
from cards import Card, CardDeck, Suit


class GameState(Enum):
    BIDDING = "Bidding"
    PASSING_TO_BID_WINNER = "PassingToBidWinner"


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

    def pass_cards(
        self, source: str, destination: str, cards: Tuple[Card, Card, Card, Card]
    ) -> "PinochleGame":
        new_hand = self.hands[0] + cards
        new_hands = (new_hand, self.hands[1], self.hands[2], self.hands[3])
        return self._replace(hands=new_hands)
