from chess.bishop import Bishop
from chess.knight import Knight
from chess.queen import Queen
from chess.rook import Rook
from chess.pawn import Pawn
from chess.king import King
from chess.figure import Figure
from chess.colors import WHITE, BLACK, opponent
from itertools import product


class Board:
    SUCCESS_STATE = 0
    FAIL_STATE = 1
    CHECK_STATE = 2
    PAT_STATE = 3
    CHECKMATE_STATE = 4
    PROMOTE_PAWN_STATE = 5

    SIZE = 8

    def __init__(self):
        self.color = WHITE
        self.board = [
            [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
             King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)],
            [Pawn(WHITE)] * self.SIZE,
            [None] * self.SIZE,
            [None] * self.SIZE,
            [None] * self.SIZE,
            [None] * self.SIZE,
            [Pawn(BLACK)] * self.SIZE,
            [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
             King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]
        ]

    def __getitem__(self, row):
        return self.board[row]

    def __str__(self):
        sep_line = '-' * self.SIZE * 3
        fmt_board = [sep_line]

        for i in range(self.SIZE):
            fmt_board.append(''.join(
                ['|' + self.cell(i, j) for j in range(self.SIZE)] + ['|']
            ))
            fmt_board.append(sep_line)

        fmt_board = '\n'.join(fmt_board)

        return fmt_board

    def cell(self, row, col) -> str:
        """
        Возвращает строку из двух символов.
        Если в клетке (row, col) находится фигура, символы цвета и фигуры.
        Если клетка пуста, то два пробела.
        :return: str
        """
        return str(self[row][col] or '  ')

    def get_king_coords(self) -> tuple:
        """
        Возвращает текущие координаты короля текущего цвета
        :return: tuple
        """
        for row, col in product(range(self.SIZE), repeat=2):
            piece = self[row][col]
            if type(piece) == King and piece.color == self.color:
                return row, col

    def can_move(self, row, col, row1, col1) -> bool:
        if {row, col, row1, col1} - set(range(self.SIZE)):
            return False  # нельзя пойти вне доски

        if (row, col) == (row1, col1):
            return False  # нельзя пойти в ту же клетку

        piece = self[row][col]

        if piece is None:
            return False  # нельзя пойти из пустого места

        if piece.color != self.color:
            return False  # сейчас ходят фигуры другого цвета

        # не атака
        if self[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False

        # атака на фигуру противника
        elif self[row1][col1].color == opponent(piece.color):
            if not piece.can_attack(self, row, col, row1, col1):
                return False

        # атака на свою фигуру
        else:
            return False

        piece1 = self[row1][col1]

        # допускаем ход фигуры для проверки вскрытия короля
        self[row][col], self[row1][col1] = None, piece

        # эти переменные используются в случае рокировки
        castled_rook_col = None
        castled_rook_col1 = None
        castled_rook = None

        if type(piece) == King:
            # в случае рокировки возвращаем начальный и конечный индексы колонки ладьи
            castled_rook_cols = piece.can_castle(self, row, col, row1, col1)
            if castled_rook_cols:
                castled_rook_col, castled_rook_col1 = castled_rook_cols
                castled_rook = self[row][castled_rook_col]

                # помимо хода короля допускаем также ход ладьи
                self[row][castled_rook_col], self[row][castled_rook_col1] = (
                    None, castled_rook
                )

        if self.check():
            king_is_protected = False
        else:
            king_is_protected = True

        # ставим фигуру обратно
        self[row][col], self[row1][col1] = piece, piece1

        # если мы допустили рокировку, то помимо короля ставим обратно и ладью
        if castled_rook:
            self[row][castled_rook_col], self[row][castled_rook_col1] = castled_rook, None

        return king_is_protected

    def check(self) -> bool:
        """
        Проверяет нохождение короля текущего цвета под шахом
        :return: bool
        """
        king_row, king_col = self.get_king_coords()
        for row, col in product(range(self.SIZE), repeat=2):
            piece = self[row][col]
            if (
                    isinstance(piece, Figure)
                    and piece.color == opponent(self.color)
                    and piece.can_attack(self, row, col, king_row, king_col)
            ):
                return True

        return False

    def pat(self) -> bool:
        """
        Проверяет, может ли хоть одна фигура текущего цвета сделать ход
        :return: bool
        """
        for row, col in product(range(self.SIZE), repeat=2):
            piece = self[row][col]
            if isinstance(piece, Figure) and piece.color == self.color:
                for row1, col1 in product(range(self.SIZE), repeat=2):
                    if self.can_move(row, col, row1, col1):
                        return False
        return True

    def checkmate(self) -> bool:
        return self.check() and self.pat()

    def promote_pawn(self, row, col, row1, col1, char):
        """
        Превращает пешку в ферзя, слона, ладью или коня
        """
        if char == 'Q':
            piece = Queen(self.color)
        elif char == 'B':
            piece = Bishop(self.color)
        elif char == 'N':
            piece = Knight(self.color)
        elif char == 'R':
            piece = Rook(self.color)
        else:
            return False

        self[row][col], self[row1][col1] = None, piece

        return True

    def move(self, row, col, row1, col1):
        """
        Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт SUCCESS_STATE.
        Если нет - вернёт FAIL_STATE
        """
        if self.can_move(row, col, row1, col1):
            piece = self[row][col]

            # делаем ход
            self[row][col], self[row1][col1] = None, piece

            if type(piece) in (Rook, King):
                # помечаем, что рокировка с этой фигурой невозможна
                piece.moved = True
                if type(piece) == King:
                    # в случае рокировки возвращаем
                    # начальный и конечный индексы колонки ладьи
                    castled_rook_cols = piece.can_castle(self, row, col, row1, col1)
                    if castled_rook_cols:
                        castled_rook_col, castled_rook_col1 = castled_rook_cols
                        castled_rook = self[row][castled_rook_col]

                        # в случае рокировки делаем ход ещё и ладьёй
                        self[row][castled_rook_col], self[row][castled_rook_col1] = (
                            None, castled_rook
                        )

            elif type(piece) == Pawn:
                if (piece.color == BLACK and row1 == 0
                        or piece.color == WHITE and row1 == 7):
                    return self.PROMOTE_PAWN_STATE

            self.color = opponent(self.color)

            if self.checkmate():
                return self.CHECKMATE_STATE
            elif self.pat():
                return self.PAT_STATE
            elif self.check():
                return self.CHECK_STATE

            return self.SUCCESS_STATE

        return self.FAIL_STATE
