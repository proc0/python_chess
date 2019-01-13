import pygame as pg
from pygame import Surface
from math import floor

from src.basic import is_even
from src.square import Square
from src.piece import Piece

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

class Board:
  squares = []
  pieces = []

  def __init__(self, size):
    self.size = (size[1], size[1])
    self.surface = Surface((self.size[0], self.size[1]))
    self.surface.fill(LIGHT)

  def draw(self):
    sq_size = int(self.size[1]/8)
    sq_range = range(1, 9)

    for y in sq_range:
      row = []
      for x in sq_range:
        alter = is_even(x) if is_even(y) else not is_even(x)
        
        sq = Square({
          'size': sq_size,
          '_x' : x-1,
          '_y' : y-1,
          'x': x*sq_size - sq_size, 
          'y': y*sq_size - sq_size,
          'pad': 12, 
          'piece': Piece() if INITBOARD[y-1][x-1] == 1 else None,
          'color': DARK if is_even(x) else LIGHT,
          'text_color': LIGHT if alter else DARK,
          'label': str(chr(73-y)) + str(x)
        })
        sq.draw()
        row.append(sq)

      self.squares.append(row)
      row_blits = list(map(lambda s: (s.surface, (s.x, s.y)), row))
      self.surface.blits(row_blits)

  def get_square(self, coords):
    sq_size = int(self.size[1]/8)
    point = lambda i: floor(coords[i]/sq_size)
    sq = self.squares[point(1)][point(0)]
    return sq
