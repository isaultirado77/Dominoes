from abc import ABC, abstractmethod
from collections import deque
import math


class Player(ABC):

    def __init__(self, name: str = 'Player'):
        self.name = name
        self.pieces = []
        self.move_msg = ''

    @abstractmethod
    def move(self, snake_pieces: deque = None):
        pass

    def get_move_msg(self) -> str:
        return self.move_msg

    def set_move_msg(self, msg) -> None:
        self.move_msg = msg

    def take_piece(self, piece: list) -> None:
        if piece:
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

    def move(self, snake_pieces: deque = None) -> tuple:
        index = self.prompt_player_move()
        if index == 0:
            return None, None
        else:
            if index < 0:  # Place piece to left
                return -1, self.get_piece_by_index(abs(index) - 1)
            if index > 0:  # Place piece to right
                return 1, self.get_piece_by_index(index - 1)

    def __str__(self):
        return "Player"


class Computer(Player):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.set_move_msg('Computer is about to make a move. Press Enter to continue...')
        self.random_counter = 0

    def move(self, snake_pieces: deque = None):
        input()
        # Concat hand pieces and snake pieces
        total_pieces = []

        for piece in self.pieces:
            total_pieces.append(piece)

        for piece in snake_pieces:
            total_pieces.append(piece)

        # Get frequency dict for the total pieces
        pieces_freq_dict = Computer.get_frequency_of_pieces(total_pieces)

        # Get score dict for the pieces
        score_dict = self.get_score_for_pieces(pieces_freq_dict)
        for piece, score in score_dict.items():
            if piece[0] == snake_pieces[0][0] or piece[1] == snake_pieces[0][0]:
                return -1, list(piece)
            elif piece[0] == snake_pieces[-1][-1] or piece[1] == snake_pieces[-1][-1]:
                return 1, list(piece)

        return None, None

    @staticmethod
    def get_frequency_of_pieces(total_pieces: list) -> dict:
        # Create the frequency dict, including 0
        freq_dict = {key: 0 for key in range(7)}
        for piece in total_pieces:
            # Get left and right side of the pieces
            left, right = piece

            # Plus one if left or right
            freq_dict[left] += 1
            freq_dict[right] += 1

        return freq_dict

    def get_score_for_pieces(self, freq_dict: dict) -> dict:
        score_dict = {}

        for piece in self.pieces:
            l, r = piece
            score_dict[(l, r)] = freq_dict[l] + freq_dict[r]

        return sort_dictionary_by_values(score_dict)  # Return sorted dictionary in descending order

    def __str__(self):
        return "Computer"


def sort_dictionary_by_values(dictionary: dict, des: bool = True) -> dict:
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=des))
