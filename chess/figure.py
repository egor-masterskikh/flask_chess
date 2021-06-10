from chess.colors import WHITE


class Figure:
    def __init__(self, color):
        self.color = color

    def can_attack(self, board, row, col, row1, col1):
        # для пешки данный метод переопределен под взятие на проходе
        # для всех остальных фигур этот метод эквивалентен методу can_move данной фигуры
        return self.can_move(board, row, col, row1, col1)

    def can_move(self, board, row, col, row1, col1):
        return

    @staticmethod
    def is_king():
        return False

    @staticmethod
    def is_queen():
        return False

    @staticmethod
    def is_rook():
        return False

    @staticmethod
    def is_bishop():
        return False

    @staticmethod
    def is_knight():
        return False

    @staticmethod
    def is_pawn():
        return False

    def __str__(self):
        return 'w' if self.color == WHITE else 'b'
