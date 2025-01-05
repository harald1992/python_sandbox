from typing import List
from enum import Enum

from generate_maze import find_cell, CellType, Cell
from my_types import Vector2, DIRECTIONS, CELL_SIZE, SCREEN, WIDTH, HEIGHT, CLOCK
import pygame


class Algorithm(Enum):
    DFS = 0
    BFS = 1
    A_STAR = 2


class Node(Vector2):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.parent = None
        self.total_path_cost = 0

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"Node(x: {self.x}, y: {self.y}, parent: {self.parent}, total_path_cost: {len(self.total_path_cost)})"

    def __repr__(self):
        return self.__str__()


class StackFrontier:  # dfs
    def __init__(self):
        self.frontier: List[Node] = []

    def add(self, node: Node):
        self.frontier.append(node)

    def remove(self):
        if len(self.frontier) == 0:
            return None
        else:
            return self.frontier.pop()


class QueueFrontier(StackFrontier):
    def remove(self):
        if len(self.frontier) == 0:
            return None
        else:
            return self.frontier.pop(0)


class AStarFrontier(StackFrontier):
    def remove(self):
        if len(self.frontier) == 0:
            return None
        else:
            self.frontier.sort(key=lambda n: _get_heuristic_length(n, _goal) + n.total_path_cost)
            return self.frontier.pop(0)


_explored = set()
_frontier = StackFrontier()
_algorithm: Algorithm = Algorithm.A_STAR
_maze: List[Cell]
_amount_checked = 0
_goal: Node
_is_greedy = True


def _is_allowed_path(current: Node):
    if current.x < 0 or current.x > WIDTH or current.y < 0 or current.y > HEIGHT:
        return False
    cell = find_cell(_maze, Vector2(current.x, current.y))
    if cell is not None:
        return current not in _explored and cell.cell_type == CellType.PATH
    else:
        return False


def search_maze(maze: List[Cell], current: Vector2, goal: Vector2, algorithm=Algorithm.BFS, is_greedy=True):
    global _maze
    global _algorithm
    global _frontier
    global _goal
    global _is_greedy

    _maze = maze
    _algorithm = algorithm
    _goal = goal
    _is_greedy = is_greedy

    if _algorithm == Algorithm.BFS:
        _frontier = QueueFrontier()
    elif _algorithm == Algorithm.A_STAR:
        _frontier = AStarFrontier()

    _search(Node(current.x, current.y), Node(goal.x, goal.y))


def _search(current: Node, goal: Node):
    global _amount_checked
    _amount_checked = _amount_checked + 1
    print("Amount checked: ", _amount_checked)
    CLOCK.tick(6)
    if current == goal:
        print("Goal reached")
        trace_path_from_goal(current)
        return

    draw_node(current, (150, 150, 150))
    _explored.add(current)

    allowed_new_nodes: List[Node] = [
        node for node in [Node(current.x + direction[0], current.y + direction[1]) for direction in DIRECTIONS]
        if _is_allowed_path(node)
    ]

    if _is_greedy:
        allowed_new_nodes.sort(key=lambda n: _get_heuristic_length(n, goal), reverse=True)

    for node in allowed_new_nodes:
        node.parent = current
        node.total_path_cost = current.total_path_cost + 1
        _frontier.add(node)

    node: Node = _frontier.remove()
    if node is not None:
        _search(node, goal)


def _get_heuristic_length(node: Node, goal: Node):
    return abs(goal.x - node.x) + abs(goal.y - node.y) # Manhattan distance


def draw_node(node: Node, color: tuple):
    pygame.draw.rect(SCREEN, color,
                     (node.x * CELL_SIZE, node.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    font = pygame.font.Font(None, 12)  # None uses the default font, 36 is the font size

    text_surface = font.render(str(node.total_path_cost), True, (0, 0, 0))
    SCREEN.blit(text_surface, ((node.x + 0.25) * CELL_SIZE, (node.y + 0.25) * CELL_SIZE))

    pygame.display.flip()


def trace_path_from_goal(node: Node):
    while node.parent:
        CLOCK.tick(30)
        draw_node(node, (0, 0, 255))
        node = node.parent
    draw_node(node, (0, 0, 255))  # also draw the last one
