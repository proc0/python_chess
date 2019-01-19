import os
import time
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

  def update(self, board, action, event):
    sq = None
    if(action == 'GRAB'):
      sq = board.get_sq(event.pos)
      if(sq.is_focused(event.pos) and not self.player.piece):
        self.player.piece = move_piece(event.pos, sq.remove_piece())
        pg.mouse.set_cursor(*GRAB_CURSOR)
        self.action = ('MOVING', event)
      else:
        self.action = ('IDLE', event)

    if(action == 'MOVING'):
      sq = board.get_sq(event.pos)
      if(self.player.piece):
        self.player.piece = move_piece(event.pos, self.player.piece)

    if(action == 'DROPPING'):
      sq = board.get_sq(event.pos)
      sq.place_piece(self.player.piece)
      board.drop_piece(self.player.piece)
      self.player.piece = None
      self.player.move(sq)
      self.action = ('DROP', event)

    if(action == 'HOVER'):
      pg.mouse.set_cursor(*HAND_CURSOR)

    if(action == 'DROP'):
      pg.mouse.set_cursor(*HAND_CURSOR)

    if(action == 'IDLE'):
      pg.mouse.set_cursor(*self.cursor)
    
    return sq

  def draw(self, board):
    if(len(board.squares) == 0):
      board.draw()
      self.display.blit(board.surface, board.surface.get_rect())
    else:
      sq = self.update(board, *self.action)
      piece = self.player.piece
      if(sq):
        sq.draw()
        board.surface.blit(sq.surface, (sq.x, sq.y))
        self.display.blit(board.surface, board.surface.get_rect())
        if(piece):
          self.display.blit(piece.surface, (piece.x,  piece.y))

  def MouseButtonUp(self, event, board):
    if(self.player.piece):
      self.action = ('DROPPING', event)

  def MouseButtonDown(self, event, board):
    is_leftclick = event.button == 1
    if(is_leftclick):
      self.action = ('GRAB', event)

  def MouseMotion(self, event, board):
    is_leftclick = event.buttons[0] == 1
    sq = board.get_sq(event.pos)
    if(is_leftclick and self.player.piece):        
      self.action = ('MOVING', event)
    elif(sq.is_focused(event.pos)):
      self.action = ('HOVER', event)
    else:
      self.action = ('IDLE', event)

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
