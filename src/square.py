import pygame as pg
from pygame import Surface

class Square:
  piece = None
  surface = None
  def __init__(self, props):
    for k, v in props.items():
      setattr(self, k, v)
    self.surface = Surface((self.size, self.size))

  def draw(self):
    self.surface.fill(self.color)
    self.draw_coords()
    if(self.piece):
      piece_rect = self.piece.piece_png.get_rect()
      self.piece.draw()
      self.surface.blit(self.piece.surface, (self.size/2 - piece_rect[3]/2, self.size/2 - piece_rect[2]/2))
    return self.surface

  def draw_coords(self):
    font = pg.font.SysFont('Arial', 10)
    font_surface = font.render(self.label, False, self.text_color)
    self.surface.blit(font_surface, (self.pad, self.size - self.pad*2))

  def remove_piece(self):
    _piece = None
    if(self.piece):
      _piece = self.piece
      self.piece = None
    return _piece

  def place_piece(self, piece):
    self.piece = piece
    self.piece.x = self.x
    self.piece.y = self.y  
    return piece

  def within(self, pos):
    in_x = pos[0] > self.x + self.pad and pos[0] < self.x + self.size - self.pad
    in_y = pos[1] > self.y + self.pad and pos[1] < self.y + self.size - self.pad
    return self.piece and in_x and in_y
