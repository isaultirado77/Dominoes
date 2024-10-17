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

    def get_piece(self) -> list:
        piece = random.choice(self.arr)
        self.arr.remove(piece)
        return piece


class Player(ABC):

    def __init__(self, name: str = 'Player'):
        self.name = name
        self.pieces = []

    @abstractmethod
    def move(self):
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
            return [max_sum / 2, max_sum / 2]

    def get_pieces(self):
        return self.pieces

    def drop_piece(self, piece: list) -> None:
        self.pieces.remove(piece)


class Human(Player):
    def __init__(self, name: str = None):
        super().__init__(name)

    def move(self):
        print(f'{self.name} -> moving...')
        pass

    def __str__(self):
        return 'Player'


class Computer(Player):
    def __init__(self, name: str = None):
        super().__init__(name)

    def move(self) -> None:
        print(f'{self.name} -> calculating...')
        pass

    def __str__(self):
        return 'Computer'


class Engine:
    def __init__(self):
        self.box = Box()
        self.human = Human()
        self.bot = Computer()
        self.isHumanTurn = True
        self.snake = None

    def deal_dominoes(self) -> None:
        for i in range(7):
            human_piece = self.box.get_piece()
            bot_piece = self.box.get_piece()
            self.human.take_piece(human_piece)
            self.bot.take_piece(bot_piece)

    def get_first_player(self):
        human_snake = self.human.get_snake()
        bot_snake = self.bot.get_snake()
        if not human_snake and not bot_snake:
            self.deal_dominoes()
            self.get_first_player()
        if sum(bot_snake) > sum(bot_snake):
            self.snake = bot_snake
            self.bot.drop_piece(bot_snake)
            self.switch_turn()
        else:
            self.snake = human_snake
            self.human.drop_piece(human_snake)

    def switch_turn(self):
        return True if self.isHumanTurn else False

    def display_game_state(self):
        print('Stock pieces:', self.box.arr)
        print('Computer pieces:', self.bot.get_pieces())
        print('Player pieces:', self.human.get_pieces())
        print('Domino snake:', self.snake)
        print('Status:', self.human if self.isHumanTurn else self.bot)

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
