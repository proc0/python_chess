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

  def draw(self, board, piece = None, sq = None):
    if(len(board.squares) == 0):
      board.draw()
      self.display.blit(board.surface, board.surface.get_rect())
    elif(sq):
      board.draw(sq)
      self.display.blit(board.surface, board.surface.get_rect())
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

  def run(self, board, players):
    font = pg.font.Font(None, 30)
    ui = pg.Surface((self.win_size[0]-board.size[0], board.size[0]))
    clock = pg.time.Clock()
    player = players[0]
    self.draw(board)
    quit = False
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
            update(player, square, *action)
            self.draw(board, player.piece, square)
            pg.display.flip()
      # TODO: refactor to ui 
      fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
      ui.fill((0,0,0))
      ui.blit(fps, (20,20))
      self.display.blit(ui, (board.size[0],0))
