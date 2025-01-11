from decision_tree_logic import get_score_board
from game import Winner
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def test_cross_wins_row():
    board = [
        ['x', 'x', 'x'],
        ['o', ' ', 'o'],
        [' ', ' ', ' ']
    ]
    assert(get_score_board(board), Winner.CROSS.value)


def test_circle_wins_column():
    board = [
        ['o', 'x', ' '],
        ['o', 'x', ' '],
        ['o', ' ', 'x']
    ]
    assert(get_score_board(board), Winner.CIRCLE.value)


def test_cross_wins_diagonal():
    board = [
        ['x', 'o', ' '],
        ['o', 'x', ' '],
        [' ', ' ', 'x']
    ]
    assert(get_score_board(board), Winner.CROSS.value)


def test_circle_wins_counter_diagonal():
    board = [
        ['x', ' ', 'o'],
        ['x', 'o', ' '],
        ['o', ' ', 'x']
    ]
    assert(get_score_board(board), Winner.CIRCLE.value)


def test_crosses_pressure():
    board = [
        ['x', 'x', ' '],
        ['o', 'o', ' '],
        [' ', ' ', ' ']
    ]
    # self.assertGreater(get_score_board(board), 1.0)


def test_circles_pressure(self):
    board = [
        ['o', 'o', ' '],
        ['x', 'x', ' '],
        [' ', ' ', ' ']
    ]
    # self.assertLess(get_score_board(board), 1.0)


def test_tie(self):
    board = [
        ['x', 'o', 'x'],
        ['o', 'x', 'o'],
        ['o', 'x', 'o']
    ]
    assert(get_score_board(board), 1.0)

