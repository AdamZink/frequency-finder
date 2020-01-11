import unittest
from finder.genetic.tournament import *
from tests.finder.genetic.common import *


# Tests for tournament selection of fit candidates
class TestTournament(unittest.TestCase):

    def test_get_inverted_score(self):
        inverted = get_inverted_scores([1, 2, 3])
        self.assertEqual([3, 2, 1], inverted)

    def test_get_inverted_score_one_zero(self):
        inverted = get_inverted_scores([0, 1, 3])
        self.assertEqual([3, 2, 0], inverted)

    def test_get_inverted_score_all_zero(self):
        inverted = get_inverted_scores([0, 0, 0])
        self.assertEqual([0, 0, 0], inverted)

    def test_get_candidate_weights(self):
        weights = get_candidate_weights(get_candidates())
        self.assertEqual([0.4, 0.3, 0.2, 0.1], weights)

    def test_get_candidate_weights_two_zeros(self):
        weights = get_candidate_weights(get_candidates_two_zeros())
        self.assertEqual([0.5, 0.5, 0, 0], weights)

    def test_get_candidate_weights_all_zero(self):
        weights = get_candidate_weights(get_candidates_all_zero())
        self.assertEqual([0.25, 0.25, 0.25, 0.25], weights)

    def check_get_round_winner_indices(self, candidates, candidate_indices,  num_winners):
        indices = get_round_winner_indices(candidates, candidate_indices, num_winners)
        self.assertEqual(num_winners, len(indices))

    def test_get_round_winner_indices_1(self):
        self.check_get_round_winner_indices(get_candidates(), get_candidate_indices(), 1)

    def test_get_round_winner_indices_2(self):
        self.check_get_round_winner_indices(get_candidates(), get_candidate_indices(), 2)

    def test_get_round_winner_indices_3(self):
        self.check_get_round_winner_indices(get_candidates(), get_candidate_indices(), 3)

    def test_get_round_winner_indices_4(self):
        self.check_get_round_winner_indices(get_candidates(), get_candidate_indices(), 4)

    def test_select_tournament_winners_zero_elite(self):
        non_elite_surviving_indices = []
        select_tournament_winners(
            get_candidates(),
            get_candidate_indices(),
            non_elite_surviving_indices,
            2,
            0
        )
        # should be o2 non-elite because 0 elite + 2 non-elite fills the total of 2 surviving parents
        self.assertEqual(2, len(non_elite_surviving_indices))

    def test_select_tournament_winners_one_elite(self):
        non_elite_surviving_indices = []
        select_tournament_winners(
            get_candidates(),
            get_candidate_indices(),
            non_elite_surviving_indices,
            2,
            1
        )
        # should be only 1 non-elite because 1 elite + 1 non-elite fills the total of 2 surviving parents
        self.assertEqual(1, len(non_elite_surviving_indices))
