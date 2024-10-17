# Project: Dominoes

import random
import math
from abc import ABC, abstractmethod


class Box:
    def __init__(self):
        self.arr = []  # Storage the pieces
        self.generate_pieces()

    def generate_pieces(self) -> None:
        for i in range(7):  # 'i' points to the left number on the piece
            for j in range(i, 7):  # 'j' points to the right number on the piece
                piece = [i, j]
                self.arr.append(piece)

    def show_pieces(self) -> None:
        print(self.arr)

    def give_piece(self) -> list:
        piece = random.choice(self.arr)
        self.arr.remove(piece)
        return piece

    def reset_box(self) -> None:
        self.arr.clear()
        self.generate_pieces()

    def get_size(self) -> int:
        return len(self.arr)


class Player(ABC):

    def __init__(self, name: str = 'Player'):
        self.name = name
        self.pieces = []

    @abstractmethod
    def move(self, index: int):
        pass

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

    def clear_box(self) -> None:
        self.pieces.clear()

    def get_total_pieces(self) -> int:
        return len(self.pieces)

    def get_piece_by_index(self, index: int):
        return self.pieces[index]


class Human(Player):
    def __init__(self, name: str = None):
        super().__init__(name)

    def move(self, index: int):
        if index == 0:
            return None
        else:
            if index < 0:  # Place piece to left
                return 0, self.get_piece_by_index(abs(index))
            if index > 0:  # Place piece to right
                return -1, self.get_piece_by_index(index)

    def __str__(self):
        return 'Player'


class Computer(Player):
    def __init__(self, name: str = None):
        super().__init__(name)

    def move(self, index: int = None):
        total_pieces = self.get_total_pieces()
        index = random.randint(1 - total_pieces, total_pieces - 1)
        piece = self.get_piece_by_index(index)
        return piece

    def __str__(self):
        return 'Computer'


class Engine:
    def __init__(self):
        self.box = Box()
        self.human = Human()
        self.bot = Computer()
        self.is_human_turn = True
        self.current_player = self.human
        self.snake = []

    def deal_dominoes(self) -> None:
        for i in range(7):
            human_piece = self.box.give_piece()
            bot_piece = self.box.give_piece()
            self.human.take_piece(human_piece)
            self.bot.take_piece(bot_piece)

    def get_first_player(self):
        human_snake = self.human.get_snake()
        bot_snake = self.bot.get_snake()
        if not human_snake or not bot_snake:
            self.box.reset_box()
            self.clear_players_box()
            self.deal_dominoes()
            self.get_first_player()
        else:
            if sum(bot_snake) > sum(human_snake):
                self.snake.append(bot_snake)
                self.bot.drop_piece(bot_snake)
                self.switch_turn()
            else:
                self.snake.append(human_snake)
                self.human.drop_piece(human_snake)

    def switch_turn(self) -> None:
        self.is_human_turn = not self.is_human_turn
        self.current_player = self.human if self.is_human_turn else self.bot

    def clear_players_box(self) -> None:
        self.bot.clear_box()
        self.human.clear_box()

    def get_snake(self) -> str:
        return '\n'.join(str(segment) for segment in self.snake)

    def get_status(self) -> str:
        human_move = 'It\'s your turn to make a move. Enter your command.'
        bot_move = 'Computer is about to make a move. Press Enter to continue...'
        return f'Status: {bot_move if self.is_human_turn else human_move}'

    def display_player_pieces(self):
        pieces = self.human.get_pieces()
        print('Your pieces:')
        for i, piece in enumerate(pieces):
            print(f'{i + 1}:{piece}')
        print()

    def prompt_player_move(self) -> int:
        while True:
            try:
                move = int(input())
                if abs(move) < self.human.get_total_pieces():
                    return move
                else:
                    print("Error: Enter a valid index. ")
            except ValueError:
                print("Error: Enter a valid number.")

    def display_game_state(self):
        print('======================================================================')
        print('Stock size:', self.box.get_size())
        print('Computer pieces:', self.bot.get_total_pieces(), '\n')
        print(self.get_snake(), '\n')
        self.display_player_pieces()
        print('Status:', self.get_status())

    @staticmethod
    def get_engine():
        return Engine()


class Controller:
    def __init__(self):
        self.engine = Engine.get_engine()

    def run(self):
        self.engine.deal_dominoes()
        self.engine.get_first_player()
        self.engine.display_game_state()


def main():
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()
