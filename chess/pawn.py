from chess.figure import Figure
from chess.colors import WHITE
from chess.board import Board


class Pawn(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.direction = 1 if self.color == WHITE else -1
        self.start_row = 1 if self.color == WHITE else 6

    def can_move(self, board: Board, row, col, row1, col1):
        if (row, col) == (row1, col1):
            return False

        if col != col1:
            return False

        # ход на 1 клетку
        if row + self.direction == row1:
            return True

        # ход на 2 клетки
        if (
                row == self.start_row
                and row + 2 * self.direction == row1
                and board[row + self.direction][col] is None
        ):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        """Проверяется возможность взятия на проходе"""
        return row + self.direction == row1 and abs(col1 - col) == 1

    @staticmethod
    def is_pawn():
        return True

    def __str__(self):
        return super().__str__() + 'P'
