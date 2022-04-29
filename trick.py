from functools import reduce
from typing import Tuple

from cards import Card, Suit


def get_trick_winning_card(cards: Tuple[Card, ...], trump: Suit) -> Card:
    return reduce(lambda card0, card1: card1 if second_card_wins(card0, card1, trump) else card0, cards[1:], cards[0])


def get_trick_winner_index(cards: Tuple[Card, ...], trump: Suit) -> int:
    return cards.index(get_trick_winning_card(cards, trump))


def second_card_wins(card0: Card, card1: Card, trump: Suit) -> bool:
    if card0.suit == card1.suit:
        return card1.rank > card0.rank
    else:
        return card1.suit == trump
