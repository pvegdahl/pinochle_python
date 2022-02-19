from typing import List

from cards import Card, Suit, Rank


def score_meld(hand: List[Card], trump: Suit) -> int:
    meld = len([card for card in hand if card == Card(Rank.NINE, trump)])
    for suit in Suit:
        ranks_in_suit = [card.rank for card in hand if card.suit == suit]
        queen_count = len([rank for rank in ranks_in_suit if rank == Rank.QUEEN])
        king_count = len([rank for rank in ranks_in_suit if rank == Rank.KING])
        if queen_count and king_count:
            if queen_count + king_count == 4:
                meld += 4
            else:
                meld += 2
    return meld
