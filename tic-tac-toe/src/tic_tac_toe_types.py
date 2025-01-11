from enum import Enum
# from types import CodeType, FrameType, TracebackType, ModuleType, FunctionType


class Node:
    def __init__(self, board_state, action=None, is_min_player=False, parent=None):
        self.board_state = board_state
        self.action = action
        self.is_min_player = is_min_player
        self.parent = parent
        self.children = []
        self.score = None

    def __str__(self):
        return f"Node(children: {self.children}, score: {self.score}, action: {self.action})"

    def __repr__(self):
        return self.__str__()


class Action:
    __slots__ = ['x', 'y', 'is_min_player']

    def __init__(self, x: int, y: int, is_min_player: bool):
        self.x = x
        self.y = y
        self.is_min_player = is_min_player

    def __str__(self):
        return f"Action(x: {self.x}, y: {self.y}, is_min_player: {self.is_min_player}"

    def __repr__(self):
        return self.__str__()


class Winner(Enum):
    CROSS = 1.0
    TIE = 0.0
    CIRCLE = -1.0


class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
