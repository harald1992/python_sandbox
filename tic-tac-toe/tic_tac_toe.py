from game import Game
import curses


def main(stdscr: curses.window):
    game = Game()
    game.start_game(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
