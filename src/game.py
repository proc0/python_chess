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

    if(self.action[0] == 'MOVING'):
      evt = self.action[1][0]
      sq = self.action[1][1]
      
      if(self.player.piece):
        self.player.piece = move_piece(evt.pos, self.player.piece)
      else:
        self.player.piece = move_piece(evt.pos, sq.remove_piece())
      
      sq.draw()
      board.surface.blit(sq.surface, (sq.x, sq.y))
      self.display.blit(board.surface, board.surface.get_rect())
      self.display.blit(self.player.piece.surface, (self.player.piece.x,  self.player.piece.y))
    
    if(self.action[0] == 'DROP'):
      # evt = self.action[1][0]
      sq = self.action[1][1]
      sq.place_piece(self.player.piece)
      board.drop_piece(self.player.piece)
      self.player.piece = None
      self.player.move(sq)
      self.display.blit(board.surface, board.surface.get_rect())
    
    if(self.action[0] == 'DROP'):
      self.action = ('IDLE', None)

  def MouseButtonUp(self, event, board):
    if(self.player.piece):
      pg.mouse.set_cursor(*HAND_CURSOR)
      self.action = ('DROP', (event, board.get_sq(event.pos)))

  def MouseButtonDown(self, event, board):
    sq = board.get_sq(event.pos)
    is_leftclick = event.button == 1
    if(is_leftclick and sq.is_focused(event.pos)):
      self.action = ('MOVING', (event, sq))
      pg.mouse.set_cursor(*GRAB_CURSOR)


  def MouseMotion(self, event, board):
    sq = board.get_sq(event.pos)
    is_leftclick = event.buttons[0] == 1

    if(is_leftclick and self.player.piece):        
      self.action = ('MOVING', (event, sq))
      # self.player.piece = move_piece(event.pos, self.player.piece)
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
        if pg.event.event_name(event.type) in self.pg_events:
          if(board.has(event.pos)):
            handle = getattr(self, pg.event.event_name(event.type))
            handle(event, board)
      self.draw(board)
      pg.display.flip()
