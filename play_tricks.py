from typing import NamedTuple, Tuple

from cards import Card, Suit
from utils import remove_cards_from_hand, InvalidCardRemoval


class InvalidPlay(Exception):
    pass


class PlayTricksState(NamedTuple):
    hands: Tuple[Tuple[Card, ...], ...]
    players: Tuple[str, str, str, str]
    player_index: int
    current_trick: Tuple[Card, ...] = tuple()

    def play_card(self, player: str, card: Card) -> "PlayTricksState":
        if player != self.current_player():
            raise InvalidPlay(f"{player} cannot play on {self.current_player()}'s turn")
        self._validate_chosen_card(card=card)
        try:
            new_hand = remove_cards_from_hand(self._current_player_hand(), (card,))
            new_hands = self.hands[: self.player_index] + (new_hand,) + self.hands[self.player_index+1 :]
        except InvalidCardRemoval as e:
            raise InvalidPlay(f"{player} does not have a {card} in hand") from e

        return self._replace(hands=new_hands, player_index=self._incremented_player_index(), current_trick=(self.current_trick + (card,)))

    def current_player(self) -> str:
        return self.players[self.player_index]

    def _current_player_hand(self) -> Tuple[Card, ...]:
        return self.hands[self.player_index]

    def _incremented_player_index(self) -> int:
        return (self.player_index + 1) % 4

    def _validate_chosen_card(self, card: Card) -> None:
        if self._is_beginning_of_trick():
            return

        self._validate_match_suit_if_possible(card)

    def _is_beginning_of_trick(self):
        return len(self.current_trick) == 0

    def _validate_match_suit_if_possible(self, card: Card) -> None:
        suit_matches = card.suit == self.current_trick[0].suit
        if self._has_suit_in_hand() and not suit_matches:
            raise InvalidPlay("Must play on suit if possible")

    def _has_suit_in_hand(self) -> bool:
        return self._suit_of_current_trick() in (card.suit for card in self._current_player_hand())

    def _suit_of_current_trick(self) -> Suit:
        return self.current_trick[0].suit