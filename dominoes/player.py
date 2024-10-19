from abc import ABC, abstractmethod
from utils import sort_dictionary_by_values, concat_lists
from domino_snake import DominoSnake
from constants import DominoEnd


class Player(ABC):
    def __init__(self):
        self.hand_tiles = []

    @abstractmethod
    def move(self):
        pass

    def take_tile(self, tile: list) -> None:
        self.hand_tiles.append(tile)

    def get_snake_tile(self):
        snakes = [x for x in self.hand_tiles if x[0] == x[1]]

        if not snakes:
            return None

        max_piece = snakes[0]
        max_sum = sum(max_piece)

        for tile in snakes[1:]:
            current_sum = sum(tile)
            if current_sum > max_sum:
                max_piece = tile
                max_sum = current_sum

        return max_piece

    def get_hand_tiles(self) -> list:
        return self.hand_tiles

    def drop_tile(self, tile: list) -> None:
        if tile:
            self.hand_tiles.remove(tile)

    def clear_hand_tiles(self) -> None:
        self.hand_tiles.clear()

    def get_amount_of_tiles(self):
        return len(self.hand_tiles)

    def get_tile_by_index(self, index: int) -> list:
        return self.hand_tiles[index]


class Human(Player):

    def move(self):
        index = self.prompt_player_move()
        if index == 0:
            return None, None
        else:
            if index < 0:
                return DominoEnd.HEAD, self.get_tile_by_index(abs(index) - 1)
            if index > 0:
                return DominoEnd.TAIL, self.get_tile_by_index(index - 1)

    def prompt_player_move(self) -> int:
        while True:
            try:
                move = int(input())
                if abs(move) < self.get_amount_of_tiles() + 1:
                    return move
                else:
                    print("Invalid input. Please try again. ")
            except ValueError:
                print("Invalid input. Please try again.")

    @staticmethod
    def get_move_msg() -> str:
        return 'It\'s your turn to make a move. Enter your command.'

    def __str__(self):
        return "Human"


class Computer(Player):

    def move(self, snake: DominoSnake = None):
        input()

        tiles = concat_lists(snake.to_list(), self.hand_tiles)

        # Get frequency dict for the total pieces
        pieces_freq_dict = Computer.get_tiles_frequency(tiles)

        # Get score dict for the pieces
        score_dict = self.get_score_for_hand_tiles(pieces_freq_dict)

        for piece, score in score_dict.items():
            if piece[0] == snake.head() or piece[1] == snake.head():
                return DominoEnd.HEAD, list(piece)
            elif piece[0] == snake.tail() or piece[1] == snake.tail():
                return DominoEnd.TAIL, list(piece)

        return None, None

    @staticmethod
    def get_tiles_frequency(total_tiles: list) -> dict:
        freq_dict = {key: 0 for key in range(7)}

        for piece in total_tiles:
            left, right = piece

            freq_dict[left] += 1
            freq_dict[right] += 1

        return freq_dict

    def get_score_for_hand_tiles(self, freq_dict: dict) -> dict:
        score_dict = {}

        for tile in self.hand_tiles:
            l, r = tile
            score_dict[(l, r)] = freq_dict[l] + freq_dict[r]

        return sort_dictionary_by_values(score_dict)  # Return sorted dictionary in descending order

    @staticmethod
    def get_move_msg() -> str:
        return 'Computer is about to make a move. Press Enter to continue...'

    def __str__(self):
        return "Computer"
