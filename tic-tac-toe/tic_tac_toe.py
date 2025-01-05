from game import Game
import curses


def main(stdscr: curses.window):
    game = Game()
    with open('console.txt', 'w') as file:
        file.write("")
    with open('tree-output.txt', 'w') as file:
        file.write("")
    game.start_game(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
