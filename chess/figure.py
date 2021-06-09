from chess.colors import WHITE
from chess.board import Board


class Figure:
    def __init__(self, color):
        self.color = color

    def can_attack(self, board: Board, row, col, row1, col1):
        # для пешки данный метод переопределен под взятие на проходе
        # для всех остальных фигур этот метод эквивалентен методу can_move данной фигуры
        return self.can_move(board, row, col, row1, col1)

    def can_move(self, board: Board, row, col, row1, col1):
        return

    def __str__(self):
        return 'w' if self.color == WHITE else 'b'
