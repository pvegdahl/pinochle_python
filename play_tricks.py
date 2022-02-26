from typing import NamedTuple, Tuple

from cards import Card
from utils import remove_cards_from_hand, InvalidCardRemoval


class InvalidPlay(Exception):
    pass


class PlayTricksState(NamedTuple):
    hands: Tuple[Tuple[Card, ...], ...]
    players: Tuple[str, str, str, str]
    next_player: str

    def play_card(self, player: str, card: Card) -> "PlayTricksState":
        if player != self.next_player:
            raise InvalidPlay(f"{player} cannot play on {self.next_player}'s turn")
        try:
            new_hands = (remove_cards_from_hand(self.hands[0], (card,)),) + self.hands[1:]
        except InvalidCardRemoval as e:
            raise InvalidPlay(f"{player} does not have a {card} in hand") from e

        return self._replace(hands=new_hands)
