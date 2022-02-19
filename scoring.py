from typing import List

from cards import Card, Suit, Rank


def score_meld(hand: List[Card], trump: Suit) -> int:
    return len([card for card in hand if card == Card(Rank.NINE, trump)])
