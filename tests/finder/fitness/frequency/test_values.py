import unittest
from finder.fitness.frequency.values import *
from tests.finder.fitness.constants import *


# Tests to evaluate whether the correct frequency values are in the audio graph
class TestValues(unittest.TestCase):

    def test_get_frequency_tuple_too_low_score(self):
        # score should be 1 to indicate guess frequency is too low
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_tuple_too_low_score(ONE_AT_1, ONE_AT_0, axis=1)
        self.assertEqual(1, score)

    def test_get_frequency_tuple_too_low_score_zero(self):
        # score should be zero to indicate frequency is NOT too low
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_tuple_too_low_score(ONE_AT_0, ONE_AT_1, axis=1)
        self.assertEqual(0, score)

    def test_get_frequency_tuple_too_high_score(self):
        # score should be 1 to indicate guess frequency is too high
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_tuple_too_high_score(ONE_AT_0, ONE_AT_1, axis=1)
        self.assertEqual(1, score)

    def test_get_frequency_tuple_too_high_score_zero(self):
        # score should be zero to indicate frequency is NOT too high
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_tuple_too_high_score(ONE_AT_1, ONE_AT_0, axis=1)
        self.assertEqual(0, score)

    def test_get_frequency_tuple_too_low_score_with_higher(self):
        # score should be 1 to indicate one of the guess frequencies is too low, but not the other frequency
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_tuple_too_low_score(ONE_AT_0_AND_3, ONE_AT_1_AND_2, axis=1)
        self.assertEqual(1, score)

    def test_get_frequency_tuple_too_high_score_with_lower(self):
        # score should be 1 to indicate one of the guess frequencies is too high, but not the other frequency
        # i.e. sign of score reflects the adjustment direction
        score = get_frequency_tuple_too_high_score(ONE_AT_0_AND_3, ONE_AT_1_AND_2, axis=1)
        self.assertEqual(1, score)
