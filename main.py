#!/usr/bin/env python
import os
from math import floor
import pygame as pg
from pygame import Surface
from pprint import pprint
from cursors import HAND_CURSOR, GRAB_CURSOR

is_even = lambda n: n%2 == 0

class Piece(pg.sprite.Sprite):
  def __init__(self):
    pg.sprite.Sprite.__init__(self)
    # for k, v in props.items():
    #   setattr(self, k, v)
    piece_path = os.path.join('images', 'bb3.png')
    piece_png = pg.image.load(piece_path)
    piece_rect = piece_png.get_rect()
    self.piece_png = piece_png
    self.surface = Surface((piece_rect[2],piece_rect[3]), pg.SRCALPHA)

  def draw(self):
    self.surface.blit(self.piece_png, (0,0))


class Square:
  piece = None
  surface = None
  def __init__(self, props):
    for k, v in props.items():
      setattr(self, k, v)
    self.surface = Surface((self.size, self.size))
    self.surface.fill(self.color)
    # self.piece = Piece()

  def draw(self):
    font = pg.font.SysFont('Arial', 10)
    coords = font.render(self.label, False, self.text_color)
    self.surface.blit(coords, (self.pad/2, self.pad/2))

  def piece_hovering(self, coords):
    in_x = coords[0] > self.x + self.pad and coords[0] < self.x + self.size - self.pad
    in_y = coords[1] > self.y + self.pad and coords[1] < self.y + self.size - self.pad
    return self.piece and in_x and in_y

  def place_piece(self, piece):
    self.piece = piece
    self.piece.draw()
    self.surface.blit(self.piece.surface, (self.pad, self.pad))
    return piece

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

class Player:
  history = []
  def __init__(self, props):
    for k, v in props.items():
      setattr(self, k, v)

  def move(self, player_action):
    if(player_action['board_click']):
      self.history.append({
        'pos': player_action['pos']
        })

class Game():
  display = None
  def __init__(self, win_size):
    game_title = "python chess"
    logo_src = "logo.png"
    os.environ['SDL_VIDEODRIVER'] = 'directx'
    # load and set the logo
    pg.display.set_icon(pg.image.load(logo_src))
    pg.display.set_caption(game_title)
    self.display = pg.display.set_mode(win_size)

  def draw(self, board):
      self.display.blit(board.surface, board.surface.get_rect())

  def is_move(self, board, action):
    if(action[0] < board.size[0] and action[1] < board.size[1]):
      return True

  def loop(self, board, players):
    run = True
    DEFAULT_CURSOR = pg.mouse.get_cursor()
    while run:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          run = False

        elif event.type == pg.MOUSEBUTTONDOWN or \
          event.type == pg.MOUSEBUTTONUP:
          if(self.is_move(board, event.pos)):
            sq = board.get_square(event.pos)
            if(event.button == 1 and sq.piece_hovering(event.pos)):
              pg.mouse.set_cursor(*GRAB_CURSOR)
            else:
              pg.mouse.set_cursor(*DEFAULT_CURSOR)

        elif event.type == pg.MOUSEMOTION:
          # board moves
          if(self.is_move(board, event.pos)):
            sq = board.get_square(event.pos)
            if(sq.piece_hovering(event.pos)):
              pg.mouse.set_cursor(*HAND_CURSOR)
              if(event.buttons[0] == 1):
                pg.mouse.set_cursor(*GRAB_CURSOR)
            else:
              pg.mouse.set_cursor(*DEFAULT_CURSOR)

            players[0].move({ 
                'board_click': True, 
                'pos': event.pos 
              })
          else:
            pg.mouse.set_cursor(*DEFAULT_CURSOR)

      pg.display.flip()
    return run

# define a main function
def main(): 
  pg.init()
  pg.font.init()
  size = (800,640)
  # init
  game = Game(size)
  board = Board(size)
  # render
  board.draw()
  game.draw(board)
  # summon players
  players = [
    Player({'color':'white'}), 
    Player({'color':'black'})
  ]
  # main
  game.loop(board, players)
  # end
  pg.quit()
  quit()


if __name__=="__main__":
  main()