import os
import pygame as pg
from cursors import HAND_CURSOR, GRAB_CURSOR
from pprint import pprint

DEFAULT_CURSOR = None

def move_piece(event, piece):
  piece_rect = piece.piece_png.get_rect()
  piece.x = event.pos[0] - piece_rect[2]/2
  piece.y = event.pos[1] - piece_rect[3]/2
  return piece

class Game():
  display = None
  events = [
    'MouseButtonUp', 
    'MouseButtonDown', 
    'MouseMotion' ]
  
  def __init__(self, win_size, board):
    game_title = "python chess"
    logo_src = "logo.png"
    # load and set the logo
    pg.display.set_icon(pg.image.load(logo_src))
    pg.display.set_caption(game_title)
    # init display
    self.board = board
    self.display = pg.display.set_mode(win_size)
    self.default_cursor = pg.mouse.get_cursor()

  def draw(self, board):
      board.draw()
      self.display.blit(board.surface, board.surface.get_rect())

  def MouseButtonUp(self, event, player, board):
    pg.mouse.set_cursor(*HAND_CURSOR)
    if(player.piece):
      sq = board.get_sq(event.pos)
      sq.place_piece(player.piece)
      player.piece = board.piece = None
      player.move(sq)

  def MouseButtonDown(self, event, player, board):
    sq = board.get_sq(event.pos)
    is_left_click = event.button == 1
    if(is_left_click and sq.has(event.pos)):
      pg.mouse.set_cursor(*GRAB_CURSOR)
      player.piece = sq.remove_piece()
      board.piece = move_piece(event, player.piece)

  def MouseMotion(self, event, player, board):
    sq = board.get_sq(event.pos)
    is_left_click = event.buttons[0] == 1
    # piece hover
    if(sq.has(event.pos)):
      if(is_left_click):
        pg.mouse.set_cursor(*GRAB_CURSOR)
        if(player.piece):
          board.piece = move_piece(event, player.piece)
      else:
        pg.mouse.set_cursor(*HAND_CURSOR)
    # outer part of square
    elif(is_left_click and player.piece):
        pg.mouse.set_cursor(*GRAB_CURSOR)
        board.piece = move_piece(event, player.piece)            
    else:
      pg.mouse.set_cursor(*self.default_cursor)

  def run(self, board, players):
    player = players[0]
    self.draw(board)
    quit = False
    while not quit:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          quit = True
        elif pg.event.event_name(event.type) in self.events:
          if(board.has(event.pos)):
            handle = getattr(self, pg.event.event_name(event.type))
            handle(event, player, board)

      self.draw(board)
      pg.display.flip()
