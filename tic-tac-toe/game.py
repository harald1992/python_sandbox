from enum import Enum
import time
import random
import os


class Winner(Enum):
    CROSS = 1
    TIE = 0
    CIRCLE = 2


class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.is_max_player_turn = True

    def print_board(self):
        os.system('clear')
        for y in range(3):
            print(' ---' * 3)
            print('|', end='')
            for x in range(3):
                print(f' {self.board[y][x]} |', end='')
            print()
        print(' ---' * 3)

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

    def get_possible_actions(self) -> list[list[int]]:
        possible_actions = []
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == ' ':
                    possible_actions.append([x, y])
        return possible_actions

    def is_max_players_turn(self) -> bool:
        return self.is_max_player_turn

    def perform_turn_min(self):
        possible_actions = self.get_possible_actions()

        action = random.choice(possible_actions)
        self.board[action[1]][action[0]] = 'o'

    def start_game(self):
        print("Starting game")

        while True:
            # PLAYER (MAX) TURN
            self.print_board()
            choice = input("Enter your choice (x,y): ")
            x, y = map(int, choice.split(','))
            self.board[y][x] = 'x'
            self.print_board()
            if self.get_terminal() == Winner.CROSS:
                print("Cross (Max) wins!!")
                break

            # AI (Min) turn
            time.sleep(1.5)
            self.perform_turn_min()
            self.print_board()
            if self.get_terminal() == Winner.CIRCLE:
                print("Circle (Min) wins!!")
                break
