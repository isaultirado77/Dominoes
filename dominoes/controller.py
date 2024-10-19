from engine import Engine, GameState


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
            if self.engine.game_state in (GameState.GAME_OVER, GameState.DRAW):
                self.engine.display_interface()
                break
            self.engine.switch_turn()
            self.engine.display_interface()
