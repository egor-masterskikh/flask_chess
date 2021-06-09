from chess.figure import Figure


class King(Figure):
    def __init__(self, color):
        self.moved = False
        super().__init__(color)

    def can_move(self, board, row, col, row1, col1):
        if (row, col) == (row1, col1):
            return False

        # проверка хода короля максимум на один шаг по всем осям
        return not ({abs(row1 - row), abs(col1 - col)} - {0, 1})

    def __str__(self):
        return super().__str__() + 'K'
