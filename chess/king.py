from chess.figure import Figure
from chess.rook import Rook


class King(Figure):
    def __init__(self, color):
        self.moved = False
        super().__init__(color)

    def can_move(self, board, row, col, row1, col1):
        # проверка хода короля максимум на один шаг по всем осям
        if not {abs(row1 - row), abs(col1 - col)} - {0, 1}:
            return True

        if self.can_castle(board, row, col, row1, col1):
            return True

        return False

    def can_castle(self, board, row, col, row1, col1):
        if row != row1 or abs(col - col1) != 2:
            return False

        if col1 == 2:
            rook_col = 0
            rook_col1 = 3
        else:  # elif col1 == 6:
            rook_col = 7
            rook_col1 = 5

        rook = board[row][rook_col]

        if type(rook) != Rook:
            return False

        if rook.moved or self.moved:
            return False

        if rook_col == 7 and board[row][5:7] != [None] * 2:
            return False

        if rook_col == 0 and board[row][1:4] != [None] * 3:
            return False

        return rook_col, rook_col1

    def __str__(self):
        return super().__str__() + 'K'
