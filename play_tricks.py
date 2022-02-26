from typing import NamedTuple, Tuple

from cards import Card
from utils import remove_cards_from_hand


class PlayTricksState(NamedTuple):
    hands: Tuple[Tuple[Card, ...], ...]

    def play_card(self, player: str, card: Card) -> "PlayTricksState":
        new_hands = (remove_cards_from_hand(self.hands[0], (card,)),) + self.hands[1:]
        return self._replace(hands=new_hands)
