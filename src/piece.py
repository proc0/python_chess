import os
import pygame as pg
from pygame import Surface

class Piece(pg.sprite.Sprite):
  def __init__(self):
    pg.sprite.Sprite.__init__(self)
    # for k, v in props.items():
    #   setattr(self, k, v)
    piece_path = os.path.join('images', 'bb3.png')
    piece_png = pg.image.load(piece_path)
    piece_rect = piece_png.get_rect()
    self.piece_png = piece_png
    self.surface = Surface((piece_rect[2],piece_rect[3]), pg.SRCALPHA)

  def draw(self):
    self.surface.blit(self.piece_png, (0,0))
    return self
