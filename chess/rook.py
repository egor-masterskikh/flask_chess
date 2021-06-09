from chess.board import Board
from chess.figure import Figure
from math import copysign


class Rook(Figure):
    def __init__(self, color):
        self.moved = False
        super().__init__(color)

    def can_move(self, board: Board, row, col, row1, col1):
        if (row, col) == (row1, col1):
            return False

        if not (row == row1 or col == col1):
            return False

        row_step = int(copysign(1, row1 - row))
        # проверка отсутствия фигур на пути по вертикали
        for i in range(row + row_step, row1, row_step):
            if board[i][col] is not None:
                return False

        col_step = int(copysign(1, col1 - col))
        # проверка отсутствия фигур на пути по горизонтали
        for j in range(col + col_step, col1, col_step):
            if board[row][j] is not None:
                return False

        return True

    def __str__(self):
        return super().__str__() + 'R'
