from game import Game, Winner


def test_get_terminal():
    game = Game()

    game.board = [
        ['x', ' ', ' '],
        ['x', ' ', ' '],
        ['x', ' ', ' ']
    ]
    assert game.get_terminal() is Winner.CROSS

    game.board = [
        [' ', ' ', 'x'],
        [' ', ' ', 'x'],
        [' ', ' ', 'x']
    ]
    assert game.get_terminal() is Winner.CROSS

    game.board = [
        [' ', 'o', ' '],
        [' ', 'o', ' '],
        [' ', 'o', ' ']
    ]
    assert game.get_terminal() is Winner.CIRCLE

    game.board = [
        ['x', ' ', ' '],
        [' ', 'x', ' '],
        [' ', ' ', 'x']
    ]
    assert game.get_terminal() is Winner.CROSS

    game.board = [
        [' ', ' ', 'x'],
        [' ', 'x', ' '],
        ['x', ' ', ' ']
    ]
    assert game.get_terminal() is Winner.CROSS

    game.board = [
        [' ', ' ', 'x'],
        [' ', ' ', 'o'],
        [' ', ' ', 'x']
    ]
    assert game.get_terminal() is Winner.TIE


def test_possible_actions():
    game = Game()

    game.board = [
        [' ', 'o', 'x'],
        [' ', 'o', 'o'],
        ['x', ' ', 'x']
    ]
    assert game.get_possible_actions() == [[0, 0], [0, 1], [1, 2]]
