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

    def take_pieces(self, pieces: list) -> None:
        self.pieces = pieces

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


class Human(Player):
    def __init__(self, name: str = None):
        super().__init__(name)

    def move(self):
        print(f'{self.name} -> moving...')
        pass


class Computer(Player):
    def __init__(self, name: str = None):
        super().__init__(name)

    def move(self) -> None:
        print(f'{self.name} -> calculating...')
        pass


class Engine:
    def __init__(self):
        self.box = Box()
        self.human = Human()
        self.bot = Computer()
        self.isHumanTurn = True

    def deal_dominoes(self, player: Player) -> None:
        for i in range(7):
            piece = self.box.get_piece()

    def change_turn(self):
        return True if self.isHumanTurn else False

    def display_status(self):
        pass

    def get_first_player(self):
        pass

    @staticmethod
    def get_engine():
        return Engine()


class Controller:
    pass


def main():
    pass


if __name__ == "__main__":
    main()
