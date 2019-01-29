from src.piece import Piece
import re
# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

def fromFEN(fen):
    # assuming good FEN
    # TODO: check FEN form (regex?)
    parts = fen.split(' ')
    ranks = parts[0].split('/')
    board = []
    for r in range(0, len(ranks)):
        rank = ranks[r]
        row = []
        _y = r
        for s in range(0, len(rank)):
            sq = rank[s]
            _x = s
            if(re.match(r"\d", sq)):
                num_spaces = int(sq)
                for i in range(0, num_spaces):
                    _x = i
                    row.append({ '_x': _x, '_y': _y, 'piece': None })
            elif(sq.isupper()):
                row.append({ '_x': _x, '_y': _y, 'piece': { 'color': 'w', 'role': sq.lower() } })
            else:
                row.append({ '_x': _x, '_y': _y, 'piece': { 'color': 'b', 'role': sq } })
        board.append(row)
    return board

def toPieces(fen):
    ranks = fen.split('/')