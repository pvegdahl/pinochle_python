from typing import NamedTuple, Tuple

from cards import Card


class IllegalPass(Exception):
    pass


class PassingCards(NamedTuple):
    bid_winner: str
    partner: str
    bid_winner_hand: Tuple[Card, ...]
    partner_hand: Tuple[Card, ...]

    def pass_cards(
            self, source: str, destination: str, cards: Tuple[Card, Card, Card, Card]
    ) -> "PassingCards":
        # self._validate_legality_of_pass(source=source, destination=destination, cards=cards)
        new_winner_hand = self.bid_winner_hand + cards
        new_partner_card = self._remove_cards_from_hand(initial_hand=self.partner_hand, cards_to_remove=cards)
        return self._replace(bid_winner_hand=new_winner_hand, partner_hand=new_partner_card)

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

