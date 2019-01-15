import os
import pygame as pg
from cursors import HAND_CURSOR, GRAB_CURSOR

def move_piece(event, piece):
  piece_rect = piece.piece_png.get_rect()
  piece.x = event.pos[0] - piece_rect[2]/2
  piece.y = event.pos[1] - piece_rect[3]/2
  return piece

class Game():
  display = None
  def __init__(self, win_size, board):
    game_title = "python chess"
    logo_src = "logo.png"
    # os.environ['SDL_VIDEODRIVER'] = 'directx'
    # load and set the logo
    pg.display.set_icon(pg.image.load(logo_src))
    pg.display.set_caption(game_title)
    self.board = board
    self.board.draw()
    self.display = pg.display.set_mode(win_size)

  def draw(self):
      self.board.draw()
      self.display.blit(self.board.surface, self.board.surface.get_rect())

  def loop(self, board, players):
    run = True
    DEFAULT_CURSOR = pg.mouse.get_cursor()
    player = players[0]
    while run:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          run = False

        elif event.type == pg.MOUSEBUTTONUP:
          if(board.has(event.pos)):
            if(player.piece):
              sq = board.get_sq(event.pos)
              sq.place_piece(player.piece)
              player.piece = None
              board.piece = None
              player.move(sq)
            pg.mouse.set_cursor(*HAND_CURSOR)

        elif event.type == pg.MOUSEBUTTONDOWN:
          if(board.has(event.pos) and board.get_sq(event.pos).has(event.pos)):
            pg.mouse.set_cursor(*GRAB_CURSOR)

        elif event.type == pg.MOUSEMOTION:
          if(board.has(event.pos)):
            sq = board.get_sq(event.pos)
            is_left_click = event.buttons[0] == 1

            if(sq.has(event.pos)):
              if(is_left_click):
                pg.mouse.set_cursor(*GRAB_CURSOR)
                player.piece = sq.remove_piece()
                board.piece = move_piece(event, player.piece)
              else:
                pg.mouse.set_cursor(*HAND_CURSOR)
            elif(player.piece):
              if(is_left_click):
                pg.mouse.set_cursor(*GRAB_CURSOR)
                board.piece = move_piece(event, player.piece)            
            else:
              pg.mouse.set_cursor(*DEFAULT_CURSOR)
          else:
            pg.mouse.set_cursor(*DEFAULT_CURSOR)

      self.draw()
      pg.display.flip()
    return run
