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
  pieces = []
  piece = None

  def __init__(self, size):
    self.size = (size, size)
    self.sq_size = int(self.size[1]/8)
    self.surface = Surface(self.size)
    # self.buffer = self.surface.get_buffer()
    # self.piece_surface = self.surface.subsurface(self.surface.get_rect())
    # self.surface.fill(LIGHT)

  def has(self, pos):
    return pos[0] < self.size[0] and pos[1] < self.size[1]

  def get_sq(self, pos):
    point = lambda i: floor(pos[i]/self.sq_size)
    sq = self.squares[point(1)][point(0)]
    return sq

  def draw(self, drop_piece = None):
    sq_pad = 6
    sq_range = range(1, 9)

    if(len(self.squares) == 0):
      print('board draw')

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
          if(drop_piece):
            occupy = drop_piece
          elif(INITBOARD[_y][_x] == 1):
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

    if(drop_piece):
      sq = self.squares[floor(drop_piece.y/self.sq_size)][floor(drop_piece.x/self.sq_size)]
      sq.draw()
      self.surface.blit(sq.surface, (sq.x, sq.y))
      
    #   row_blits = []
    #   for row in self.squares:
    #     for sq in row:
    #       sq.draw()
    #       row_blits.append((sq.surface, (sq.x, sq.y)))
    #   self.surface.blits(row_blits)

    # if(self.piece or activity == 'DROP'):
    #   # xy = [2,1,0,-1,-2]
    #   # sq_coords = list(filter(lambda c: c != [0,0], product(xy, xy)))
    #   # sqs = list(map(lambda coord: self.squares[coord[0]+floor(self.piece.y/self.sq_size)][coord[1]+floor(self.piece.x/self.sq_size)], sq_coords))
    #   # sqs_blits = []
    #   # for row in self.squares:
    #   #   for sq in row:
    #   #     sq.draw()
    #   #     sqs_blits.append((sq.surface, (sq.x, sq.y)))
    #   # self.surface.blits(sqs_blits)              
    #   if(activity == 'DROP'):
    #     self.piece = None
    #   else:
    #     self.surface.fill(self.buffer)
    #     self.piece_surface.blit(self.piece.surface, (self.piece.x, self.piece.y))

    
