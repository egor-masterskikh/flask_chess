from chess.bishop import Bishop
from chess.rook import Rook
from chess.figure import Figure


class Queen(Rook, Bishop):
    def can_move(self, board, row, col, row1, col1):
        return (
                Bishop.can_move(self, board, row, col, row1, col1)
                or Rook.can_move(self, board, row, col, row1, col1)
        )

    def __str__(self):
        return Figure.__str__(self) + 'Q'
