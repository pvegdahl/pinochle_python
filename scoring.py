from typing import List

from cards import Card, Suit, Rank


def score_meld(hand: List[Card], trump: Suit) -> int:
    meld = count_nines_of_trump(hand, trump)
    for suit in Suit:
        meld += count_marriages_in_suit(hand, suit) * 2
    return meld


def count_nines_of_trump(hand: List[Card], trump: Suit) -> int:
    return len([card for card in hand if card == Card(Rank.NINE, trump)])


def count_marriages_in_suit(hand: List[Card], suit: Suit) -> int:
    queen_count = len([card for card in hand if card.rank == Rank.QUEEN and card.suit == suit])
    king_count = len([card for card in hand if card.rank == Rank.KING and card.suit == suit])
    if queen_count and king_count:
        return int((queen_count + king_count) / 2)
    return 0

