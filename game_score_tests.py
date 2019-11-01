"""
Unit tests for game score class
"""

import unittest
from game_score import GameScore


class GameScoreTest(unittest.TestCase):
    def setUp(self):
        self.game_score = GameScore()

    def test_single_score(self):
        self.game_score.simple_score('test')
        print(self.game_score.scores['test'])
        self.assertIsInstance(self.game_score.scores['test'], dict)

    def test_add_score(self):
        self.game_score.simple_score('test')
        self.game_score.add(1, 'test')
        print(self.game_score.scores['test']['score'])

    def test_simple_highscore(self):
        self.game_score.simple_score_with_highscore('test')
        print(self.game_score.scores['test']['path'])

if __name__ == '__main__':
    unittest.main()