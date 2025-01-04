from enum import Enum
import pygame


class CellType(Enum):
    PATH = 0
    WALL = 1


class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Cell(Vector2):
    def __init__(self, x: int, y: int, cell_type: CellType):
        super().__init__(x, y)
        self.cell_type = cell_type


class MazeResult:
    def __init__(self, maze: list[Cell], start_coordinate: Vector2, last_coordinate: Vector2):
        self.maze = maze
        self.start_coordinate = start_coordinate
        self.goal_coordinate = last_coordinate


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
WIDTH, HEIGHT = 30, 30
CELL_SIZE = 640 / WIDTH
SCREEN = pygame.display.set_mode((640, 640))
CLOCK = pygame.time.Clock()
