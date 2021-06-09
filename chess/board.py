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
    CHECK_STATE, PAT_STATE, CHECKMATE_STATE = range(3)
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
            return False

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

        return True

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

    def castle(self, row, col, row1, col1):
        # TODO: перенести метод castle в метод короля проверки хода
        if row != row1 or abs(col - col1) != 2:
            return False
        king = self[row][col]
        if not isinstance(king, King):
            return False
        rook_col = 0 if col1 == 2 else 7
        rook = self[row][rook_col]
        if not isinstance(rook, Rook) or isinstance(rook, Queen):
            return False
        if rook.moved or king.can_castle:
            return False
        if rook_col == 7 and self[row][5:7] != [None, None]:
            return False
        if rook_col == 0 and self[row][1:4] != [None, None, None]:
            return False
        if self.check(row, col):
            return False
        # наконец можно рокироваться
        self[row][col], self[row][col1] = None, king
        if rook_col == 7:
            self[row][rook_col], self[row][5] = None, rook
        else:
            self[row][rook_col], self[row][3] = None, rook
        king.can_castle, rook.moved = True, True
        self.kings_coords[self.color] = row, col1
        self.color = opponent(self.color)
        return True

    def move(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет - вернёт False"""
        piece = self[row][col]
        piece1 = self[row1][col1]

        if self.can_move(row, col, row1, col1):
            self[row][col], self[row1][col1] = None, piece

            if isinstance(piece, King):
                king_row, king_col = row1, col1
            else:
                king_row, king_col = self.kings_coords[self.color]

            if self.check(king_row, king_col):
                self[row][col], self[row1][col1] = piece, piece1
                return False

            # если передвинули ладью или короля, то помечаем,
            # что эта фигура уже двигалась и рокировка с этой фигурой невозможна
            if isinstance(piece, Rook) and not isinstance(piece, Queen):
                piece.moved = True
            elif isinstance(piece, King):
                piece.moved = True
                # перезаписываем текущие координаты короля
                self.kings_coords[self.color] = row1, col1

            if (
                    isinstance(piece, Pawn)
                    and (piece.color == BLACK and row1 == 0
                         or piece.color == WHITE and row1 == 7)
            ):
                pass
                # TODO: отправить статус, что возможно провести пешку

            self.color = opponent(self.color)

            if self.checkmate():
                return self.CHECKMATE_STATE
            elif self.pat():
                return self.PAT_STATE
            elif self.check():
                return self.CHECK_STATE

            return True

        return False
