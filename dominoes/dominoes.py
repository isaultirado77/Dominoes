# Project: Dominoes

import random
import math
from abc import ABC, abstractmethod
from enum import Enum


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

    def clear_box(self) -> None:
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


class Engine:
    def __init__(self):
        self.box = Box()
        self.human = Human()
        self.bot = Computer()
        self.current_player = self.human
        self.snake = []
        self.game_state = GameState.IN_PROGRESS

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
            else:
                self.snake.append(human_snake)
                self.human.drop_piece(human_snake)
                self.switch_turn()

    def switch_turn(self) -> None:
        current_player_name = self.current_player.__str__()
        self.current_player = self.bot if current_player_name == 'Player' else self.human

    def clear_players_box(self) -> None:
        self.bot.clear_box()
        self.human.clear_box()

    def get_snake(self) -> str:
        return ''.join(str(segment) for segment in self.snake)

    def get_status(self) -> str:
        if self.game_state == GameState.GAME_OVER:
            if self.human.get_total_pieces() == 0:
                return 'The game is over. You won!'
            else:
                return 'The game is over. The computer won!'
        elif self.game_state == GameState.DRAW:
            return 'The game is over. It\'s a draw!'
        else:
            return self.current_player.get_move_msg()

    def display_player_pieces(self) -> None:
        pieces = self.human.get_pieces()
        print('Your pieces:')
        for i, piece in enumerate(pieces):
            print(f'{i + 1}:{piece}')
        print()

    def display_snake(self) -> None:
        length = len(self.snake)
        right_limit = length - 3
        if length > 6:
            left = self.snake[:3]
            right = self.snake[right_limit:]
            left_str = ''.join(str(item) for item in left)
            right_str = ''.join(str(item) for item in right)
            print(left_str + '...' + right_str + '\n')
        else:
            print(self.get_snake(), '\n')

    def display_interface(self) -> None:
        print('======================================================================')
        print('Stock size:', self.box.get_size())
        print('Computer pieces:', self.bot.get_total_pieces(), '\n')
        self.display_snake()
        self.display_player_pieces()
        print('Status:', self.get_status())

    def make_move(self) -> None:
        index, piece = self.current_player.move()
        if not index and not piece:  # Take a piece
            piece = self.box.give_piece()
            self.current_player.take_piece(piece)
        else:
            # Insert piece at the given index on the snake
            if index == 0:  # Insert at the left of the snake
                self.snake.insert(0, piece)
            else:  # Insert at the right of the snake
                self.snake.append(piece)
            # Drop piece from the current player stock
            self.current_player.drop_piece(piece)

    def change_game_state(self, state) -> None:
        self.game_state = state

    def is_win(self) -> bool:
        # Check if either the current player, human, or bot has no pieces left
        return self.human.get_total_pieces() == 0 or self.bot.get_total_pieces() == 0

    def is_draw(self):
        first = self.snake[0][0]
        last = self.snake[-1][-1]
        if first == last:
            count = 0
            for piece in self.snake:
                if first in piece:
                    count += 1
            return count == 8
        return False

    def check_game_state(self) -> None:
        if self.is_win():
            self.change_game_state(GameState.GAME_OVER)
        elif self.is_draw():
            self.change_game_state(GameState.DRAW)


class GameState(Enum):
    IN_PROGRESS = "The game is in progress."
    GAME_OVER = "The game is over."
    DRAW = "It's a draw."


class Controller:
    def __init__(self):
        self.engine = Engine()

    def run(self) -> None:
        self.engine.deal_dominoes()
        self.engine.get_first_player()
        self.engine.display_interface()

        while True:
            self.engine.make_move()
            self.engine.check_game_state()
            if self.engine.game_state == GameState.GAME_OVER:
                self.engine.display_interface()
                break
            self.engine.switch_turn()
            self.engine.display_interface()


def main():
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()
