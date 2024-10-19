from _collections import deque


class Error(Exception):
    """
    Base Error class for the dominoes.py module.
    """


class IllegalMoveError(Error):
    """
    Raise when an illegal tile is to be added to the snake.
    """


class DominoSnake(deque):
    def head(self) -> int:
        return self[0][0]

    def tail(self) -> int:
        return self[-1][-1]

    def append(self, tile) -> None:
        if len(self) > 0:
            if tile[0] == self.tail():
                pass
            elif tile[-1] == self.tail():
                tile.reverse()
            else:
                raise IllegalMoveError

        super().append(tile)

    def append_left(self, tile) -> None:
        if tile[-1] == self.head():
            pass
        elif tile[0] == self.head():
            tile.reverse()
        else:
            raise IllegalMoveError
        super().appendleft(tile)

    def to_list(self) -> list:
        return list(self)

    def __str__(self):
        if len(self) <= 6:
            return ''.join(f'{tile}' for tile in self)
        else:
            return f'{self[0]}{self[1]}{self[2]}...{self[-3]}{self[-2]}{self[-1]}'
