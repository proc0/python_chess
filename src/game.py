import os
import pygame as pg
from cursors import HAND_CURSOR, GRAB_CURSOR
from pprint import pprint

def move_piece(pos, piece):
  piece_rect = piece.piece_png.get_rect()
  piece.x = pos[0] - piece_rect[2]/2
  piece.y = pos[1] - piece_rect[3]/2
  return piece

class Game():
  display = None
  player = None
  pg_events = [
    'MouseButtonUp', 
    'MouseButtonDown', 
    'MouseMotion' ]
  
  def __init__(self, win_size):
    self.display = pg.display.set_mode(win_size)
    self.cursor = pg.mouse.get_cursor()
    self.action = ('IDLE', None)

  def draw(self, board):
    if(len(board.squares) == 0):
      board.draw()
      self.display.blit(board.surface, board.surface.get_rect())

    refresh = False
    if(self.action[0] == 'GRAB'):
      evt = self.action[1]
      sq = board.get_sq(evt.pos)
      print(sq.piece)

      if(sq.is_focused(evt.pos) and not self.player.piece):
        self.player.piece = move_piece(evt.pos, sq.remove_piece())
        self.action = ('MOVING', evt)
      else:
        self.action = ('IDLE', evt)

      pg.mouse.set_cursor(*GRAB_CURSOR)
      refresh = True

    if(self.action[0] == 'MOVING'):
      evt = self.action[1]
      sq = board.get_sq(evt.pos)

      if (sq.is_focused(evt.pos) and not self.player.piece):
        self.action = ('IDLE', evt)
      elif(self.player.piece):
        self.player.piece = move_piece(evt.pos, self.player.piece)

      refresh = True

    if(self.action[0] == 'DROP'):
      evt = self.action[1]
      sq = board.get_sq(evt.pos)
      sq.place_piece(self.player.piece)
      board.drop_piece(self.player.piece)
      self.player.piece = None
      self.player.move(sq)
      pg.mouse.set_cursor(*HAND_CURSOR)
      self.action = ('IDLE', evt)
      refresh = True

    if(self.action[0] == 'IDLE'):
      evt = self.action[1]
      sq = board.get_sq(evt.pos) if evt else None
      cursor = self.cursor
      if (sq and sq.is_focused(evt.pos) and not self.player.piece):
        cursor = HAND_CURSOR
      pg.mouse.set_cursor(*self.cursor)
    
    if(refresh):
      sq.draw()
      board.surface.blit(sq.surface, (sq.x, sq.y))
      self.display.blit(board.surface, board.surface.get_rect())
      if(self.player.piece):
        self.display.blit(self.player.piece.surface, (self.player.piece.x,  self.player.piece.y))

  def MouseButtonUp(self, event, board):
    if(self.player.piece):
      self.action = ('DROP', event)

  def MouseButtonDown(self, event, board):
    is_leftclick = event.button == 1
    if(is_leftclick):
      self.action = ('GRAB', event)

  def MouseMotion(self, event, board):
    is_leftclick = event.buttons[0] == 1
    if(is_leftclick and self.player.piece):        
      self.action = ('MOVING', event)

  def run(self, board, players):
    self.player = players[0]
    self.draw(board)
    quit = False
    while not quit:
      for event in pg.event.get():
        quit = event.type == pg.QUIT
        pg_event = pg.event.event_name(event.type)
        if pg_event in self.pg_events:
          if(board.has(event.pos)):
            handle = getattr(self, pg_event)
            handle(event, board)
      self.draw(board)
      pg.display.flip()
