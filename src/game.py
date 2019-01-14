import os
import pygame as pg
from cursors import HAND_CURSOR, GRAB_CURSOR

class Game():
  display = None
  def __init__(self, win_size):
    game_title = "python chess"
    logo_src = "logo.png"
    # os.environ['SDL_VIDEODRIVER'] = 'directx'
    # load and set the logo
    pg.display.set_icon(pg.image.load(logo_src))
    pg.display.set_caption(game_title)
    self.display = pg.display.set_mode(win_size)

  def draw(self, board):
      self.display.blit(board.surface, board.surface.get_rect())

  def loop(self, board, players):
    run = True
    DEFAULT_CURSOR = pg.mouse.get_cursor()
    while run:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          run = False

        elif event.type == pg.MOUSEBUTTONUP:
          if(board.has(event.pos) and board.get_sq(event.pos).has(event.pos)):
            pg.mouse.set_cursor(*HAND_CURSOR)
            players[0].move({ 
                'board_click': True, 
                'pos': event.pos 
              })

        elif event.type == pg.MOUSEBUTTONDOWN:
          if(board.has(event.pos) and board.get_sq(event.pos).has(event.pos)):
            pg.mouse.set_cursor(*GRAB_CURSOR)

        elif event.type == pg.MOUSEMOTION:
          if(board.has(event.pos)):
            sq = board.get_sq(event.pos)
            is_left_click = event.buttons[0] == 1

            if(sq.has(event.pos)):
              sq.remove_piece()
              board.draw()
              self.draw(board)

              if(is_left_click):
                pg.mouse.set_cursor(*GRAB_CURSOR)
                # sq.piece = None
              else:
                pg.mouse.set_cursor(*HAND_CURSOR)
            else:
              pg.mouse.set_cursor(*DEFAULT_CURSOR)
          else:
            pg.mouse.set_cursor(*DEFAULT_CURSOR)

      pg.display.flip()
    return run
