from typing import List

from cards import Card, Suit, Rank


def score_meld(hand: List[Card], trump: Suit) -> int:
    meld = len([card for card in hand if card == Card(Rank.NINE, trump)])
    for suit in Suit:
        ranks_in_suit = [card.rank for card in hand if card.suit == suit]
        if Rank.QUEEN in ranks_in_suit and Rank.KING in ranks_in_suit:
            meld += 2
    return meld
