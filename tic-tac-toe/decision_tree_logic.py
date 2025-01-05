import curses

_stdscr: curses.window
_method_count: int = 0


class Node:
    def __init__(self, board_state, is_min_player=True):
        self.children: list[Node] = []
        self.parent: Node | None = None
        self.score: int | None = None
        self.iteration = 0
        self.board_state: list[list[str]] = board_state
        self.is_min_player: bool = is_min_player


class Action:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def get_possible_actions(board: list[list[str]]) -> list[Action]:
    possible_actions: list[Action] = []
    for y in range(3):
        for x in range(3):
            if board[y][x] == ' ':
                possible_actions.append(Action(x, y))
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


def create_actions_tree(board: list[list[str]], stdscr: curses.window):
    global _stdscr
    _stdscr = stdscr
    with open('console.txt', 'w') as file:
        file.write("")
    with open('tree-output.txt', 'w') as file:
        file.write("")
    initial_node = Node(board)

    _create_new_action_node(initial_node)

    _print_node(initial_node)


def _print_node(node: Node):
    print_board_to_file(node.board_state)

    for child in node.children:
        _print_node(child)


def _create_new_action_node(node: Node):
    global _method_count
    with open('console.txt', 'a') as file:
        file.write(str(node.is_min_player))
    node.iteration += 1
    _stdscr.addstr(7, 0, "iteration: " + str(node.iteration))
    _method_count += 1
    _stdscr.addstr(8, 0, "method count: " + str(_method_count))

    _stdscr.refresh()

    # if node.iteration > 4:
    #     return
    possible_actions: list[Action] = get_possible_actions(node.board_state)
    for action in possible_actions:
        board_copy = [row[:] for row in node.board_state]  # Create a deep copy of the board
        if node.is_min_player:
            board_copy[action.y][action.x] = 'o'
        else:
            board_copy[action.y][action.x] = 'x'

        new_node = Node(board_copy, not node.is_min_player)
        new_node.iteration = node.iteration
        node.children.append(new_node)
        _create_new_action_node(new_node)
