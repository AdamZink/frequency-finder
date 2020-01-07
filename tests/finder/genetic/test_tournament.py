import unittest
from finder.genetic.tournament import *
from finder.candidate import Candidate


def get_candidates():
    candidates = []
    for i in range(4):
        c = Candidate()
        c.set_too_high_score(i + 1)
        c.set_too_low_score(0)
        candidates.append(c)
    return candidates


def get_candidates_two_zeros():
    candidates = []
    for i in range(4):
        c = Candidate()
        if i > 1:
            c.set_too_high_score(3)
        else:
            c.set_too_high_score(0)
        c.set_too_low_score(0)
        candidates.append(c)
    return candidates


def get_candidates_all_zero():
    candidates = []
    for i in range(4):
        c = Candidate()
        c.set_too_high_score(0)
        c.set_too_low_score(0)
        candidates.append(c)
    return candidates


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

    def check_get_round_winner_indices(self, round_candidates, num_winners):
        indices = get_round_winner_indices(round_candidates, num_winners)
        self.assertEqual(num_winners, len(indices))

    def test_get_round_winner_indices_1(self):
        self.check_get_round_winner_indices(get_candidates(), 1)

    def test_get_round_winner_indices_2(self):
        self.check_get_round_winner_indices(get_candidates(), 2)

    def test_get_round_winner_indices_3(self):
        self.check_get_round_winner_indices(get_candidates(), 3)

    def test_get_round_winner_indices_4(self):
        self.check_get_round_winner_indices(get_candidates(), 4)

