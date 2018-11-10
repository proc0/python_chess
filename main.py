#!/usr/bin/env python
import pygame as pg
from pygame import Surface

class Square:
  surface = None
  def __init__(self, props):
    self.size = props['size']
    self.x = props['x']
    self.y = props['y']
    self.color = props['color']
    self.label = props['label']
    self.surface = Surface((self.size, self.size))
    self.surface.fill(self.color)


class Board:
  bg_color = (255,255,255)
  light = (255,255,255)
  dark = (0,0,0)
  squares = []

  def __init__(self, size):
    self.size = size
    self.surface = Surface((self.size, self.size))
    self.surface.fill(self.bg_color)

  def draw(self, screen):
    sq_size = int(self.size/8)
    sq_range = range(1, 9)
    is_even = lambda n: n%2 == 0
    text = pg.font.SysFont('Arial', 10)

    for y in sq_range:
      even_row = is_even(y)

      row = []
      for x in sq_range:
        even_col = is_even(x)
        alternate = even_col if even_row else not even_col
        sq = Square({
          'size': sq_size,
          'x': x*sq_size - sq_size, 
          'y': y*sq_size - sq_size,
          'color': self.dark if alternate else self.light,
          'label': str(chr(73-y)) + str(x)
        })
        
        txt_surface = text.render(sq.label, False, self.light if alternate else self.dark)
        rect = (sq.x, sq.y, sq.size, sq.size)
        sq.surface.blit(txt_surface, (5,5))
        row.append((sq.surface, (sq.x, sq.y)))

      self.squares.append(row)
      self.surface.blits(row)



def loop():
  run = True
  while run:
    for event in pg.event.get():
      if event.type == pg.QUIT:
          run = False
    pg.display.update()
  return run

# define a main function
def main(): 
  game_title = "python chess"
  win_size = (800,640)
  logo_src = "logo.png"

  pg.init()
  pg.font.init()
  # load and set the logo
  pg.display.set_icon(pg.image.load(logo_src))
  pg.display.set_caption(game_title)
  screen = pg.display.set_mode(win_size)
  # draw board
  board = Board(win_size[1])
  board.draw(screen)

  screen.blit(board.surface, board.surface.get_rect())
  # main
  loop()
  # end
  pg.quit()
  quit()


if __name__=="__main__":
  main()