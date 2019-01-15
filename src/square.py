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
    self.draw()

  def draw(self):
    if(self.piece):
      piece_rect = self.piece.piece_png.get_rect()
      self.piece.draw()
      self.surface.blit(self.piece.surface, (self.size/2 - piece_rect[3]/2, self.size/2 - piece_rect[2]/2))
    self.draw_coords()

  def draw_coords(self):
    font = pg.font.SysFont('Arial', 10)
    font_surface = font.render(self.label, False, self.text_color)
    self.surface.blit(font_surface, (self.pad, self.size - self.pad*2))

  def remove_piece(self):
    p = None
    if(self.piece):
      p = self.piece
      self.piece = None
      self.surface.fill(self.color)
      self.draw_coords()
    return p

  def place_piece(self, piece):
    self.piece = piece
    self.piece.x = self.x
    self.piece.y = self.y    
    self.surface.blit(self.piece.surface, (self.pad, self.pad))
    self.draw_coords()

  def has(self, pos):
    in_x = pos[0] > self.x + self.pad and pos[0] < self.x + self.size - self.pad
    in_y = pos[1] > self.y + self.pad and pos[1] < self.y + self.size - self.pad
    return self.piece and in_x and in_y
