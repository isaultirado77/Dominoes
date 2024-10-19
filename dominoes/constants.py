from enum import Enum


class DominoEnd(Enum):
    HEAD = -1
    TAIL = 1


class GameState(Enum):
    IN_PROGRESS = "The game is in progress."
    GAME_OVER = "The game is over."
    DRAW = "It's a draw."
