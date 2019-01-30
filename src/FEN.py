from src.piece import Piece
import re

def fromFEN(fen):
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
                    row.append(get_square_props(_x, _y))
            else:
                row.append(get_square_props(_x, _y, sq))
        board.append(row)
    return board

def get_square_props(_x, _y, role=None):
    square_props = { 
        '_x': _x, 
        '_y': _y }

    square_props['piece'] = { 
        'color': 'w' if role.isupper() else 'b', 
        'role': role.lower() } if role else None

    return square_props