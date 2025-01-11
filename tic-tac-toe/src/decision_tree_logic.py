from tic_tac_toe_types import Node, Action, Winner
from typing import Dict
import math
from graphviz import Digraph

_board_dictionary: Dict[str, Node] = {}
_method_count: int = 0
_terminal_nodes: list[Node] = []
_stack = []


def flatten_board_state(board: list[list[str]]) -> str:
    return ''.join([cell for row in board for cell in row])


def get_possible_actions(node: Node) -> list[Action]:
    possible_actions: list[Action] = []
    for y in range(3):
        for x in range(3):
            if node.board_state[y][x] == ' ':
                possible_actions.append(Action(x, y, not node.action.is_min_player))
    return possible_actions


def create_decision_tree(initial_node: Node) -> Action:
    if initial_node.score is None:
        if initial_node.action.is_min_player:
            initial_node.score = math.inf
        else:
            initial_node.score = -math.inf

    # _stack.append(initial_node)

    # while _stack:
    #     node = _stack.pop()
    _minimax(initial_node, 8, False)
    print("Finished action tree, method recursion count: " + str(_method_count))

    valid_children = [child for child in initial_node.children if child.score is not None]

    best_node: Node = min(valid_children, key=lambda child: child.score)

    if best_node:
        print(f'Best action: {best_node.action}')
        return best_node.action
    else:
        print("NO GOOD ACTION FOUND?")
    # _print_node(initial_node)
    # graph = visualize_tree(initial_node)
    # graph.render('tree', format='png', view=True)

    # _stack.append(initial_node)

    # best_node: Node = min(node.children, key=lambda child: child.score + child.iteration)

    # while _stack:
    #     node = _stack.pop(0)    # queue for bfs to check best option taking into account the least steps
    #     if node.action.is_min_player:
    # winning_nodes: list[Node] = [n for n in _terminal_nodes if n.score == Winner.CIRCLE.value]
    # print(f'length winning nodes: {len(winning_nodes)}')
    # for a in winning_nodes:
    #     print("score = " + str(a.score))
    # best_node: Node = min(winning_nodes, key=lambda n: n.score + n.iteration)
    # last_node: Node = initial_node
    #
    # while best_node.parent:
    #     last_node = best_node
    #     best_node = best_node.parent
    # print(f'lastNode {last_node.action}, {last_node.score}')
    # print(f'best_node {best_node.action}')
    #
    # return last_node.action
    #         return best_node.action
    #     else:
    #         _stack.extend(node.children)


def get_children(node: Node, is_maximizing: bool) -> list[Node]:
    children = []
    for action in get_possible_actions(node):
        new_board = [row[:] for row in node.board_state]
        new_board[action.y][action.x] = 'x' if is_maximizing else 'o'
        child_node = Node(new_board, action, not is_maximizing, node)
        node.children.append(child_node)
        children.append(child_node)
    return children


def _minimax(node, depth, is_maximizing):
    if is_terminal(node.board_state):
        winner = get_winner(node.board_state)
        return winner.value

    if is_maximizing:
        max_eval = -float('inf')
        for child in get_children(node, is_maximizing):
            evaluation = _minimax(child, depth + 1, False)
            max_eval = max(max_eval, evaluation)
        node.score = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for child in get_children(node, is_maximizing):
            evaluation = _minimax(child, depth + 1, True)
            min_eval = min(min_eval, evaluation)
        node.score = min_eval
        return min_eval


# def _minimax(node: Node) -> None:
#     global _terminal_nodes
#     global _method_count
#     _method_count += 1
#
#     if node.iteration > 22 or is_terminal(node.board_state):
#         _terminal_nodes.append(node)
#         return
#
#     # for each action determine the best one
#     best_nodes: list[Node] = []
#     best_score = -math.inf if not node.action.is_min_player else math.inf
#
#     for action in get_possible_actions(node):
#         board_copy = [row[:] for row in node.board_state]  # Create a deep copy of the board
#         board_copy[action.y][action.x] = 'o' if action.is_min_player else 'x'
#         # score: float = get_score_from_board(board_copy)
#         score: float = get_score_simple(board_copy)
#
#         new_node = Node(board_copy, action, node.iteration + 1)
#         new_node.score = score
#         new_node.parent = node
#
#         _minimax(new_node)  # Recursively call minimax on the new node
#
#         if node.action.is_min_player:
#             best_score = min(best_score, new_node.score)
#         else:
#             best_score = max(best_score, new_node.score)
#
#         if new_node.score == best_score:
#             best_nodes = [new_node]
#         elif new_node.score == best_score:
#             best_nodes.append(new_node)
#
#     node.score = best_score
#     node.children.extend(best_nodes)
#     _stack.extend(best_nodes)


#
#
# def _minimax(node: Node):
#     global _method_count
#     _method_count += 1
#
#     # if node.iteration > 5:
#     #     return
#
#     score: float = get_score_from_board(node.board_state)
#     node.score = score
#
#     if get_winner(node.board_state) != Winner.TIE:
#         return  # No actions needed anymore, since it is at an end.
#
#     for action in get_possible_actions(node):
#         board_copy = [row[:] for row in node.board_state]  # Create a deep copy of the board
#         board_copy[action.y][action.x] = 'o' if node.action.is_min_player else 'x'
#
#         flattened_board = flatten_board_state(board_copy)
#
#         # if flattened_board not in _board_dictionary:
#         exists = _board_dictionary.get(flattened_board)
#         if exists:
#             return
#         else:
#             new_node = Node(board_copy, action, node.iteration + 1)
#             _board_dictionary[flattened_board] = new_node
#
#             node.children.append(new_node)
#             _stack.append(new_node)
#         # We can use memoization in the way of it doesn't matter how the algorithm came here, and the children of
#         # this board_state only need to be calculated once.


def is_terminal(board: list[list[str]]) -> bool:
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return True
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    # Check for a tie
    for row in board:
        if ' ' in row:
            return False
    return True


def get_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return Winner.CROSS if board[i][0] == 'x' else Winner.CIRCLE
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return Winner.CROSS if board[0][i] == 'x' else Winner.CIRCLE
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return Winner.CROSS if board[0][0] == 'x' else Winner.CIRCLE
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return Winner.CROSS if board[0][2] == 'x' else Winner.CIRCLE
    return Winner.TIE


def check_line(line: list[str], crosses_pressure: int, circles_pressure: int) -> (float, int, int):
    crosses_in_line = [cell for cell in line if cell == 'x']
    circles_in_line = [cell for cell in line if cell == 'o']

    if len(crosses_in_line) == 3:
        return Winner.CROSS.value, crosses_pressure, circles_pressure
    elif len(crosses_in_line) == 2 and len(circles_in_line) == 0:
        crosses_pressure += 1
    else:
        circles_in_line = [cell for cell in line if cell == 'o']
        if len(circles_in_line) == 3:
            return Winner.CIRCLE.value, crosses_pressure, circles_pressure
        elif len(circles_in_line) == 2 and len(crosses_in_line) == 0:
            circles_pressure += 1
    return None, crosses_pressure, circles_pressure


def get_score_from_board(board: list[list[str]]) -> float:
    crosses_pressure = 0
    circles_pressure = 0

    # Check rows
    for row in board:
        result, crosses_pressure, circles_pressure = check_line(row, crosses_pressure, circles_pressure)
        if result is not None:
            return result

    # Check columns
    for col in range(3):
        column = [board[row][col] for row in range(3)]
        result, crosses_pressure, circles_pressure = check_line(column, crosses_pressure, circles_pressure)
        if result is not None:
            return result

    # Check diagonals
    diagonal = [board[i][i] for i in range(3)]
    result, crosses_pressure, circles_pressure = check_line(diagonal, crosses_pressure, circles_pressure)
    if result is not None:
        return result

    counter_diagonal = [board[i][2 - i] for i in range(3)]
    result, crosses_pressure, circles_pressure = check_line(counter_diagonal, crosses_pressure, circles_pressure)
    if result is not None:
        return result

    score: float = (crosses_pressure - circles_pressure) / 10
    return score


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


def _get_visualized_board(board: list[list[str]]) -> str:
    flattened = flatten_board_state(board)
    return add_separator_every_three_chars(flattened)


def add_separator_every_three_chars(input_string: str) -> str:
    result = []
    for i in range(0, len(input_string), 3):
        result.append(input_string[i:i + 3])
    return '\n'.join(result)


def visualize_tree(node, graph=None, parent=None):
    board = _get_visualized_board(node.board_state)
    if graph is None:
        graph = Digraph()
        graph.attr(size='1000,1000!')  # Set the maximum width and height of the image
        graph.node(name=board, label=board)
    else:
        graph.node(name=board, label=board)
        if parent:
            graph.edge(_get_visualized_board(parent.board_state), board)

    for child in node.children:
        visualize_tree(child, graph, node)

    return graph


def _print_node(node: Node):
    print_board_to_file(node.board_state)
    with open('tree-output.txt', 'a') as file:
        file.write("SCORE: " + str(node.score))
        file.write('\n')

    for child in node.children:
        _print_node(child)
