from bishop import Bishop
from rook import Rook


class Queen(Rook, Bishop):
    def can_move(self, board, row, col, row1, col1):
        return (
                Bishop.can_move(self, board, row, col, row1, col1)
                or Rook.can_move(self, board, row, col, row1, col1)
        )

    def __str__(self):
        return super().__str__() + 'Q'
