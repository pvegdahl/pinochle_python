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
        new_hand_0 = self.hands[0] + cards
        new_hand_2 = self._remove_cards_from_hand(
            initial_hand=self.hands[2], cards_to_remove=cards
        )
        new_hands = (new_hand_0, self.hands[1], new_hand_2, self.hands[3])
        return self._replace(hands=new_hands)

    @classmethod
    def _remove_cards_from_hand(
        cls, initial_hand: Tuple[Card, ...], cards_to_remove: Tuple[Card, ...]
    ) -> Tuple[Card, ...]:
        if not cards_to_remove:
            return initial_hand
        index_to_remove = initial_hand.index(cards_to_remove[0])
        new_hand = initial_hand[:index_to_remove] + initial_hand[index_to_remove + 1 :]
        return cls._remove_cards_from_hand(
            initial_hand=new_hand, cards_to_remove=cards_to_remove[1:]
        )
