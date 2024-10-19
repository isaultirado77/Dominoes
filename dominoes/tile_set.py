from random import choice


class TileSet:
    def __init__(self):
        self.tile_set = []  # Storage the pieces
        self.generate_tile_set()

    def generate_tile_set(self) -> None:
        for i in range(7):  # 'i' points to the left number on the piece
            for j in range(i, 7):  # 'j' points to the right number on the piece
                tile = [i, j]
                self.tile_set.append(tile)

    def display_tile_set(self) -> None:
        print(self.tile_set)

    def give_tile(self) -> list:
        if len(self.tile_set) > 0:
            tile = choice(self.tile_set)
            self.tile_set.remove(tile)
            return tile

    def reset_box(self) -> None:
        self.tile_set.clear()
        self.generate_tile_set()

    def get_size(self) -> int:
        return len(self.tile_set)
