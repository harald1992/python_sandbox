from decision_tree_logic import create_decision_tree, is_terminal, get_score_from_board
import os
from tic_tac_toe_types import Vector2, Winner, Node, Action

finger_emoticon = "\U0001F446"


class Game:
    def __init__(self):
        self.node: Node | None = None
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.cursor = Vector2(-1, -1)
        self.debug_mode = True

    def print_board(self):
        if not self.debug_mode:
            os.system('clear')
        for y in range(3):
            print(' ---' * 3)
            print('|', end='')
            for x in range(3):
                if y == self.cursor.y and x == self.cursor.x:
                    print(f' {finger_emoticon}', end='|')
                else:
                    print(f' {self.board[y][x]} ', end='|')
            print()
        print(' ---' * 3)

    def get_state(self) -> list[list[str]]:
        return self.board

    def perform_turn_min(self):
        action = create_decision_tree(self.node)
        self.board[action.y][action.x] = 'o'

    def start_game(self):
        os.system('clear')
        print("Starting game")

        while True:
            self.player_turn()
            self.print_board()

            if is_terminal(self.board) and get_score_from_board(self.board) == Winner.CROSS.value:
                print("CROSS (MAX) WINS!!")
                break

            # AI (Min) turn
            self.perform_turn_min()
            self.print_board()
            if is_terminal(self.board) and get_score_from_board(self.board) == Winner.CIRCLE.value:
                print("CIRCLE (MIN) WINS!!")
                break

    def player_turn(self):
        self.cursor = self.find_first_unoccupied_spot()

        while True:
            self.print_board()

            move = input("Enter your move (w/a/s/d for movement, space to place 'x'): ").lower()
            print(move)
            if move == 'w' and self.cursor.y > 0:
                self.cursor.y -= 1
            elif move == 's' and self.cursor.y < 2:
                self.cursor.y += 1
            elif move == 'a' and self.cursor.x > 0:
                self.cursor.x -= 1
            elif move == 'd' and self.cursor.x < 2:
                self.cursor.x += 1
            elif move == ' ':
                print("move is space")
                if self.board[self.cursor.y][self.cursor.x] == ' ':
                    self.board[self.cursor.y][self.cursor.x] = 'x'

                    self.node = Node(self.board, Action(self.cursor.x, self.cursor.y, False), False, None)

                    self.cursor = Vector2(-1, -1)   # reset cursor to be invis
                    break

    def find_first_unoccupied_spot(self) -> Vector2:
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == ' ':
                    return Vector2(x, y)

        raise Exception("No unoccupied spot found")
