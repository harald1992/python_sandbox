import pygame

from generate_maze import generate_maze
from my_types import MazeResult, CellType, CELL_SIZE, SCREEN, CLOCK
from depth_search_algorithms import depth_first_search, Node
from bfs_dfs_greedy_first_search_a_star_algorithms import search_maze, Algorithm

pygame.init()

mazeResult: MazeResult = generate_maze()
pygame.display.set_caption("Press any key to continue...")

print("Returned from function lastCoordinate: ", mazeResult.goal_coordinate.x, mazeResult.goal_coordinate.y)

index = 0


def handle_event(event):
    global index
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    elif event.type == pygame.KEYDOWN:
        print(event)
        if index == 0:
            draw_start_goal()
            index = index + 1
        else:
            search()


def draw_start_goal():
    SCREEN.fill((0, 0, 0))
    for cell in mazeResult.maze:
        color = (255, 255, 255) if cell.cell_type == CellType.PATH else (0, 0, 0)
        pygame.draw.rect(SCREEN, color, (cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # draw start & end coordinates
    pygame.draw.rect(SCREEN, (255, 0, 0), (0, 0, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(SCREEN, (0, 255, 0),
                     (mazeResult.goal_coordinate.x * CELL_SIZE,
                      mazeResult.goal_coordinate.y * CELL_SIZE,
                      CELL_SIZE,
                      CELL_SIZE))

    pygame.display.flip()  # flip() the display to put your work on screen


def search():
    # depth_first_search(mazeResult.maze, Node(mazeResult.start_coordinate.x, mazeResult.start_coordinate.y),
    #                    Node(mazeResult.last_coordinate.x, mazeResult.last_coordinate.y))
    search_maze(mazeResult.maze, mazeResult.start_coordinate, mazeResult.goal_coordinate, Algorithm.A_STAR, True)


while True:
    CLOCK.tick(60)
    new_event = pygame.event.wait()
    handle_event(new_event)
