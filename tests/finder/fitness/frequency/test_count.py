import unittest
import numpy as np
from finder.fitness.frequency.count import *
from tests.finder.fitness.constants import *


# Tests to evaluate whether the correct number of frequencies are in the audio graph
class TestCount(unittest.TestCase):

    def test_get_frequency_count_score_negative(self):
        # score should be negative to indicate too many frequencies
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_count_score(FOUR_ZEROS, ONE_AT_0)
        self.assertLess(score, 0)

    def test_get_frequency_count_score_positive(self):
        # score should be positive to indicate no frequencies
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_count_score(ONE_AT_0, FOUR_ZEROS)
        self.assertGreater(score, 0)

    def test_get_frequency_count_score_equal_same_freq(self):
        # score should be equal to indicate same number of frequencies
        score = get_frequency_count_score(ONE_AT_0, ONE_AT_0)
        self.assertEqual(score, 0)

    def test_get_frequency_count_score_equal_diff_freq(self):
        # score should be equal to indicate same number of frequencies (even if frequency values are different)
        score = get_frequency_count_score(ONE_AT_0, ONE_AT_3)
        self.assertEqual(score, 0)

    def test_get_frequency_count_score_positive_multiple(self):
        # score should be positive to indicate not enough frequencies
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_count_score(ONE_AT_0_AND_1, ONE_AT_2)
        self.assertGreater(score, 0)

    def test_get_frequency_count_score_positive_middle(self):
        # score should be positive to indicate not enough frequencies (even with higher and lower frequency values)
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_count_score(ONE_AT_0_AND_2, ONE_AT_1)
        self.assertGreater(score, 0)

    def test_get_frequency_count_score_positive_highest_index(self):
        # score should be equal to indicate same number of frequencies
        score = get_frequency_count_score(ONE_AT_2, ONE_AT_3)
        self.assertEqual(score, 0)


if __name__ == '__main__':
    unittest.main()
