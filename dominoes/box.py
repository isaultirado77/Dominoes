import random


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
