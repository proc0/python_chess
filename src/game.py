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
    self.idle = 'IDLE'

  def draw(self, board, player):
    if(len(board.squares) == 0):
      self.display.blit(board.draw(), board.surface.get_rect())
    else:
      self.display.blit(board.update(), board.surface.get_rect())
      if(player.piece):
        self.display.blit(player.piece.surface, (player.piece.x,  player.piece.y))

  def MouseButtonUp(self, board, event, player):
    action = self.idle
    if(player.piece):
      action = 'DROPPING'
    return action

  def MouseButtonDown(self, board, event, player):
    is_leftclick = event.button == 1
    action = self.idle
    if(is_leftclick):
      action = 'GRAB'
    return action

  def MouseMotion(self, board, event, player):
    is_leftclick = event.buttons[0] == 1
    action = self.idle
    if(is_leftclick and player.piece):        
      action = 'MOVING'
    elif(board.square(event.pos).within(event.pos)):
      action = 'HOVER'
    return action

  def run(self, ui, board, players):
    player = players[0]
    clock = pg.time.Clock()
    ui_pos = (board.size[0],0)

    self.draw(board, player)
    quit = False
    while not quit:
      clock.tick(60)
      for event in pg.event.get():
        quit = event.type == pg.QUIT
        pg_event = pg.event.event_name(event.type)
        if pg_event in self.pg_events:
          if(board.within(event.pos)):
            input = getattr(self, pg_event)
            action = input(board, event, player)

          if(action != 'IDLE'):
            # update game
            board, player = update(board, action, event, player)
            # update board
            self.draw(board, player)
            # update pg
            pg.display.flip()

      # debug
      fps = int(clock.get_fps())
      # update ui
      self.display.blit(ui.draw(fps), ui_pos)
