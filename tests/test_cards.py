import pytest

from cards import Rank


@pytest.mark.parametrize("lower, higher", [
    (Rank.NINE, Rank.JACK),
    (Rank.NINE, Rank.QUEEN),
    (Rank.NINE, Rank.KING),
    (Rank.NINE, Rank.TEN),
    (Rank.NINE, Rank.ACE),
    (Rank.JACK, Rank.QUEEN),
    (Rank.JACK, Rank.KING),
    (Rank.JACK, Rank.TEN),
    (Rank.JACK, Rank.ACE),
    (Rank.QUEEN, Rank.KING),
    (Rank.QUEEN, Rank.TEN),
    (Rank.QUEEN, Rank.ACE),
    (Rank.KING, Rank.TEN),
    (Rank.KING, Rank.ACE),
    (Rank.TEN, Rank.ACE),
])
def test_rank_ordering(lower, higher):
    assert lower < higher
    assert not lower > higher

