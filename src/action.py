import pygame as pg
from cursors import HAND_CURSOR, GRAB_CURSOR, DEFAULT_CURSOR

def move_piece(pos, piece):
  piece_rect = piece.piece_png.get_rect()
  piece.x = pos[0] - piece_rect[2]/2
  piece.y = pos[1] - piece_rect[3]/2
  return piece

def update(player, board, action, event):
    sq = None
    if(action == 'GRAB'):
      sq = board.get_sq(event.pos)
      if(sq.is_focused(event.pos) and not player.piece):
        player.piece = move_piece(event.pos, sq.remove_piece())
        pg.mouse.set_cursor(*GRAB_CURSOR)

    if(action == 'MOVING'):
      sq = board.get_sq(event.pos)
      if(player.piece):
        player.piece = move_piece(event.pos, player.piece)

    if(action == 'DROPPING'):
      sq = board.get_sq(event.pos)
      sq.place_piece(player.piece)
      board.drop_piece(player.piece)
      player.piece = None
      player.move(sq)
      pg.mouse.set_cursor(*HAND_CURSOR)

    if(action == 'HOVER'):
      pg.mouse.set_cursor(*HAND_CURSOR)

    if(action == 'IDLE'):
      pg.mouse.set_cursor(*DEFAULT_CURSOR)
    
    return sq