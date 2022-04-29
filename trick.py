from typing import Tuple

from cards import Card, Suit


def get_trick_winner(cards: Tuple[Card, ...], trump: Suit) -> Card:
    trump_cards = [card for card in cards if card.suit == trump]
    if trump_cards:
        return max(trump_cards)

    matching_cards = [card for card in cards if card.suit == cards[0].suit]
    return max(matching_cards)


def get_trick_winner_index(cards: Tuple[Card, ...], trump: Suit) -> int:
    return cards.index(get_trick_winner(cards, trump))
