from typing import Tuple

from cards import Card


class Trick:
    def __init__(self, cards: Tuple[Card, ...]):
        self._cards: Tuple[Card, ...] = cards

    def get_winner(self) -> Card:
        led_suit = self._cards[0].suit
        matching_cards = [card for card in self._cards if card.suit == led_suit]
        return max(matching_cards)
