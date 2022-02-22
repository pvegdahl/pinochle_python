from typing import Tuple

import pytest

from bidding import BiddingState
from cards import CardDeck, Suit, Card, Rank
from pinochle_game import PinochleGame, GameState, IllegalPass


@pytest.fixture(scope="session")
def players() -> Tuple[str, str, str, str]:
    return "a", "b", "c", "d"


@pytest.fixture(scope="session")
def new_game(players: Tuple[str, str, str, str]) -> PinochleGame:
    return PinochleGame.new_game(players=players)


@pytest.fixture(scope="session")
def game_bidding_complete(players: Tuple[str, str, str, str]) -> PinochleGame:
    return PinochleGame(
        state=GameState.BIDDING,
        players=players,
        hands=CardDeck.deal(),
        bidding=BiddingState(active_players=("a",), current_bid=25),
        trump=None,
    )


@pytest.fixture(scope="session")
def game_ready_to_pass(players: Tuple[str, str, str, str]) -> PinochleGame:
    # For simplicity, we're setting up the hands so that player A has all clubs, B diamonds, C hearts, and D spades
    sorted_cards = tuple(sorted(CardDeck.all_cards()))
    return PinochleGame(
        state=GameState.PASSING_TO_BID_WINNER,
        players=players,
        hands=(
            sorted_cards[:12],
            sorted_cards[12:24],
            sorted_cards[24:36],
            sorted_cards[36:],
        ),
        bidding=BiddingState(active_players=("a",), current_bid=25),
        trump=Suit.CLUBS,
    )


@pytest.fixture(scope="session")
def passed_cards() -> Tuple[Card, Card, Card, Card]:
    return (
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
    )


def test_new_game_state_is_bidding(new_game) -> None:
    assert new_game.state == GameState.BIDDING
    assert new_game.bidding is not None


def test_new_game_deals_cards_to_players(new_game) -> None:
    assert len(new_game.hands) == 4


def test_no_trump_at_start(new_game) -> None:
    assert new_game.trump is None


@pytest.mark.parametrize("trump_suit", [suit for suit in Suit])
def test_set_trump_does_what_it_says(
    trump_suit: Suit, game_bidding_complete: PinochleGame
) -> None:
    game = game_bidding_complete.select_trump(player="a", trump=trump_suit)
    assert game.trump == trump_suit


def test_set_trump_advances_state_to_passing(
    game_bidding_complete: PinochleGame,
) -> None:
    game = game_bidding_complete.select_trump(player="a", trump=Suit.DIAMONDS)
    assert game.state == GameState.PASSING_TO_BID_WINNER


def test_pass_to_winner_creates_correct_winner_hand(
    game_ready_to_pass: PinochleGame, passed_cards: Tuple[Card, Card, Card, Card]
) -> None:
    game = game_ready_to_pass.pass_cards(
        source="c", destination="a", cards=passed_cards
    )

    assert sorted(game.hands[0]) == sorted(
        tuple(Card(rank, Suit.CLUBS) for rank in Rank) * 2
        + (
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.HEARTS),
        )
    )


def test_pass_to_winner_creates_correct_partner_hand(
    game_ready_to_pass: PinochleGame, passed_cards: Tuple[Card, Card, Card, Card]
) -> None:
    game = game_ready_to_pass.pass_cards(
        source="c", destination="a", cards=passed_cards
    )

    assert sorted(game.hands[2]) == sorted(
        (
            Card(Rank.TEN, Suit.HEARTS),
            Card(Rank.TEN, Suit.HEARTS),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.HEARTS),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.NINE, Suit.HEARTS),
            Card(Rank.NINE, Suit.HEARTS),
        )
    )


def test_must_have_passed_cards(
        game_ready_to_pass: PinochleGame
) -> None:
    passed_cards = (
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.SPADES),
    )

    with pytest.raises(IllegalPass) as e:
        game_ready_to_pass.pass_cards(
            source="c", destination="a", cards=passed_cards
        )
    assert e.value.args[0] == "Jack of Diamonds is not in hand to pass"


@pytest.mark.parametrize("source, destination, suit_to_pass", [
    ("a", "a", Suit.CLUBS),
    ("a", "b", Suit.CLUBS),
    ("a", "c", Suit.CLUBS),
    ("a", "d", Suit.CLUBS),
    ("b", "a", Suit.DIAMONDS),
    ("b", "b", Suit.DIAMONDS),
    ("b", "c", Suit.DIAMONDS),
    ("b", "d", Suit.DIAMONDS),
    ("c", "b", Suit.HEARTS),
    ("c", "c", Suit.HEARTS),
    ("c", "d", Suit.HEARTS),
    ("d", "a", Suit.SPADES),
    ("d", "b", Suit.SPADES),
    ("d", "c", Suit.SPADES),
    ("d", "d", Suit.SPADES),
])
def test_initial_pass_must_be_from_partner_to_winner(source, destination, suit_to_pass, game_ready_to_pass: PinochleGame) -> None:
    cards_to_pass = (Card(Rank.ACE, suit_to_pass), Card(Rank.TEN, suit_to_pass)) * 2
    with pytest.raises(IllegalPass) as e:
        game_ready_to_pass.pass_cards(source=source, destination=destination, cards=cards_to_pass)
    assert e.value.args[0] == "The only legal pass is from c to a"




# Support passing between other players
# Make sure the pass is a legal pass
#  - In the correct stage of game
#  - From partner to winner
#  - Then from winner to partner
#  - Exactly four cards

