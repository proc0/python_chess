import os
import pygame as pg
from cursors import HAND_CURSOR, GRAB_CURSOR
from pprint import pprint

def move_piece(event, piece):
  piece_rect = piece.piece_png.get_rect()
  piece.x = event.pos[0] - piece_rect[2]/2
  piece.y = event.pos[1] - piece_rect[3]/2
  return piece

class Game():
  display = None
  player = None
  events = [
    'MouseButtonUp', 
    'MouseButtonDown', 
    'MouseMotion' ]
  
  def __init__(self, win_size):
    game_title = "python chess"
    logo_src = "logo.png"
    # load and set the logo
    pg.display.set_icon(pg.image.load(logo_src))
    pg.display.set_caption(game_title)
    # init display
    self.display = pg.display.set_mode(win_size)
    self.cursor = pg.mouse.get_cursor()

  def draw(self, board):
      board.draw()
      self.display.blit(board.surface, board.surface.get_rect())

  def MouseButtonUp(self, event, board):
    if(self.player.piece):
      pg.mouse.set_cursor(*HAND_CURSOR)
      sq = board.get_sq(event.pos)
      sq.place_piece(self.player.piece)
      self.player.piece = board.piece = None
      self.player.move(sq)

  def MouseButtonDown(self, event, board):
    sq = board.get_sq(event.pos)
    is_leftclick = event.button == 1
    if(is_leftclick and sq.piece and sq.has(event.pos)):
      pg.mouse.set_cursor(*GRAB_CURSOR)
      self.player.piece = sq.remove_piece()
      board.piece = move_piece(event, self.player.piece)

  def MouseMotion(self, event, board):
    sq = board.get_sq(event.pos)
    is_leftclick = event.buttons[0] == 1

    if(is_leftclick and self.player.piece):        
      board.piece = move_piece(event, self.player.piece)
    else:
      cursor = HAND_CURSOR if sq.piece else self.cursor
      pg.mouse.set_cursor(*cursor)

  def run(self, board, players):
    self.player = players[0]
    self.draw(board)
    clock = pg.time.Clock()
    quit = False
    while not quit:
      clock.tick(60)
      for event in pg.event.get():
        if event.type == pg.QUIT:
          quit = True
        elif pg.event.event_name(event.type) in self.events:
          if(board.has(event.pos)):
            handle = getattr(self, pg.event.event_name(event.type))
            handle(event, board)

      self.draw(board)
      pg.display.flip()
