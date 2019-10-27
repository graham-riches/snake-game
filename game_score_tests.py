"""
Unit tests for game score class
"""

import unittest
from game_score import GameScore


class GameScoreTest(unittest.TestCase):
    def setUp(self):
        self.game_score = GameScore()

    def test_single_score(self):
        self.game_score.new_simple_score('test')
        print(self.game_score.scores['test'])
        self.assertIsInstance(self.game_score.scores['test'], dict)

    

if __name__ == '__main__':
    unittest.main()