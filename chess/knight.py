from chess.figure import Figure


class Knight(Figure):
    def can_move(self, board, row, col, row1, col1):
        # проверка хода буквой Г
        return {abs(row1 - row), abs(col1 - col)} == {1, 2}

    @staticmethod
    def is_knight():
        return True

    def __str__(self):
        return super().__str__() + 'N'
