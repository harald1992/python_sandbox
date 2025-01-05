from enum import Enum
import time
import random
import curses
from decision_tree_logic import create_actions_tree


class Winner(Enum):
    CROSS = 1
    TIE = 0
    CIRCLE = 2


class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.is_max_player_turn = True
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

    def get_terminal(self) -> Winner:
        winner = Winner.TIE

        # Check rows:
        for y in range(3):
            row = self.board[y]
            if all(cell == 'x' for cell in row):
                return Winner.CROSS
            if all(cell == 'o' for cell in row):
                return Winner.CIRCLE

        # Check columns: First transpose the board and then rows are columns
        transposed_board = [[' ' for _ in range(3)] for _ in range(3)]
        for y in range(3):
            for x in range(3):
                transposed_board[x][y] = self.board[y][x]

        for y in range(3):
            transposed_row = transposed_board[y]
            if all(cell == 'x' for cell in transposed_row):
                return Winner.CROSS
            if all(cell == 'o' for cell in transposed_row):
                return Winner.CIRCLE

        # Check top left to right down diagonal
        diagonal = []
        for y in range(3):
            for x in range(3):
                if x == y:
                    diagonal.append(self.board[y][x])
        if all(cell == 'x' for cell in diagonal):
            return Winner.CROSS
        if all(cell == 'o' for cell in diagonal):
            return Winner.CIRCLE

        # Check top right to left down diagonal
        counter_diagonal = []
        for y in range(3):
            for x in range(3):
                if x + y == 2:
                    counter_diagonal.append(self.board[y][x])
        if all(cell == 'x' for cell in counter_diagonal):
            return Winner.CROSS
        if all(cell == 'o' for cell in counter_diagonal):
            return Winner.CIRCLE

        return winner

    def is_max_players_turn(self) -> bool:
        return self.is_max_player_turn

    # def perform_turn_min(self):
        # possible_actions = self.get_possible_actions()
        #
        # action = random.choice(possible_actions)
        # self.board[action[1]][action[0]] = 'o'
        # create_actions_tree(self.board)

    def start_game(self, stdscr: curses.window):
        curses.curs_set(0)
        stdscr.keypad(True)
        stdscr.clear()
        stdscr.refresh()
        print("Starting game")

        while True:
            self.player_turn(stdscr)
            self.print_board(stdscr)

            if self.get_terminal() == Winner.CROSS:
                stdscr.addstr(7, 0, "Cross (Max) wins!!")
                stdscr.refresh()
                stdscr.getch()
                break

            # AI (Min) turn
            # time.sleep(2.5)
            # self.perform_turn_min()
            create_actions_tree(self.board, stdscr)
            # self.print_board(stdscr)
            # if self.get_terminal() == Winner.CIRCLE:
            #     stdscr.addstr(7, 0, "Circle (Min) wins!!")
            #     stdscr.refresh()
            #     stdscr.getch()
            #     break

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
                    break


