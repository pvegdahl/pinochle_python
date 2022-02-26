from typing import Tuple

from cards import Card


class InvalidCardRemoval(Exception):
    pass


def remove_cards_from_hand(hand: Tuple[Card, ...], cards_to_remove: Tuple[Card, ...]) -> Tuple[Card, ...]:
    if not cards_to_remove:
        return hand
    try:
        index_to_remove = hand.index(cards_to_remove[0])
    except ValueError as e:
        raise InvalidCardRemoval(f"{cards_to_remove[0]} is not in hand")

    new_hand = hand[:index_to_remove] + hand[index_to_remove + 1 :]
    return remove_cards_from_hand(hand=new_hand, cards_to_remove=cards_to_remove[1:])
