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
    self.display = pg.display.set_mode(win_size)
    self.cursor = pg.mouse.get_cursor()
    self.activity = 'IDLE'

  def draw(self, board):
    if(len(board.squares) == 0):
      board.draw()
      self.display.blit(board.surface, board.surface.get_rect())

    if(self.activity == 'MOVING' or self.activity == 'DROP'):
      self.display.blit(board.surface, board.surface.get_rect())
      if(self.activity != 'DROP'):
        self.display.blit(self.player.piece.surface, (self.player.piece.x,  self.player.piece.y))
      else:
        board.draw(self.player.piece)
        self.display.blit(board.surface, board.surface.get_rect())
    
    if(self.activity == 'DROP'):
      self.activity = 'IDLE'

  def MouseButtonUp(self, event, board):
    if(self.player.piece):
      self.activity = 'DROP'
      pg.mouse.set_cursor(*HAND_CURSOR)
      sq = board.get_sq(event.pos)
      sq.place_piece(self.player.piece)
      self.player.piece = None
      self.player.move(sq)

  def MouseButtonDown(self, event, board):
    sq = board.get_sq(event.pos)
    is_leftclick = event.button == 1
    if(is_leftclick and sq.is_focused(event.pos)):
      self.activity = 'MOVING'
      pg.mouse.set_cursor(*GRAB_CURSOR)
      self.player.piece = sq.remove_piece()
      self.player.piece = move_piece(event, self.player.piece)

  def MouseMotion(self, event, board):
    sq = board.get_sq(event.pos)
    is_leftclick = event.buttons[0] == 1

    if(is_leftclick and self.player.piece):        
      self.player.piece = move_piece(event, self.player.piece)
    else:
      cursor = self.cursor
      if sq.is_focused(event.pos):
        cursor = HAND_CURSOR
      pg.mouse.set_cursor(*cursor)

  def run(self, board, players):
    self.player = players[0]
    self.draw(board)
    quit = False
    while not quit:
      for event in pg.event.get():
        quit = event.type == pg.QUIT
        if pg.event.event_name(event.type) in self.events:
          if(board.has(event.pos)):
            handle = getattr(self, pg.event.event_name(event.type))
            handle(event, board)
      self.draw(board)
      pg.display.flip()
