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
        # координаты королей нужны для отслеживания шаха, мата и пата
        self.kings_coords = {BLACK: (7, 4), WHITE: (0, 4)}

    def __getitem__(self, item):
        return self.board[item]

    def __str__(self):
        fmt_board = '-' * self.SIZE * 4
        for i in range(self.SIZE):
            fmt_board += ''.join(['|' + self.cell(i, j) + '|' for j in range(self.SIZE)])
        fmt_board += '-' * self.SIZE * 4
        return fmt_board

    def cell(self, row, col):
        """
        Возвращает строку из двух символов.
        Если в клетке (row, col) находится фигура, символы цвета и фигуры.
        Если клетка пуста, то два пробела.
        """
        return str(self[row][col] or '  ')

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
        king_is_protected = True

        # допускаем ход фигуры для проверки вскрытия короля
        self[row][col], self[row1][col1] = None, piece

        if piece.is_king():
            king_row, king_col = row1, col1

            # если король хочет сделать рокировку,
            # то возвращаем ему начальный и конечный индексы колонки ладьи
            rook_cols = piece.can_castle(self, row, col, row1, col1)
            if rook_cols:
                rook_col, rook_col1 = rook_cols
                rook = self[row][rook_col]
                self[row][rook_col], self[row][rook_col1] = None, rook

        else:
            king_row, king_col = self.kings_coords[self.color]

        if self.check(king_row, king_col):
            king_is_protected = False

        self[row][col], self[row1][col1] = piece, piece1

        # TODO: в случае рокировки надо поставить ладью на место

        return king_is_protected

    def check(self, king_row=None, king_col=None) -> bool:
        if not king_row and not king_col:
            king_row, king_col = self.kings_coords[self.color]

        for i, j in product(range(self.SIZE), repeat=2):
            p = self[i][j]
            if (
                    isinstance(p, Figure)
                    and p.color == opponent(self.color)
                    and p.can_attack(self, i, j, king_row, king_col)
            ):
                return True

        return False

    def pat(self) -> bool:
        for i, j in product(range(self.SIZE), repeat=2):
            piece = self[i][j]
            if isinstance(piece, Figure) and piece.color == self.color:
                for i1, j1 in product(range(self.SIZE), repeat=2):
                    if self.can_move(i, j, i1, j1):
                        return False
        return True

    def checkmate(self) -> bool:
        return self.check() and self.pat()

    def promote_pawn(self, row, col, row1, col1, char):
        """Превращение пешки в ферзя, слона, ладью или коня"""
        if char in ('Q', 'B', 'N', 'R'):
            self[row][col] = None

            if char == 'Q':
                self[row1][col1] = Queen(self.color)
            elif char == 'B':
                self[row1][col1] = Bishop(self.color)
            elif char == 'N':
                self[row1][col1] = Knight(self.color)
            elif char == 'R':
                self[row1][col1] = Rook(self.color)

            return True

        return False

    def move(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет - вернёт False"""
        if self.can_move(row, col, row1, col1):
            piece = self[row][col]
            # если передвинули ладью или короля, то помечаем,
            # что эта фигура уже двигалась и рокировка с ней невозможна
            if piece.is_rook() or piece.is_king():
                piece.moved = True
                if piece.is_king():
                    # TODO: в случае рокировки ставим ладью на своё место
                    # перезаписываем текущие координаты короля
                    self.kings_coords[self.color] = row1, col1

            elif (piece.is_pawn() and (
                    piece.color == BLACK and row1 == 0
                    or piece.color == WHITE and row1 == 7
            )):
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
