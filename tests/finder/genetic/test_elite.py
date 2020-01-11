import unittest
from finder.genetic.elite import *
from tests.finder.genetic.common import *


# Tests for selection of elite candidates
class TestTournament(unittest.TestCase):

    def test_get_elite_indices_1(self):
        indices = get_elite_indices(get_candidates(), 1)
        self.assertEqual(1, len(indices))
        self.assertIn(0, indices)

    def test_get_elite_indices_4(self):
        indices = get_elite_indices(get_candidates(), 4)
        self.assertEqual(4, len(indices))
        self.assertIn(0, indices)
        self.assertIn(1, indices)
        self.assertIn(2, indices)
        self.assertIn(3, indices)
