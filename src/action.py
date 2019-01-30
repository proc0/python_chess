import pygame as pg
from cursors import HAND_CURSOR, GRAB_CURSOR, DEFAULT_CURSOR

class Actions():
  IDLE = 0
  HOVER = 1
  GRAB = 2
  DRAG = 3
  DROP = 4
  CLEAR = 5

actions = Actions()

def move_piece(pos, piece):
  piece_rect = piece.piece_png.get_rect()
  piece.x = pos[0] - piece_rect[2]/2
  piece.y = pos[1] - piece_rect[3]/2
  return piece

def update(board, action, event, player):
  square = board.square(event.pos)

  if(action == actions.HOVER):
    for row in board.squares:
      for sq in row:
        sq.hover = False
        sq.fresh = False
    square.hover = True
    square.fresh = False
    pg.mouse.set_cursor(*HAND_CURSOR)

  elif(action == actions.GRAB):
    if(square.within(event.pos) and not player.piece):
      player.piece = move_piece(event.pos, square.remove_piece())
      square.hover = False
      pg.mouse.set_cursor(*GRAB_CURSOR)

  elif(action == actions.DRAG):
    if(player.piece):
      player.piece = move_piece(event.pos, player.piece)

  elif(action == actions.DROP):
    square.place_piece(player.piece)
    player.piece = None
    player.move(square)
    pg.mouse.set_cursor(*HAND_CURSOR)

  elif(action == actions.CLEAR):
    for row in board.squares:
      for sq in row:
        sq.hover = False
        sq.fresh = False
    pg.mouse.set_cursor(*DEFAULT_CURSOR)

  return board, player
    