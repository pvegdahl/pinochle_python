from typing import Tuple

import pytest

from cards import Card, Suit, Rank
from passing_cards import PassingCards, IllegalPass
from utils import InvalidCardRemoval


def bid_winner() -> str:
    return "bid_winner"


def partner() -> str:
    return "partner"


@pytest.fixture(scope="session")
def passing_cards_state(all_spades, all_diamonds) -> PassingCards:
    # For simplicity, we're setting up the hands so that the winner has all spades, and the partner has all diamonds
    return PassingCards(
        bid_winner=bid_winner(),
        partner=partner(),
        bid_winner_hand=all_spades,
        partner_hand=all_diamonds,
    )


@pytest.fixture(scope="session")
def partner_passed_cards() -> Tuple[Card, Card, Card, Card]:
    return (
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
    )


@pytest.fixture(scope="session")
def bid_winner_passed_cards() -> Tuple[Card, Card, Card, Card]:
    return (
        Card(Rank.NINE, Suit.SPADES),
        Card(Rank.JACK, Suit.SPADES),
    ) * 2


def test_pass_to_winner_creates_correct_winner_hand(passing_cards_state, partner_passed_cards, all_spades) -> None:
    updated = passing_cards_state.pass_cards(source=partner(), destination=bid_winner(), cards=partner_passed_cards)

    assert sorted(updated.bid_winner_hand) == sorted(
        all_spades
        + (
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.DIAMONDS),
        )
    )


def test_pass_to_winner_creates_correct_partner_hand(passing_cards_state, partner_passed_cards) -> None:
    updated = passing_cards_state.pass_cards(source=partner(), destination=bid_winner(), cards=partner_passed_cards)

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


def test_passee_must_have_passed_cards(passing_cards_state) -> None:
    passed_cards = (
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.SPADES),
    )

    with pytest.raises(InvalidCardRemoval) as e:
        passing_cards_state.pass_cards(source=partner(), destination=bid_winner(), cards=passed_cards)
    assert e.value.args[0] == "Jack of Hearts is not in hand"


@pytest.mark.parametrize(
    "source, destination",
    [
        (bid_winner(), bid_winner()),
        (partner(), partner()),
        (partner(), "other"),
        ("other", bid_winner()),
    ],
)
def test_reject_passes_not_between_the_partners(source, destination, passing_cards_state):
    cards_to_pass = (Card(Rank.ACE, Suit.DIAMONDS), Card(Rank.JACK, Suit.DIAMONDS)) * 2
    with pytest.raises(IllegalPass) as e:
        passing_cards_state.pass_cards(source=source, destination=destination, cards=cards_to_pass)
    assert e.value.args[0] == f"Illegal pass from {source} to {destination}"


@pytest.mark.parametrize("num_cards_to_pass", [0, 1, 2, 3, 5, 6])
def test_pass_must_be_exactly_four_cards(passing_cards_state, num_cards_to_pass) -> None:
    passed_cards = passing_cards_state.partner_hand[:num_cards_to_pass]
    with pytest.raises(IllegalPass) as e:
        passing_cards_state.pass_cards(source=partner(), destination=bid_winner(), cards=passed_cards)
    assert e.value.args[0] == f"Passes must be exactly 4 cards, not {num_cards_to_pass}"


def test_no_winner_to_partner_for_first_pass(passing_cards_state, bid_winner_passed_cards):
    with pytest.raises(IllegalPass) as e:
        passing_cards_state.pass_cards(source=bid_winner(), destination=partner(), cards=bid_winner_passed_cards)
    assert e.value.args[0] == "bid_winner must have 16 cards in hand to pass, has 12"


def test_second_pass_from_bid_winner_back_to_partner(
    passing_cards_state, partner_passed_cards, bid_winner_passed_cards
):
    first_pass = passing_cards_state.pass_cards(source=partner(), destination=bid_winner(), cards=partner_passed_cards)
    second_pass = first_pass.pass_cards(source=bid_winner(), destination=partner(), cards=bid_winner_passed_cards)
    assert sorted(second_pass.bid_winner_hand) == sorted(
        (
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.DIAMONDS),
        ),
    )

    assert sorted(second_pass.partner_hand) == sorted(
        (
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.SPADES),
            Card(Rank.JACK, Suit.SPADES),
            Card(Rank.NINE, Suit.SPADES),
            Card(Rank.NINE, Suit.SPADES),
        )
    )
