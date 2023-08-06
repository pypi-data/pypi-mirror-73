EMPTY = 0
CYAN = 1
VIOLET = 2

MARKS = (' ', '♙', '♟')

# These globals should be accessed only by using Board instance variables
_NROWS = None             # pragma: no mutate
_COLS = None              # pragma: no mutate
_WELL_FORMED_MOVES = None # pragma: no mutate

def init_board_params(ncols, nrows=3):
    """Init globals used for Board instantiation."""
    global _NROWS, _COLS, _WELL_FORMED_MOVES
    COL_NAMES = ('V', 'W', 'X', 'Y', 'Z')
    _NROWS = nrows
    _COLS = tuple(COL_NAMES[-ncols:])
    _WELL_FORMED_MOVES = []
    for i in _COLS:
        for j in _COLS:
            if abs(ord(i) - ord(j)) <= 1:
                _WELL_FORMED_MOVES.append(i+j)
    _WELL_FORMED_MOVES = tuple(_WELL_FORMED_MOVES)

def other(player):
    """Return opposite color. """
    if player == VIOLET:
        return CYAN
    if player == CYAN:
        return VIOLET
    return EMPTY

def pawns_to_code(pawns_dict):
    """Return an alphanumeric representation of a board for ease board matching.

    The code is a string of alphanumeric digits representing columns,
    therefore a flipped board has exactly the reverse code.

    """
    r = ''
    DIGITS="0123456789ABCDEFGHIJKLMNOPQ"
    base = VIOLET+1
    assert len(DIGITS) == base**3, len(DIGITS) # pragma: no mutate
    for c in sorted(pawns_dict.keys()):
        n = 0
        for i, p in enumerate(pawns_dict[c]):
            n += p * base**i
        r += DIGITS[n]
    return r.upper()


class Board:
    """All the Boards in a program must have the same number of columns and rows.
    """

    def __init__(self, code=None):
        assert _COLS is not None, "Board params not initialized" # pragma: no mutate

        def pawns_from_code(h):
            """Return a dict corresponding to code digits.
            """
            assert len(self.COLS) == len(h) # pragma: no mutate
            r = {}
            base = VIOLET + 1
            for i, c in enumerate(self.COLS):
                col = []
                n = int(h[i], base=base**3)
                for j in range(self.NROWS):
                    col.append(n % base)
                    n = n // base
                r[c] = tuple(col)

            return r

        self.WELL_FORMED_MOVES = _WELL_FORMED_MOVES
        self.COLS = _COLS
        self.NROWS = _NROWS
        if code is None:
            self.pawns = pawns_from_code('B'*len(self.COLS))
        else:
            self.pawns = pawns_from_code(code)

    def __str__(self, m=MARKS):
        """Return a string representation for the board.

        It uses Unicode code points for 'WHITE CHESS PAWN' and 'BLACK CHESS PAWN'.
        """

        def add_hline(line):
            line = line + ' '
            for _ in self.COLS:
                line = line + '+---'
            line = line + '+\n'
            return line


        s = '\n '
        for c in self.COLS:
            s = s + '  ' + c + ' '
        s = add_hline(s + ' \n')

        for r in range(self.NROWS):
            for c in self.COLS:
                s = s + ' | {}'.format(m[self[c][r]])
            s = s + ' |\n'
            s = add_hline(s)
        s = s + 'Board code: {}\n'.format(self.__hash__())
        return s

    def __eq__(self, other_board):
        return self.__hash__() == other_board.__hash__()

    def __hash__(self):
        return pawns_to_code(self.pawns)

    def __getitem__(self, col):
        return self.pawns[col]

    def __setitem__(self, col, value):
        raise TypeError("'Board' objects are immutable!")


    def flip(self):
        """Return a board with the columns flipped.
        """
        return Board(self.__hash__()[::-1])

    @classmethod
    def flip_move(cls, move):
        """Return a flipped move, i.e. the move according to the board with flipped colums.
        """
        r = ''
        for c in move:
            for i, k in enumerate(_COLS):
                if c == k:
                    r = r + _COLS[-(i+1)]
        return r

    def exchange(self):
        """Return a board with players exchanged as if VIOLET played as CYAN and viceversa.
        """
        b = {}
        for c in self.COLS:
            b[c] = [EMPTY, EMPTY, EMPTY]
            for i, p in enumerate(self[c][::-1]):
                b[c][i] = other(p)
            b[c] = tuple(b[c])
        return Board(pawns_to_code(b))

    def can_move_fwd(self, player, column):
        """True if player can move forward in column.
        """
        if player == VIOLET:
            for row in range(self.NROWS-1):
                if self[column][row] == VIOLET and self[column][row+1] == EMPTY:
                    return True
            return False
        else:
            return self.exchange().can_move_fwd(VIOLET, column)

    def can_capture(self, player, column):
        """True if player can move diagonally from column and capture a pawn of the other color.
        """
        if player == VIOLET:
            if column == self.COLS[0]:
                for row in range(_NROWS-1):
                    if self[self.COLS[0]][row] == VIOLET and self[self.COLS[1]][row + 1] == CYAN:
                        return True
            elif column == self.COLS[-1]:
                return self.flip().can_capture(VIOLET, self.COLS[0])
            else:
                c = _COLS.index(column)
                for row in range(self.NROWS-1):
                    if self[column][row] == VIOLET and (self[self.COLS[c-1]][row + 1] == CYAN
                                                        or self[self.COLS[c+1]][row + 1] == CYAN):
                        return True
            return False
        else:
            return self.exchange().can_capture(VIOLET, column)

    def is_winner(self, player):
        """True if player is winning. """
        if player == VIOLET:
            opponent_moves = 0
            for c in self.COLS:
                if self[c][-1] == VIOLET:
                    return True
                if self.can_move_fwd(CYAN, c) or self.can_capture(CYAN, c):
                    opponent_moves += 1
            return opponent_moves == 0
        return self.exchange().is_winner(VIOLET)

    class IllegalMoveError(Exception):
        pass


    def move(self, player, start, end):
        """Return a board in which player has moved from columns start to column end.

        Raise an exception if the move is not legal.
        """
        assert start+end in self.WELL_FORMED_MOVES # pragma: no mutate

        b = {}
        for c in self.COLS:
            b[c] = self[c]

        if player == VIOLET:
            if start == end and not self.can_move_fwd(VIOLET, start):
                raise IllegalMoveError("{} cannot move forward on column {}".format(VIOLET, start))
            if start == end:
                assert self.can_move_fwd(VIOLET, start) # pragma: no mutate
                b[start] = list(self[start])
                i = len(b[start]) - 1 - b[start][::-1].index(VIOLET)
                b[start][i] = EMPTY
                b[start][i + 1] = VIOLET
                b[start] = tuple(b[start])
                return Board(pawns_to_code(b))

            assert self.can_capture(VIOLET, start) # pragma: no mutate

            def capture(bdict, from_row, to_row):
                if self[start][from_row] == VIOLET and self[end][to_row] == CYAN:
                    bdict[start] = list(self[start])
                    bdict[end] = list(self[end])
                    bdict[start][from_row] = EMPTY
                    bdict[end][to_row] = VIOLET
                    bdict[start] = tuple(bdict[start])
                    bdict[end] = tuple(bdict[end])
                    return Board(pawns_to_code(bdict))
                return None

            for row in range(self.NROWS-1):
                r = capture(b, row, row + 1)
                if r is not None:
                    return r

            raise Exception("No move is possible!")
        else:
            return self.exchange().move(VIOLET, start, end).exchange()

    def is_symmetrical(self):
        """True if board is symmetric."""
        return self == self.flip()


    def get_legal_moves(self, player):
        """Return a list of all legal moves for player in a given board position."""
        r = []
        for m in self.WELL_FORMED_MOVES:
            try:
                self.move(player, m[0], m[1])
                r.append(m)
            except:
                pass
        return r

    @classmethod
    def prune_sym_moves(cls, moves):
        if len(moves) <= 1:
            return moves
        if cls.flip_move(moves[0]) in moves[1:]:
            return cls.prune_sym_moves(moves[1:])
        return cls.prune_sym_moves(moves[1:]) + [moves[0]]

    @classmethod
    def get_forest(cls):
        """Return a string with a LaTeX (tikz, forest) representation of the game tree and the set of unique boards.

        Boards are returned as a dictionary with the lists of turns in which each appears.
        """

        boards = {}

        def get_tree(board, player, turn, a_move, indent):
            code = board.__hash__()
            if board.is_winner(other(player)):
                s = "{}[{},winner{},move={{{}}}{{{}}}]".format(indent, code,
                                                               other(player),
                                                               other(player), a_move.lower())
                return s, other(player)
            moves = board.get_legal_moves(player)
            if board.is_symmetrical():
                moves = cls.prune_sym_moves(moves)
            if code in boards:
                for m in moves:
                    boards[code][1].add(m)
            elif code[::-1] in boards:
                for m in moves:
                    boards[code[::-1]][1].add(cls.flip_move(m))
            else:
                boards[code] = (turn, set(moves))
            s = "{}[{},winner@".format(indent, code)
            if a_move != None:
                s = s + ",move={{{}}}{{{}}},winner@".format(other(player), a_move.lower())
            s = s + "\n"
            winners = []
            for m in moves:
                b = board.move(player, m[0], m[1])
                t, w = get_tree(b, other(player), turn+1, m, indent + " ")
                s = s + t + "\n"
                winners.append(w)
            if len(set(winners)) == 1:
                winner = winners[0]
            else:
                winner = player
            s = s.replace('@', str(winner))
            return s + indent + "]", winner

        f = """
%% Game tree for LEX --- Learning EX-a-pawn
%% Uncomment the lines which begin with % for a standalone LaTeX document
%\\documentclass[tikz]{standalone}
%\\usepackage{forest}
%\\begin{document}

\\forestset{
  default preamble={
    for tree={font=\\tiny}
  }
}
\\begin{forest}
  winner1/.style={draw,fill=cyan,inner sep=1pt,outer sep=0},
  winner2/.style={draw,fill=violet!60,inner sep=1pt,outer sep=0},
  move/.style n args=2{%
    if={#1<2}%
    {edge label/.expanded={%
      node [midway,fill=white,text=cyan,font=\\unexpanded{\\tiny}] {$#2$}%
    }}{edge label/.expanded={%
      node [midway,fill=white,text=violet!60,font=\\unexpanded{\\tiny}] {$#2$}%
    }},
  }
"""
        t, _ = get_tree(Board(), CYAN, 1, None, " ")
        f = f + t
        f = f + "\n\\end{forest}"
        f = f + "\n%\\end{document}"

        for h in boards:
            b = Board(h)
            if b.is_symmetrical():
                moves = cls.prune_sym_moves(list(boards[h][1]))
                boards[h] = (boards[h][0], set(moves))

        return f, boards
