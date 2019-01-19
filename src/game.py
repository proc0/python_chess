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

  def draw(self, player, board, sq = None):
    if(len(board.squares) == 0):
      board.draw()
      sq_blits = list(map(lambda row: list(map(lambda s: (s.surface, (s.x, s.y)), row)), board.squares))
      for row_blits in sq_blits:
        board.surface.blits(row_blits)
      self.display.blit(board.surface, board.surface.get_rect())
    else:
      piece = player.piece
      if(sq):
        sq.draw()
        board.surface.blit(sq.surface, (sq.x, sq.y))
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
    sq = board.get_sq(event.pos)
    action = self.idle
    if(is_leftclick and player.piece):        
      action = ('MOVING', event)
    elif(sq.is_focused(event.pos)):
      action = ('HOVER', event)
    else:
      action = ('IDLE', event)
    return action

  def run(self, board, players):
    player = players[0]
    self.draw(player, board)
    font = pg.font.Font(None, 30)
    ui = pg.Surface((self.win_size[0]-board.size[0], board.size[0]))
    clock = pg.time.Clock()
    quit = False
    while not quit:
      clock.tick(60)
      for event in pg.event.get():
        quit = event.type == pg.QUIT
        pg_event = pg.event.event_name(event.type)
        sq = None
        if pg_event in self.pg_events:
          if(board.has(event.pos)):
            input = getattr(self, pg_event)
            action = input(event, player, board)
            sq = update(player, board, *action)
            self.draw(player, board, sq)
            pg.display.flip()
      # TODO: refactor to ui 
      fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
      ui.fill((0,0,0))
      ui.blit(fps, (20,20))
      self.display.blit(ui, (board.size[0],0))
