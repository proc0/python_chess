import pygame as pg
from pygame import Surface
from math import floor
from pprint import pprint

from src.basic import is_even
from src.square import Square
from src.piece import Piece
from src.FEN import fromFEN

LIGHT = (255,255,255)
DARK = (50,50,50)
INITBOARD = [
    [0,0,1,0,0,1,0,1],
    [0,0,1,0,0,1,0,0],
    [0,1,0,0,0,1,0,0],
    [0,0,0,0,1,1,0,0],
    [0,0,1,0,0,0,0,0],
    [0,1,1,0,0,1,0,0],
    [1,0,1,0,0,1,0,0],
    [0,1,0,0,0,1,0,0]
  ]

initial_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

class Board:
  squares = []
  pieces = []
  piece = None

  def __init__(self, size):
    self.size = (size, size)
    self.sq_size = int(self.size[1]/8)
    self.surface = Surface(self.size)
    # self.surface.fill(LIGHT)

  def has(self, pos):
    return pos[0] < self.size[0] and pos[1] < self.size[1]

  def get_sq(self, pos):
    point = lambda i: floor(pos[i]/self.sq_size)
    sq = self.squares[point(1)][point(0)]
    return sq

  def draw(self):
    sq_size = int(self.size[1]/8)
    sq_pad = 6
    sq_range = range(1, 9)

    for y in sq_range:
      row = []
      _y = y-1
      for x in sq_range:
        _x = x-1
        if(len(self.squares) < 64):
          tx = sq_size*_x
          ty = sq_size*_y
          toggle_color = is_even(x) ^ is_even(y)
          pc_props = {
            '_x' : _x,
            '_y' : _y,
            'x': tx, 
            'y': ty,
            'size': sq_size - (sq_pad*2),
            'role': 'k',
            'color': 'w',
          }
          sq = Square({
            'size': sq_size,
            '_x' : _x,
            '_y' : _y,
            'x': tx, 
            'y': ty,
            'pad': sq_pad, 
            'piece': Piece(pc_props) if INITBOARD[_y][_x] == 1 else None,
            'color': DARK if toggle_color else LIGHT,
            'text_color': LIGHT if toggle_color else DARK,
            'label': str(chr(73-y)) + str(x)
          })
          row.append(sq)
        else:
          sq = self.squares[_y][_x]
          if(self.piece and sq.piece and self.piece == sq.piece):
            sq.piece = None
          row.append(sq)

        # sq.draw()

      if(len(self.squares) < 64):
        self.squares.append(row)

      row_blits = list(map(lambda s: (s.surface, (s.x, s.y)), row))
      self.surface.blits(row_blits)

    if(self.piece):
      self.surface.blit(self.piece.surface, (self.piece.x, self.piece.y))              

    
