import pygame as pg
from pygame import Surface

class Square:
  piece = None
  surface = None
  hover = False

  def __init__(self, props):
    for k, v in props.items():
      setattr(self, k, v)
    self.surface = Surface((self.size, self.size))
    self.fresh = False
    self.sq_highlight1 = Surface((self.size, 4))
    self.sq_highlight2 = Surface((4, self.size))
    self.sq_highlight1.fill((255,255,153))
    self.sq_highlight2.fill((255,255,153))

  def draw(self):
    # print(self.label, ' draw ', self.hover)
    if(self.hover):
      self.surface.fill(self.color)
      self.highlight()
    else:
      self.surface.fill(self.color)
    self.draw_coords()
    if(self.piece):
      piece_rect = self.piece.piece_png.get_rect()
      self.piece.draw()
      self.surface.blit(self.piece.surface, (self.size/2 - piece_rect[3]/2, self.size/2 - piece_rect[2]/2))
    self.fresh = True
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
    self.fresh = False
    return _piece

  def highlight(self):
    self.surface.blit(self.sq_highlight1, (0,0))
    self.surface.blit(self.sq_highlight2, (0,0))
    self.surface.blit(self.sq_highlight1, (0,self.size-4))
    self.surface.blit(self.sq_highlight2, (self.size-4,0))
    self.fresh = False

  def place_piece(self, piece):
    self.piece = piece
    self.piece.x = self.x
    self.piece.y = self.y  
    self.fresh = False
    return piece

  def within(self, pos):
    in_x = pos[0] > self.x + self.pad and pos[0] < self.x + self.size - self.pad
    in_y = pos[1] > self.y + self.pad and pos[1] < self.y + self.size - self.pad
    return self.piece and in_x and in_y
