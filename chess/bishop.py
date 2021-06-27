from chess.figure import Figure
from math import copysign


class Bishop(Figure):
    def can_move(self, board, row, col, row1, col1):
        if abs(row - row1) != abs(col - col1):
            return False  # слон двигается только по диагонали

        step_row = int(copysign(1, row1 - row))
        step_col = int(copysign(1, col1 - col))

        # проверка отсутствия фигур на пути
        for i in range(1, abs(row1 - row)):
            if board[row + step_row * i][col + step_col * i] is not None:
                return False

        return True

    def __str__(self):
        return super().__str__() + 'B'
