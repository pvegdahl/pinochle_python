from enum import Enum
from typing import NamedTuple, Tuple, Optional

from bidding import BiddingState
from cards import Card, CardDeck, Suit


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

    def pass_cards(
        self, source: str, destination: str, cards: Tuple[Card, Card, Card, Card]
    ) -> "PinochleGame":
        self._validate_legality_of_pass(source=source, destination=destination, cards=cards)

        new_hand_0 = self.hands[0] + cards
        new_hand_2 = self._remove_cards_from_hand(
            initial_hand=self.hands[2], cards_to_remove=cards
        )
        new_hands = (new_hand_0, self.hands[1], new_hand_2, self.hands[3])
        return self._replace(hands=new_hands)

    def _validate_legality_of_pass(self, source: str, destination: str, cards: Tuple[Card, Card, Card, Card]):
        if len(cards) != 4:
            raise IllegalPass(f"Passes must be exactly 4 cards, not {len(cards)}")
        if self.state != GameState.PASSING_TO_BID_WINNER:
            raise IllegalPass(f"You cannot pass cards in the {self.state} phase")

        if source != "c" or destination != "a":
            raise IllegalPass(f"The only legal pass is from {self._get_bid_winner_partner()} to {self._get_bid_winner()}")

    def _get_bid_winner(self) -> str:
        return self.bidding.get_winner()

    def _get_bid_winner_partner(self) -> str:
        bid_winner_index = self.players.index(self._get_bid_winner())
        partner_index = (bid_winner_index + 2) % 4
        return self.players[partner_index]

    @classmethod
    def _remove_cards_from_hand(
        cls, initial_hand: Tuple[Card, ...], cards_to_remove: Tuple[Card, ...]
    ) -> Tuple[Card, ...]:
        if not cards_to_remove:
            return initial_hand
        try:
            index_to_remove = initial_hand.index(cards_to_remove[0])
        except ValueError as e:
            raise IllegalPass(f"{cards_to_remove[0]} is not in hand to pass")

        new_hand = initial_hand[:index_to_remove] + initial_hand[index_to_remove + 1:]
        return cls._remove_cards_from_hand(
            initial_hand=new_hand, cards_to_remove=cards_to_remove[1:]
        )
