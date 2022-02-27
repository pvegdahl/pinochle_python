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
            current_hand = self.hands[self._next_player_index()]
            new_hand = remove_cards_from_hand(current_hand, (card,))
            new_hands = self.hands[: self._next_player_index()] + (new_hand,) + self.hands[self._next_player_index() :]
        except InvalidCardRemoval as e:
            raise InvalidPlay(f"{player} does not have a {card} in hand") from e

        return self._replace(hands=new_hands)

    def _next_player_index(self) -> int:
        return self.players.index(self.next_player)
