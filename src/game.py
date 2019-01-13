import os
import pygame as pg
from cursors import HAND_CURSOR, GRAB_CURSOR

class Game():
  display = None
  def __init__(self, win_size):
    game_title = "python chess"
    logo_src = "logo.png"
    os.environ['SDL_VIDEODRIVER'] = 'directx'
    # load and set the logo
    pg.display.set_icon(pg.image.load(logo_src))
    pg.display.set_caption(game_title)
    self.display = pg.display.set_mode(win_size)

  def draw(self, board):
      self.display.blit(board.surface, board.surface.get_rect())

  def is_move(self, board, action):
    if(action[0] < board.size[0] and action[1] < board.size[1]):
      return True

  def loop(self, board, players):
    run = True
    DEFAULT_CURSOR = pg.mouse.get_cursor()
    while run:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          run = False
        elif event.type == pg.MOUSEBUTTONUP:
          sq = board.get_square(event.pos)

          if(self.is_move(board, event.pos) and sq.has_hover(event.pos)):
            pg.mouse.set_cursor(*HAND_CURSOR)
            players[0].move({ 
                'board_click': True, 
                'pos': event.pos 
              })
        elif event.type == pg.MOUSEBUTTONDOWN:
          sq = board.get_square(event.pos)

          if(self.is_move(board, event.pos) and sq.has_hover(event.pos)):
            pg.mouse.set_cursor(*GRAB_CURSOR)
        elif event.type == pg.MOUSEMOTION:
          
          if(self.is_move(board, event.pos)):
            sq = board.get_square(event.pos)

            if(sq.has_hover(event.pos)):
              if(event.buttons[0] == 1):
                pg.mouse.set_cursor(*GRAB_CURSOR)
              else:
                pg.mouse.set_cursor(*HAND_CURSOR)
            else:
              pg.mouse.set_cursor(*DEFAULT_CURSOR)
          else:
            pg.mouse.set_cursor(*DEFAULT_CURSOR)

      pg.display.flip()
    return run
