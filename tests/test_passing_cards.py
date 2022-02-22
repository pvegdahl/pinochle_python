from typing import Tuple

import pytest

from cards import CardDeck, Card, Suit, Rank
from passing_cards import PassingCards


def bid_winner() -> str:
    return "a"


def partner() -> str:
    return "c"


@pytest.fixture(scope="session")
def all_spades() -> Tuple[Card, ...]:
    return tuple(Card(rank, Suit.SPADES) for rank in Rank) * 2


@pytest.fixture(scope="session")
def all_diamonds() -> Tuple[Card, ...]:
    return tuple(Card(rank, Suit.DIAMONDS) for rank in Rank) * 2


@pytest.fixture(scope="session")
def passing_cards(all_spades, all_diamonds) -> PassingCards:
    # For simplicity, we're setting up the hands so that the winner has all spades, and the partner has all diamonds
    return PassingCards(bid_winner=bid_winner(), partner=partner(), bid_winner_hand=all_spades, partner_hand=all_diamonds)


@pytest.fixture(scope="session")
def partner_passed_cards() -> Tuple[Card, Card, Card, Card]:
    return (
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
    )


def test_pass_to_winner_creates_correct_winner_hand(passing_cards, partner_passed_cards, all_spades) -> None:
    updated = passing_cards.pass_cards(source=partner(), destination=bid_winner(), cards=partner_passed_cards)

    assert sorted(updated.bid_winner_hand) == sorted(
        all_spades
        + (
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.DIAMONDS),
        )
    )


def test_pass_to_winner_creates_correct_partner_hand(passing_cards, partner_passed_cards) -> None:
    updated = passing_cards.pass_cards(source=partner(), destination=bid_winner(), cards=partner_passed_cards)

    assert sorted(updated.partner_hand) == sorted(
        (
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.DIAMONDS),
        )
    )


# def test_must_have_passed_cards(
#         game_ready_to_pass: PinochleGame
# ) -> None:
#     passed_cards = (
#         Card(Rank.ACE, Suit.HEARTS),
#         Card(Rank.ACE, Suit.HEARTS),
#         Card(Rank.JACK, Suit.DIAMONDS),
#         Card(Rank.QUEEN, Suit.SPADES),
#     )
#
#     with pytest.raises(IllegalPass) as e:
#         game_ready_to_pass.pass_cards(
#             source="c", destination="a", cards=passed_cards
#         )
#     assert e.value.args[0] == "Jack of Diamonds is not in hand to pass"
#
#
# @pytest.mark.parametrize("source, destination, suit_to_pass", [
#     ("a", "a", Suit.CLUBS),
#     ("a", "b", Suit.CLUBS),
#     ("a", "c", Suit.CLUBS),
#     ("a", "d", Suit.CLUBS),
#     ("b", "a", Suit.DIAMONDS),
#     ("b", "b", Suit.DIAMONDS),
#     ("b", "c", Suit.DIAMONDS),
#     ("b", "d", Suit.DIAMONDS),
#     ("c", "b", Suit.HEARTS),
#     ("c", "c", Suit.HEARTS),
#     ("c", "d", Suit.HEARTS),
#     ("d", "a", Suit.SPADES),
#     ("d", "b", Suit.SPADES),
#     ("d", "c", Suit.SPADES),
#     ("d", "d", Suit.SPADES),
# ])
# def test_initial_pass_must_be_from_partner_to_winner(source, destination, suit_to_pass, game_ready_to_pass: PinochleGame) -> None:
#     cards_to_pass = (Card(Rank.ACE, suit_to_pass), Card(Rank.TEN, suit_to_pass)) * 2
#     with pytest.raises(IllegalPass) as e:
#         game_ready_to_pass.pass_cards(source=source, destination=destination, cards=cards_to_pass)
#     assert e.value.args[0] == "The only legal pass is from c to a"
#
#
# def test_no_pass_legal_before_passing_phase(game_bidding_complete: PinochleGame, passed_cards) -> None:
#     with pytest.raises(IllegalPass) as e:
#         game_bidding_complete.pass_cards(source="c", destination="a", cards=passed_cards)
#     assert e.value.args[0] == "You cannot pass cards in the Bidding phase"
#
#
# @pytest.mark.parametrize("num_cards_to_pass", [0, 1, 2, 3, 5, 6])
# def test_pass_must_be_exactly_four_cards(game_ready_to_pass: PinochleGame, num_cards_to_pass) -> None:
#     passed_cards = game_ready_to_pass.hands[2][:num_cards_to_pass]
#     with pytest.raises(IllegalPass) as e:
#         game_ready_to_pass.pass_cards(source="c", destination="a", cards=passed_cards)
#     assert e.value.args[0] == f"Passes must be exactly 4 cards, not {num_cards_to_pass}"
#
#
#
#
#
# # Support passing between other winning bidders
# # Make sure the pass is a legal pass
# #  - Then from winner to partner
# #  - Exactly four cards
#
