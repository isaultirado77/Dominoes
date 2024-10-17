from abc import ABC, abstractmethod
import random
import math


class Player(ABC):

    def __init__(self, name: str = 'Player'):
        self.name = name
        self.pieces = []
        self.move_msg = ''

    @abstractmethod
    def move(self, index: int):
        pass

    def get_move_msg(self) -> str:
        return self.move_msg

    def set_move_msg(self, msg) -> None:
        self.move_msg = msg

    def take_piece(self, piece: list) -> None:
        self.pieces.append(piece)

    def get_snake(self):
        snakes = [x for x in self.pieces if x[0] == x[1]]

        if snakes:
            if len(snakes) == 1:
                return snakes[0]
            # Find the largest piece
            max_sum = (-1) * math.inf
            for piece in snakes:
                current_sum = sum(piece)
                if current_sum > max_sum:
                    max_sum = current_sum
            return [int(max_sum / 2), int(max_sum / 2)]

    def get_pieces(self) -> list:
        return self.pieces

    def drop_piece(self, piece: list) -> None:
        if piece:
            self.pieces.remove(piece)

    def clear_pieces(self) -> None:
        self.pieces.clear()

    def get_total_pieces(self) -> int:
        return len(self.pieces)

    def get_piece_by_index(self, index: int):
        return self.pieces[index]


class Human(Player):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.set_move_msg('It\'s your turn to make a move. Enter your command.')

    def prompt_player_move(self) -> int:
        while True:
            try:
                move = int(input())
                if abs(move) < self.get_total_pieces() + 1:
                    return move
                else:
                    print("Invalid input. Please try again. ")
            except ValueError:
                print("Invalid input. Please try again.")

    def move(self, **kwargs):
        index = self.prompt_player_move()
        if index == 0:
            return None, None
        else:
            if index < 0:  # Place piece to left
                return 0, self.get_piece_by_index(abs(index) - 1)
            if index > 0:  # Place piece to right
                return -1, self.get_piece_by_index(index - 1)

    def __str__(self):
        return 'Player'


class Computer(Player):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.set_move_msg('Computer is about to make a move. Press Enter to continue...')

    def move(self, index: int = None):
        input()
        total_pieces = self.get_total_pieces()
        index = random.randint(1 - total_pieces, total_pieces - 1)
        piece = self.get_piece_by_index(index)
        return 0 if index < 0 else -1, piece

    def __str__(self):
        return 'Computer'
