#!/usr/bin/env python
import pygame as pg
from pygame import Surface

is_even = lambda n: n%2 == 0

class Player:
  history = []
  def __init__(self, props):
    for k, v in props.items():
      setattr(self, k, v)

  def move(self, player_action):
    if(player_action['board_click']):
      self.history.append({
        'pos': player_action['pos']
        })

class Square:
  surface = None
  def __init__(self, props):
    for k, v in props.items():
      setattr(self, k, v)
    self.surface = Surface((self.size, self.size))
    self.surface.fill(self.color)

  def draw(self):
    font = pg.font.SysFont('Arial', 10)
    coords = font.render(self.label, False, self.text_color)
    self.surface.blit(coords, (5,5))


class Board:
  bg_color = (255,255,255)
  light = (255,255,255)
  dark = (0,0,0)
  squares = []

  def __init__(self, size):
    self.size = (size[1], size[1])
    self.surface = Surface((self.size[0], self.size[1]))
    self.surface.fill(self.bg_color)

  def draw(self):
    sq_size = int(self.size[1]/8)
    sq_range = range(1, 9)

    for y in sq_range:
      even_row = is_even(y)

      row = []
      for x in sq_range:
        even_col = is_even(x)
        alter = even_col if even_row else not even_col
        sq = Square({
          'size': sq_size,
          'x': x*sq_size - sq_size, 
          'y': y*sq_size - sq_size,
          'color': self.dark if alter else self.light,
          'text_color': self.light if alter else self.dark,
          'label': str(chr(73-y)) + str(x)
        })
        sq.draw()
        row.append((sq.surface, (sq.x, sq.y)))

      self.squares.append(row)
      self.surface.blits(row)

class Game():
  display = None
  def __init__(self, win_size):
    game_title = "python chess"
    logo_src = "logo.png"
    # load and set the logo
    pg.display.set_icon(pg.image.load(logo_src))
    pg.display.set_caption(game_title)
    self.display = pg.display.set_mode(win_size)

  def is_move(self, board, action):
    if(action[0] < board.size[0] and action[1] < board.size[1]):
      return True

  def loop(self, board, players):
    run = True
    while run:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          run = False
        elif event.type == pg.MOUSEBUTTONDOWN:
          click = event.button
          pos = event.pos
          if(click == 1):
            if(self.is_move(board, pos)):
              print(event)
              players[0].move({ 
                  'board_click': True, 
                  'pos': pos 
                })
      pg.display.update()
    return run

# define a main function
def main(): 
  pg.init()
  pg.font.init()
  size = (800,640)
  # draw board
  board = Board(size)
  board.draw()
  # init game
  game = Game(size)
  game.display.blit(board.surface, board.surface.get_rect())
  # summon players
  players = [
    Player({'color':'white'}), 
    Player({'color':'black'})
  ]
  # main
  game.loop(board, players)
  for m in players[0].history:
    print(m)
  # end
  pg.quit()
  quit()


if __name__=="__main__":
  main()