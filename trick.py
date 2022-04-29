from typing import Tuple

from cards import Card


def get_trick_winner(cards: Tuple[Card, ...]) -> Card:
    led_suit = cards[0].suit
    matching_cards = [card for card in cards if card.suit == led_suit]
    return max(matching_cards)

