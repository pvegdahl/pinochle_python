from typing import NamedTuple, Tuple

from cards import Card
from utils import remove_cards_from_hand, InvalidCardRemoval


class InvalidPlay(Exception):
    pass


class PlayTricksState(NamedTuple):
    hands: Tuple[Tuple[Card, ...], ...]
    players: Tuple[str, str, str, str]
    player_index: int

    def play_card(self, player: str, card: Card) -> "PlayTricksState":
        if player != self.current_player():
            raise InvalidPlay(f"{player} cannot play on {self.current_player()}'s turn")
        try:
            current_hand = self.hands[self.player_index]
            new_hand = remove_cards_from_hand(current_hand, (card,))
            new_hands = self.hands[: self.player_index] + (new_hand,) + self.hands[self.player_index :]
        except InvalidCardRemoval as e:
            raise InvalidPlay(f"{player} does not have a {card} in hand") from e

        return self._replace(hands=new_hands, player_index=self._incremented_player_index())

    def current_player(self) -> str:
        return self.players[self.player_index]

    def _incremented_player_index(self) -> int:
        return (self.player_index + 1) % 4
