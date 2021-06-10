from chess.board import Board
from chess.figure import Figure


class King(Figure):
    def __init__(self, color):
        self.moved = False
        super().__init__(color)

    def can_move(self, board, row, col, row1, col1):
        if (row, col) == (row1, col1):
            return False

        # проверка хода короля максимум на один шаг по всем осям
        if {abs(row1 - row), abs(col1 - col)} - {0, 1}:
            return False

        return True

    def can_castle(self, board: Board, row, col, row1, col1):
        if row != row1 or abs(col - col1) != 2:
            return False

        rook_col = 0 if col1 == 2 else 7
        rook = board[row][rook_col]

        if not rook.is_rook():
            return False

        if rook.moved or self.moved:
            return False

        if rook_col == 7 and board[row][5:7] != [None] * 2:
            return False

        if rook_col == 0 and board[row][1:4] != [None] * 3:
            return False

        if board.check(row, col):
            return False

        return True

    @staticmethod
    def is_king():
        return True

    def __str__(self):
        return super().__str__() + 'K'
