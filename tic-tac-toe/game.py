import curses
from decision_tree_logic import create_actions_tree, Winner, get_terminal, Node, Action, log_console


class Game:
    def __init__(self):
        self.node: Node | None = None
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.cursor_x = 0
        self.cursor_y = 0

    def print_board(self, stdscr: curses.window):
        stdscr.clear()
        for y in range(3):
            stdscr.addstr(y * 2, 0, ' ---' * 3)
            stdscr.addstr(y * 2 + 1, 0, '|')
            for x in range(3):
                if y == self.cursor_y and x == self.cursor_x:
                    stdscr.addstr(y * 2 + 1, x * 4 + 1, f'[{self.board[y][x]}]')
                else:
                    stdscr.addstr(y * 2 + 1, x * 4 + 1, f' {self.board[y][x]} ')
                stdscr.addstr(y * 2 + 1, x * 4 + 4, '|')
            stdscr.addstr(y * 2 + 2, 0, ' ---' * 3)
        stdscr.refresh()

    def get_state(self) -> list[list[str]]:
        return self.board

    def perform_turn_min(self, stdscr: curses.window):
        action = create_actions_tree(self.node, stdscr)
        self.board[action.y][action.x] = 'o'
        log_console(str(self.board) + "\n")

    def start_game(self, stdscr: curses.window):
        curses.curs_set(0)
        stdscr.keypad(True)
        stdscr.clear()
        stdscr.refresh()
        print("Starting game")

        while True:
            self.player_turn(stdscr)
            self.print_board(stdscr)

            if get_terminal(self.board) == Winner.CROSS:
                stdscr.addstr(7, 0, "Cross (Max) wins!!")
                stdscr.refresh()
                stdscr.getch()
                break

            # AI (Min) turn
            self.perform_turn_min(stdscr)
            self.print_board(stdscr)
            if get_terminal(self.board) == Winner.CIRCLE:
                stdscr.addstr(7, 0, "Circle (Min) wins!!")
                stdscr.refresh()
                stdscr.getch()
                break

    def player_turn(self, stdscr: curses.window):
        while True:
            self.print_board(stdscr)

            key = stdscr.getch()
            stdscr.addstr(7, 0, str(key))

            if key == curses.KEY_UP and self.cursor_y > 0:
                self.cursor_y -= 1
            elif key == curses.KEY_DOWN and self.cursor_y < 2:
                self.cursor_y += 1
            elif key == curses.KEY_LEFT and self.cursor_x > 0:
                self.cursor_x -= 1
            elif key == curses.KEY_RIGHT and self.cursor_x < 2:
                self.cursor_x += 1
            elif key == ord(' '):
                if self.board[self.cursor_y][self.cursor_x] == ' ':
                    self.board[self.cursor_y][self.cursor_x] = 'x'
                    self.node: Node = Node(self.board, False, Action(self.cursor_x, self.cursor_y, False), 0)
                    break
