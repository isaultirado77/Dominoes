from tile_set import TileSet
from player import Computer, Human
from domino_snake import DominoSnake, IllegalMoveError
from constants import DominoEnd, GameState


class GameEngine:
    def __init__(self):
        self.tile_set = TileSet()
        self.snake = DominoSnake
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

        while not human_snake or not computer_snake:
            self.tile_set.reset_tile_set()
            self.clear_players_tile_set()
            self.deal_dominoes()
            human_snake = self.human.get_snake_tile()
            computer_snake = self.computer.get_snake_tile()

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


class GameController:
    pass
