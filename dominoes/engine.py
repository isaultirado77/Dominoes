from enum import Enum
from collections import deque
from box import Box
from player import Human, Computer


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
        length = len(self.snake)
        right_limit = length - 3
        if length > 6:
            left = self.snake[:3]
            right = self.snake[right_limit:]
            left_str = ''.join(str(item) for item in left)
            right_str = ''.join(str(item) for item in right)
            print(left_str + '...' + right_str + '\n')
        else:
            print(self.get_snake_as_string(), '\n')

    def make_move(self):
        pass

    def validate_move(self):
        pass

    def flip_piece(self):
        pass

    def check_game_state(self) -> None:
        if self.is_win():
            self.change_game_state(GameState.GAME_OVER)
        elif self.is_draw():
            self.change_game_state(GameState.DRAW)

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

    def change_game_state(self, state) -> None:
        self.game_state = state


class GameState(Enum):
    IN_PROGRESS = "The game is in progress."
    GAME_OVER = "The game is over."
    DRAW = "It's a draw."
