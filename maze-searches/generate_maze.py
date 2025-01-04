import random
from typing import List, Optional

import pygame

from my_types import CellType, DIRECTIONS, MazeResult, Vector2, WIDTH, HEIGHT, Cell, CELL_SIZE, SCREEN, CLOCK

last_coordinate: Vector2 = Vector2(0, 0)


def generate_maze() -> MazeResult:
    maze: List[Cell] = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            maze.append(Cell(x, y, CellType.WALL))
    maze[0].cell_type = CellType.PATH
    start_coordinate = Vector2(0, 0)
    return _explore_step_and_generate_new_steps(maze, start_coordinate)


def find_cell(maze: List[Cell], coordinate: Vector2) -> Optional[Cell]:
    for cell in maze:
        if cell.x == coordinate.x and cell.y == coordinate.y:
            return cell
    return None


def is_valid_move_and_wall(maze: List[Cell], next_coordinate: Vector2) -> bool:
    return (0 <= next_coordinate.x < WIDTH
            and 0 <= next_coordinate.y < HEIGHT
            and find_cell(maze, next_coordinate).cell_type == CellType.WALL)


def _explore_step_and_generate_new_steps(
        maze: List[Cell],
        current_coordinate: Vector2) -> MazeResult:
    global last_coordinate
    cell2 = find_cell(maze, current_coordinate)
    if cell2 is not None:
        cell2.cell_type = CellType.PATH
        pygame.draw.rect(SCREEN, (255, 255, 255),
                         (cell2.x * CELL_SIZE, cell2.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # CLOCK.tick(60)
    random.shuffle(DIRECTIONS)
    for dx, dy in DIRECTIONS:
        next_coordinate = Vector2(current_coordinate.x + dx * 2, current_coordinate.y + dy * 2)
        if is_valid_move_and_wall(maze, next_coordinate):
            cell = find_cell(maze, Vector2(current_coordinate.x + dx, current_coordinate.y + dy))
            if cell is not None:
                cell.cell_type = CellType.PATH
                pygame.draw.rect(SCREEN, (255, 255, 255),
                                 (cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()  # Update the display after drawing each cell

            last_coordinate = next_coordinate
            _explore_step_and_generate_new_steps(maze, next_coordinate)
    return MazeResult(maze, current_coordinate, last_coordinate)
