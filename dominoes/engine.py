from enum import Enum
from collections import deque
from itertools import islice
from box import Box
from player import Human, Computer


def flip_piece(piece):
    return [piece[1], piece[0]]


class Engine:
    def __init__(self):
        self.box = Box()
        self.snake = deque()  # Snake uses a Deque as data structure
        self.human = Human()
        self.bot = Computer()
        self.current_player = self.human
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

    def clear_players_box(self) -> None:
        self.bot.clear_pieces()
        self.human.clear_pieces()

    def switch_turn(self) -> None:
        current_player_name = self.current_player.__str__()
        self.current_player = self.bot if current_player_name == 'Player' else self.human

    def get_snake_as_string(self) -> str:
        return ''.join(str(segment) for segment in self.snake)

    def display_interface(self) -> None:
        print('======================================================================')
        print('Stock size:', self.box.get_size())
        print('Computer pieces:', self.bot.get_total_pieces(), '\n')
        self.display_snake()
        self.display_player_pieces()
        print('Status:', self.get_game_status_message())

    def get_game_status_message(self):
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
        left, right = self.get_left_right_slices()
        if right:
            left_str = ''.join(str(item) for item in left)
            right_str = ''.join(str(item) for item in right)
            print(left_str + '...' + right_str + '\n')
        else:
            print(self.get_snake_as_string(), '\n')

    def get_left_right_slices(self):
        length = len(self.snake)
        if length <= 6:
            return list(self.snake), []  # If length <= 6, don't slice
        left = list(islice(self.snake, 3))  # Left side
        right = list(islice(self.snake, length - 3, length))  # Right side
        return left, right

    def make_move(self) -> None:
        if isinstance(self.current_player, Human):
            self.handle_human_move()
        else:
            self.handle_bot_move()

    def handle_human_move(self) -> None:
        while True:
            index, piece = self.current_player.move()

            if not index and not piece:  # Pass turn
                self.pass_turn()
                return

            if self.is_valid_move(index, piece):
                self.place_piece(index, piece)
                return
            else:
                print('\nIllegal move. Please try again.')

    def handle_bot_move(self) -> None:
        index, piece = self.current_player.move(self.snake)

        if not index and not piece:  # Pass turn
            self.pass_turn()
            return

        if self.is_valid_move(index, piece):
            self.place_piece(index, piece)
            return
        else:
            print('\nComputer illegal move.\n')

    def pass_turn(self) -> None:
        piece = self.box.give_piece()
        self.current_player.take_piece(piece)

    def place_piece(self, index: int, piece: list) -> None:
        flipped = False
        # Place piece on left side
        if index < 0:
            if piece[1] != self.snake[0][0]:
                piece = flip_piece(piece)
                flipped = True
            self.snake.appendleft(piece)

        else:
            if piece[0] != self.snake[-1][-1]:
                piece = flip_piece(piece)
                flipped = True
            self.snake.append(piece)

        if flipped:
            piece = flip_piece(piece)
        self.current_player.drop_piece(piece)

    def is_valid_move(self, index: int, piece: list) -> bool:
        if index < 0:  # Move on left side
            return piece[1] == self.snake[0][0] or piece[0] == self.snake[0][0]
        elif index > 0:  # Move on right side
            return piece[0] == self.snake[-1][-1] or piece[1] == self.snake[-1][-1]

    def check_game_state(self) -> None:
        if self.is_win():
            self.change_game_state(GameState.GAME_OVER)
        elif self.is_draw():
            self.change_game_state(GameState.DRAW)

    def is_win(self) -> bool:
        # Check if either the current player, human, or bot has no pieces left
        return self.human.get_total_pieces() == 0 or self.bot.get_total_pieces() == 0

    def is_draw(self) -> bool:
        first = self.snake[0][0]
        last = self.snake[-1][-1]

        if first == last:
            count = sum(piece.count(first) for piece in self.snake)

            if count >= 8:
                return True

        return False

    def change_game_state(self, state) -> None:
        self.game_state = state


class GameState(Enum):
    IN_PROGRESS = "The game is in progress."
    GAME_OVER = "The game is over."
    DRAW = "It's a draw."
