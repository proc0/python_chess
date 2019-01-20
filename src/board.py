import pygame as pg
from pygame import Surface
from math import floor
from pprint import pprint
from itertools import product

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

  def __init__(self, size):
    self.size = (size, size)
    self.sq_size = int(self.size[1]/8)
    self.surface = Surface(self.size)

  def within(self, pos):
    return pos[0] < self.size[0] and pos[1] < self.size[1]

  def square(self, pos):
    point = lambda i: floor(pos[i]/self.sq_size)
    return self.squares[point(1)][point(0)]

  def update(self, square):
    square.draw()
    self.surface.blit(square.surface, (square.x, square.y))
    return self.surface

  def draw(self, square = None):
    sq_pad = 6
    sq_range = range(1, 9)

    if(len(self.squares) == 0):
      for y in sq_range:
        row = []
        _y = y-1
        for x in sq_range:
          _x = x-1
          tx = self.sq_size*_x
          ty = self.sq_size*_y

          toggle_color = is_even(x) ^ is_even(y)
          pc_props = {
            '_x' : _x,
            '_y' : _y,
            'x': tx, 
            'y': ty,
            'size': self.sq_size - (sq_pad*2),
            'role': 'k',
            'color': 'w',
          }
          
          occupy = None
          if(INITBOARD[_y][_x] == 1):
            occupy = Piece(pc_props)

          sq = Square({
            'size': self.sq_size,
            '_x' : _x,
            '_y' : _y,
            'x': tx, 
            'y': ty,
            'pad': sq_pad, 
            'piece': occupy,
            'color': DARK if toggle_color else LIGHT,
            'text_color': LIGHT if toggle_color else DARK,
            'label': str(chr(73-y)) + str(x)
          })
          sq.draw()
          row.append(sq)
        self.squares.append(row)
        row_blits = list(map(lambda s: (s.surface, (s.x, s.y)), row))
        self.surface.blits(row_blits)
    return self.surface

    
