import pygame as pg
from cursors import HAND_CURSOR, GRAB_CURSOR, DEFAULT_CURSOR

def move_piece(pos, piece):
  piece_rect = piece.piece_png.get_rect()
  piece.x = pos[0] - piece_rect[2]/2
  piece.y = pos[1] - piece_rect[3]/2
  return piece

def update(player, squares, action, event):
    # print(action)
    square = squares[0]
    past_sq = squares[1]
    # print(square.label, past_sq.label if past_sq else '')
    if(action == 'GRAB'):
      if(square.within(event.pos) and not player.piece):
        player.piece = move_piece(event.pos, square.remove_piece())
        pg.mouse.set_cursor(*GRAB_CURSOR)

    if(action == 'MOVING'):
      if(player.piece):
        player.piece = move_piece(event.pos, player.piece)

    if(action == 'DROPPING'):
      square.place_piece(player.piece)
      player.piece = None
      player.move(square)
      pg.mouse.set_cursor(*HAND_CURSOR)

    if(action == 'HOVER'):
      square.hover = True
      pg.mouse.set_cursor(*HAND_CURSOR)

    if(action == 'IDLE'):
      if(past_sq):
        past_sq.hover = False
      pg.mouse.set_cursor(*DEFAULT_CURSOR)
    