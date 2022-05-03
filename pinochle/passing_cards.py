from enum import Enum
from typing import NamedTuple, Tuple

from pinochle.cards import Card
from pinochle.utils import remove_cards_from_hand


class IllegalPass(Exception):
    pass


class PassDirection(Enum):
    PARTNER_TO_BID_WINNER = "PartnerToBidWinner"
    BID_WINNER_TO_PARTNER = "BidWinnerToPartner"


class PassingCards(NamedTuple):
    bid_winner: str
    partner: str
    bid_winner_hand: Tuple[Card, ...]
    partner_hand: Tuple[Card, ...]

    def pass_cards(self, source: str, destination: str, cards: Tuple[Card, Card, Card, Card]) -> "PassingCards":
        pass_direction = self._get_pass_direction(source=source, destination=destination)
        self._validate_legality_of_pass(pass_direction=pass_direction, cards=cards)
        if pass_direction == PassDirection.BID_WINNER_TO_PARTNER:
            new_winner_hand = self.bid_winner_hand + cards
            new_partner_hand = remove_cards_from_hand(hand=self.partner_hand, cards_to_remove=cards)
        else:
            new_winner_hand = remove_cards_from_hand(hand=self.bid_winner_hand, cards_to_remove=cards)
            new_partner_hand = self.partner_hand + cards
        return self._replace(bid_winner_hand=new_winner_hand, partner_hand=new_partner_hand)

    def _get_pass_direction(self, source: str, destination: str) -> PassDirection:
        if source == self.bid_winner and destination == self.partner:
            return PassDirection.PARTNER_TO_BID_WINNER
        elif source == self.partner and destination == self.bid_winner:
            return PassDirection.BID_WINNER_TO_PARTNER
        else:
            raise IllegalPass(f"Illegal pass from {source} to {destination}")

    def _validate_legality_of_pass(self, pass_direction: PassDirection, cards: Tuple[Card, Card, Card, Card]):
        if pass_direction == PassDirection.BID_WINNER_TO_PARTNER:
            self._validate_hand_size(player=self.bid_winner, hand=self.bid_winner_hand, target_size=12)
            self._validate_hand_size(player=self.partner, hand=self.partner_hand, target_size=12)
        else:
            self._validate_hand_size(player=self.bid_winner, hand=self.bid_winner_hand, target_size=16)
            self._validate_hand_size(player=self.partner, hand=self.partner_hand, target_size=8)

        self._validate_size_of_pass(cards)

    @staticmethod
    def _validate_hand_size(player: str, hand: Tuple[Card, ...], target_size: int) -> None:
        if len(hand) != target_size:
            raise IllegalPass(f"{player} must have {target_size} cards in hand to pass, has {len(hand)}")

    @staticmethod
    def _validate_size_of_pass(cards: Tuple[Card, ...]):
        if len(cards) != 4:
            raise IllegalPass(f"Passes must be exactly 4 cards, not {len(cards)}")
