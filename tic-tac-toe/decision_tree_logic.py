import curses
from enum import Enum
import random


class Node:
    def __init__(self, board_state, is_min_player, action, iteration: int):
        self.board_state: list[list[str]] = board_state
        self.is_min_player: bool = is_min_player
        self.action: Action = action
        self.iteration = iteration

        self.children: list[Node] = []
        self.parent: Node | None = None
        self.score: int | None = None

    def __str__(self):
        return f"Node(children: {self.children}, score: {self.score}, is_min_player: {self.is_min_player}, action: {self.action})"

    def __repr__(self):
        return self.__str__()


class Action:
    def __init__(self, x: int, y: int, is_min_player: bool):
        self.x = x
        self.y = y
        self.is_min_player = is_min_player

    def __str__(self):
        return f"Action(x: {self.x}, y: {self.y}, is_min_player: {self.is_min_player}"

    def __repr__(self):
        return self.__str__()


class Winner(Enum):
    CROSS = 1
    TIE = 0
    CIRCLE = -1


_stdscr: curses.window
_method_count: int = 0
_nodes_where_ai_wins: list[Node] = []


def log_console(item):
    with open('console.txt', 'a') as file:
        file.write(item)


def get_possible_actions(node: Node) -> list[Action]:
    possible_actions: list[Action] = []
    for y in range(3):
        for x in range(3):
            if node.board_state[y][x] == ' ':
                possible_actions.append(Action(x, y, node.is_min_player))
    return possible_actions


def print_board_to_file(board, file_path="tree-output.txt"):
    with open(file_path, 'a') as file:
        file.write('\n')
        for y in range(3):
            file.write(' ---' * 3 + '\n')
            file.write('|')
            for x in range(3):
                file.write(f' {board[y][x]} |')
            file.write('\n')
        file.write(' ---' * 3 + '\n')


def create_actions_tree(initial_node: Node, stdscr: curses.window) -> Action:
    global _stdscr
    _stdscr = stdscr

    _create_new_action_node(initial_node)
    log_console("Finished creating action tree" + str(initial_node) + "\n")

    if len(_nodes_where_ai_wins) == 0:
        possible_actions: list[Action] = get_possible_actions(initial_node)
        action = random.choice(possible_actions)
        action.is_min_player = True
        log_console("Random action: " + str(action) + "\n")

        return action
    for node in _nodes_where_ai_wins:
        print_board_to_file(node.board_state)
    best_choice = min(_nodes_where_ai_wins, key=lambda n: n.iteration)

    while best_choice.parent:
        log_console("best choice in loop: " + str(best_choice) + "\n")
        best_choice = best_choice.parent

    log_console("best choice in else no parent: " + str(best_choice) + "\n")
    return best_choice.action


def _print_node(node: Node):
    print_board_to_file(node.board_state)

    for child in node.children:
        _print_node(child)


def _create_new_action_node(node: Node):
    global _method_count
    global _nodes_where_ai_wins

    _stdscr.addstr(7, 0, "iteration: " + str(node.iteration))
    _method_count += 1
    _stdscr.addstr(8, 0, "method count: " + str(_method_count))

    _stdscr.refresh()

    if node.iteration > 5:
        return
    winner: Winner = get_terminal(node.board_state)
    if winner == Winner.CIRCLE:
        _nodes_where_ai_wins.append(node)
    if winner != Winner.TIE:
        node.score = winner.value
        return
    possible_actions: list[Action] = get_possible_actions(node)
    for action in possible_actions:
        board_copy = [row[:] for row in node.board_state]  # Create a deep copy of the board

        new_node = Node(board_copy, not node.is_min_player, action, node.iteration + 1)
        if new_node.is_min_player:
            board_copy[action.y][action.x] = 'o'
        else:
            board_copy[action.y][action.x] = 'x'

        node.children.append(new_node)
        _create_new_action_node(new_node)


def get_terminal(board: list[list[str]]) -> Winner:
    winner = Winner.TIE

    # Check rows:
    for y in range(3):
        row = board[y]
        if all(cell == 'x' for cell in row):
            return Winner.CROSS
        if all(cell == 'o' for cell in row):
            return Winner.CIRCLE

    # Check columns: First transpose the board and then rows are columns
    transposed_board = [[' ' for _ in range(3)] for _ in range(3)]
    for y in range(3):
        for x in range(3):
            transposed_board[x][y] = board[y][x]

    for y in range(3):
        transposed_row = transposed_board[y]
        if all(cell == 'x' for cell in transposed_row):
            return Winner.CROSS
        if all(cell == 'o' for cell in transposed_row):
            return Winner.CIRCLE

    # Check top left to right down diagonal
    diagonal = []
    for y in range(3):
        for x in range(3):
            if x == y:
                diagonal.append(board[y][x])
    if all(cell == 'x' for cell in diagonal):
        return Winner.CROSS
    if all(cell == 'o' for cell in diagonal):
        return Winner.CIRCLE

    # Check top right to left down diagonal
    counter_diagonal = []
    for y in range(3):
        for x in range(3):
            if x + y == 2:
                counter_diagonal.append(board[y][x])
    if all(cell == 'x' for cell in counter_diagonal):
        return Winner.CROSS
    if all(cell == 'o' for cell in counter_diagonal):
        return Winner.CIRCLE

    return winner
