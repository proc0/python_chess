import pygame as pg
from pygame import Surface

class Square:
  piece = None
  surface = None
  def __init__(self, props):
    for k, v in props.items():
      setattr(self, k, v)
    self.surface = Surface((self.size, self.size))
    self.surface.fill(self.color)

  def draw(self):
    font = pg.font.SysFont('Arial', 10)
    font_surface = font.render(self.label, False, self.text_color)

    if(self.piece):
      self.piece.draw()
      self.surface.blit(self.piece.surface, (self.pad, self.pad))
    self.surface.blit(font_surface, (self.pad/2, self.pad/2))

  def remove_piece(self):
    if(self.piece):
      # self.piece.surface.fill(self.color)
      self.piece = None
      self.surface.fill(self.color)

  def has(self, pos):
    in_x = pos[0] > self.x + self.pad and pos[0] < self.x + self.size - self.pad
    in_y = pos[1] > self.y + self.pad and pos[1] < self.y + self.size - self.pad
    return self.piece and in_x and in_y
