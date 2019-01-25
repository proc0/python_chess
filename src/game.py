import os
import time
import pygame as pg
from pprint import pprint

from src.action import update, actions

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

  def draw(self, board, player):
    if(len(board.squares) == 0):
      self.display.blit(board.draw(), board.surface.get_rect())
    else:
      self.display.blit(board.update(), board.surface.get_rect())
      if(player.piece):
        self.display.blit(player.piece.surface, (player.piece.x,  player.piece.y))

  def MouseButtonUp(self, board, event, player):
    action = actions.IDLE
    if(player.piece):
      action = actions.DROP
    return action

  def MouseButtonDown(self, board, event, player):
    is_leftclick = event.button == 1
    action = actions.IDLE
    if(is_leftclick):
      action = actions.GRAB
    return action

  def MouseMotion(self, board, event, player):
    is_leftclick = event.buttons[0] == 1
    action = actions.IDLE
    if(is_leftclick and player.piece):        
      action = actions.DRAG
    elif(board.square(event.pos).within(event.pos)):
      action = actions.HOVER
    else:
      action = actions.CLEAR
    return action

  def run(self, ui, board, players):
    player = players[0]
    clock = pg.time.Clock()
    ui_pos = (board.size[0],0)

    quit = False
    cleared = False
    self.draw(board, player)
    while not quit:
      clock.tick(60)
      for event in pg.event.get():
        quit = event.type == pg.QUIT
        pg_event = pg.event.event_name(event.type)
        if pg_event in self.pg_events:
          if(board.within(event.pos)):
            input = getattr(self, pg_event)
            action = input(board, event, player)
            should_clear = action == actions.CLEAR and not cleared
            if(action != actions.IDLE or should_clear):
              # update game
              board, player = update(board, action, event, player)
              # draw game
              self.draw(board, player)
              # flip display
              pg.display.flip()
              # TODO: refactor event optim
              cleared = action == actions.CLEAR
      # debug
      fps = int(clock.get_fps())
      # update ui
      self.display.blit(ui.draw(fps), ui_pos)
