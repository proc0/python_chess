import pygame as pg
from pygame import Surface
from math import floor

from src.common import is_even
from src.square import Square
from src.piece import Piece

class Board:
  bg_color = (255,255,255)
  light = (255,255,255)
  dark = (50,50,50)
  squares = []
  pieces = []
  dummy_board = [
      [0,0,1,0,0,1,0,1],
      [0,0,1,0,0,1,0,0],
      [0,1,0,0,0,1,0,0],
      [0,0,0,0,1,1,0,0],
      [0,0,1,0,0,0,0,0],
      [0,1,1,0,0,1,0,0],
      [1,0,1,0,0,1,0,0],
      [0,1,0,0,0,1,0,0]
    ]
  def __init__(self, size):
    self.size = (size[1], size[1])
    self.surface = Surface((self.size[0], self.size[1]))
    self.surface.fill(self.bg_color)

  def draw(self):
    sq_size = int(self.size[1]/8)
    sq_range = range(1, 9)

    for y in sq_range:
      even_row = is_even(y)

      row = []
      for x in sq_range:
        even_col = is_even(x)
        alter = even_col if even_row else not even_col
        sq = Square({
          'size': sq_size,
          '_x' : x-1,
          '_y' : y-1,
          'x': x*sq_size - sq_size, 
          'y': y*sq_size - sq_size,
          'pad': 12,
          'color': self.dark if alter else self.light,
          'text_color': self.light if alter else self.dark,
          'label': str(chr(73-y)) + str(x)
        })
        sq.draw()
        row.append(sq)

      self.squares.append(row)
      self.surface.blits(list(map(lambda s: (s.place_piece(Piece()) if self.dummy_board[s._y][s._x] == 1 else True) and (s.surface, (s.x, s.y)), row)))

  def get_square(self, coords):
    sq_size = int(self.size[1]/8)
    point = lambda i: floor(coords[i]/sq_size)
    sq = self.squares[point(1)][point(0)]
    return sq
