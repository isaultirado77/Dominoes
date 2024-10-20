from tile_set import TileSet
from player import Computer, Human
from domino_snake import DominoSnake, IllegalMoveError
from constants import GameState, DominoEnd


class GameEngine:
    def __init__(self):
        self.tile_set = TileSet()
        self.snake = DominoSnake()
        self.human = Human()
        self.computer = Computer()
        self.current_player = self.human
        self.game_state = GameState.IN_PROGRESS

    def deal_dominoes(self) -> None:
        for i in range(7):
            self.human.take_tile(self.tile_set.give_tile())
            self.computer.take_tile(self.tile_set.give_tile())

    def get_first_player(self):
        human_snake = self.human.get_snake_tile()
        computer_snake = self.computer.get_snake_tile()

        if not human_snake or not computer_snake:
            self.tile_set.reset_tile_set()
            self.clear_players_tile_set()
            self.deal_dominoes()
            self.get_first_player()
        else:
            if sum(computer_snake) > sum(human_snake):
                self.snake.append(computer_snake)
                self.computer.drop_tile(computer_snake)
            else:
                self.snake.append(human_snake)
                self.human.drop_tile(human_snake)
                self.switch_turn()

    def clear_players_tile_set(self) -> None:
        self.computer.clear_hand_tiles()
        self.human.clear_hand_tiles()

    def switch_turn(self) -> None:
        current_player_name = self.current_player.__str__()
        self.current_player = self.computer if current_player_name == 'Human' else self.human

    def display_interface(self) -> None:
        print('======================================================================')
        print('Stock size:', self.tile_set.get_set_size())
        print('Computer pieces:', self.computer.get_amount_of_tiles(), '\n')
        print(self.snake)
        self.display_player_tiles()
        print('Status:', self.get_game_status_message())

    def get_game_status_message(self):
        if self.game_state == GameState.GAME_OVER:
            if self.human.get_amount_of_tiles() == 0:
                return 'The game is over. You won!'
            else:
                return 'The game is over. The computer won!'
        elif self.game_state == GameState.DRAW:
            return 'The game is over. It\'s a draw!'
        else:
            return self.current_player.get_move_msg()

    def display_player_tiles(self) -> None:
        pieces = self.human.get_hand_tiles()
        print('\nYour pieces:')
        for i, piece in enumerate(pieces):
            print(f'{i + 1}:{piece}')
        print()

    def make_move(self):
        while True:
            domino_end, tile = self.current_player.move(self.snake)

            if not domino_end and not tile:  # Pass turn
                self.pass_turn()
                return

            try:
                if domino_end == DominoEnd.HEAD:
                    self.snake.append_head(tile)
                else:
                    self.snake.append_tail(tile)

                self.current_player.drop_tile(tile)
                return
            except IllegalMoveError:
                print('\nIllegal move. Please try again.')

    def pass_turn(self) -> None:
        tile = self.tile_set.give_tile()
        self.current_player.take_tile(tile)

    def check_game_state(self) -> None:
        if self.is_win():
            self.change_game_state(GameState.GAME_OVER)
        elif self.is_draw():
            self.change_game_state(GameState.DRAW)

    def is_win(self) -> bool:
        # Check if either the current player, human, or bot has no pieces left
        return self.human.get_amount_of_tiles() == 0 or self.computer.get_amount_of_tiles() == 0

    def is_draw(self) -> bool:
        if self.snake.head() == self.snake.tail():
            count = sum(piece.count(self.snake.head()) for piece in self.snake)

            if count >= 8:
                return True

        return False

    def change_game_state(self, state) -> None:
        self.game_state = state


class GameController:
    def __init__(self):
        self.engine = GameEngine()

    def run(self) -> None:
        self.engine.deal_dominoes()
        self.engine.get_first_player()
        self.engine.display_interface()

        while True:
            self.engine.make_move()
            self.engine.check_game_state()
            if self.engine.game_state in (GameState.GAME_OVER, GameState.DRAW):
                self.engine.display_interface()
                break
            self.engine.switch_turn()
            self.engine.display_interface()
