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
    # self.piece = Piece()

  def draw(self):
    font = pg.font.SysFont('Arial', 10)
    coords = font.render(self.label, False, self.text_color)
    self.surface.blit(coords, (self.pad/2, self.pad/2))

  def piece_hovering(self, coords):
    in_x = coords[0] > self.x + self.pad and coords[0] < self.x + self.size - self.pad
    in_y = coords[1] > self.y + self.pad and coords[1] < self.y + self.size - self.pad
    return self.piece and in_x and in_y

  def place_piece(self, piece):
    self.piece = piece
    self.piece.draw()
    self.surface.blit(self.piece.surface, (self.pad, self.pad))
    return piece
