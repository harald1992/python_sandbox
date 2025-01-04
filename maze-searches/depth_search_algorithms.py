from typing import List, Optional

import pygame

from generate_maze import find_cell, WIDTH, HEIGHT, CellType
from my_types import Vector2, DIRECTIONS, Cell, SCREEN, CELL_SIZE, CLOCK


class Node(Vector2):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.children = []
        self.parent = None


def find_node(node_list: List[Node], coordinate: Node) -> Optional[Node]:
    for node in node_list:
        if node.x == coordinate.x and node.y == coordinate.y:
            return node
    return None


visited_nodes: List[Node] = []
found_goal = False


def is_valid_path(maze: List[Cell], next_coordinate: Vector2) -> bool:
    return (0 <= next_coordinate.x < WIDTH
            and 0 <= next_coordinate.y < HEIGHT
            and find_cell(maze, next_coordinate).cell_type == CellType.PATH)


def draw_node(node: Node, color: tuple):
    pygame.draw.rect(SCREEN, color,
                     (node.x * CELL_SIZE, node.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()


def depth_first_search(maze: List[Cell], current: Node, goal: Node):
    global visited_nodes
    global found_goal

    if found_goal:
        return
    CLOCK.tick(5)
    print("new node added: ", current.x, current.y)
    draw_node(current, (100, 100, 100))

    for direction in DIRECTIONS:
        if found_goal:
            return

        new_node = Node(current.x + direction[0], current.y + direction[1])
        new_node.parent = current
        if new_node.x == goal.x and new_node.y == goal.y:
            print("found goal: parent = ", new_node.parent)
            found_goal = True
            trace_path_from_goal(new_node)
            return
        elif find_node(visited_nodes, new_node):
            print("already in visited nodes, don't search")
        else:
            print("new node parent = :", new_node.parent)
            current.children.append(new_node)
            visited_nodes.append(new_node)
            if is_valid_path(maze, new_node):
                print("Is valid move: ", new_node.x, new_node.y)
                depth_first_search(maze, new_node, goal)


def trace_path_from_goal(node: Node):
    while node.parent:
        print("Path from goal to start: ", node.x, node.y, node.parent)
        draw_node(node, (0, 0, 255))
        node = node.parent
    draw_node(node, (0, 0, 255))    # also draw the last one

    for visited_node in visited_nodes:
        print("visited node: ", visited_node.x, visited_node.y)

