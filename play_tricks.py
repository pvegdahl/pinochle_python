from typing import NamedTuple, Tuple, Set

from cards import Card, Suit
from utils import remove_cards_from_hand, InvalidCardRemoval


class InvalidPlay(Exception):
    pass


class PlayTricksState(NamedTuple):
    hands: Tuple[Tuple[Card, ...], ...]
    players: Tuple[str, str, str, str]
    player_index: int
    trump: Suit
    current_trick: Tuple[Card, ...] = tuple()

    def play_card(self, player: str, card: Card) -> "PlayTricksState":
        if player != self.current_player():
            raise InvalidPlay(f"{player} cannot play on {self.current_player()}'s turn")
        self._validate_chosen_card(card=card)
        try:
            new_hand = remove_cards_from_hand(self._current_player_hand(), (card,))
            new_hands = self.hands[: self.player_index] + (new_hand,) + self.hands[self.player_index + 1 :]
        except InvalidCardRemoval as e:
            raise InvalidPlay(f"{player} does not have a {card} in hand") from e

        return self._replace(
            hands=new_hands, player_index=self._incremented_player_index(), current_trick=(self.current_trick + (card,))
        )

    def current_player(self) -> str:
        return self.players[self.player_index]

    def _current_player_hand(self) -> Tuple[Card, ...]:
        return self.hands[self.player_index]

    def _incremented_player_index(self) -> int:
        return (self.player_index + 1) % 4

    def _validate_chosen_card(self, card: Card) -> None:
        if card not in self._get_valid_cards_to_play():
            raise InvalidPlay("Invalid card played")

    def _get_valid_cards_to_play(self) -> Set[Card]:
        if self._is_beginning_of_trick():
            return set(self._current_player_hand())

        # (1) filter to either the current suit or trump or just return everything
        if self._has_suit_in_hand(self._suit_of_current_trick()):
            matching_cards = set(card for card in self._current_player_hand() if card.suit == self._suit_of_current_trick())
        elif self._has_suit_in_hand(self.trump):
            matching_cards = set(card for card in self._current_player_hand() if card.suit == self.trump)
        else:
            return set(self._current_player_hand())

        # (2) filter to only winning cards
        winning_cards = set(filter(lambda card: card > self._current_winning_card(), matching_cards))

        # (3) if there are no winning cards, then return all matching cards
        return winning_cards if winning_cards else matching_cards

    def _is_beginning_of_trick(self):
        return len(self.current_trick) == 0

    def _has_suit_in_hand(self, suit: Suit) -> bool:
        return suit in {card.suit for card in self._current_player_hand()}

    def _suit_of_current_trick(self) -> Suit:
        return self.current_trick[0].suit

    def _current_winning_card(self) -> Card:
        result = self.current_trick[0]
        for card in self.current_trick[1:]:
            if self._second_card_wins(result, card):
                result = card
        return result

    def _second_card_wins(self, card0: Card, card1: Card) -> bool:
        if card0.suit == card1.suit:
            return card1.rank > card0.rank
        else:
            return card1.suit == self.trump
