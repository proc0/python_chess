import os
import time
import pygame as pg
from pprint import pprint

from src.action import update

class Game():
  display = None
  win_size = (0,0)
  pg_events = [
    'MouseButtonUp', 
    'MouseButtonDown', 
    'MouseMotion' ]
  
  def __init__(self, win_size):
    self.display = pg.display.set_mode(win_size)
    self.win_size = win_size
    self.cursor = pg.mouse.get_cursor()
    self.idle = ('IDLE', None)

  def draw(self, board, square = None, piece = None):
    if(len(board.squares) == 0):
      self.display.blit(board.draw(), board.surface.get_rect())
    else:
      self.display.blit(board.update(square), board.surface.get_rect())
      if(piece):
        self.display.blit(piece.surface, (piece.x,  piece.y))

  def MouseButtonUp(self, event, player, board):
    action = self.idle
    if(player.piece):
      action = ('DROPPING', event)
    return action

  def MouseButtonDown(self, event, player, board):
    is_leftclick = event.button == 1
    action = self.idle
    if(is_leftclick):
      action = ('GRAB', event)
    return action

  def MouseMotion(self, event, player, board):
    is_leftclick = event.buttons[0] == 1
    action = self.idle
    if(is_leftclick and player.piece):        
      action = ('MOVING', event)
    elif(board.square(event.pos).within(event.pos)):
      action = ('HOVER', event)
    else:
      action = ('IDLE', event)
    return action

  def run(self, ui, board, players):
    quit = False
    player = players[0]
    clock = pg.time.Clock()
    while not quit:
      clock.tick(60)
      for event in pg.event.get():
        quit = event.type == pg.QUIT
        pg_event = pg.event.event_name(event.type)
        if pg_event in self.pg_events:
          if(board.within(event.pos)):
            input = getattr(self, pg_event)
            action = input(event, player, board)
            square = board.square(event.pos)
            # update player
            update(player, square, *action)
            # update board
            self.draw(board, square, player.piece)
            pg.display.flip()
      # update ui
      self.display.blit(ui.draw(int(clock.get_fps())), (board.size[0],0))
