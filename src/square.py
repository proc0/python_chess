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
    self.settings = { 'draw_coords': False, 'draw_rankfile': True }

  def draw(self):
    if(self.hover):
      self.surface.fill(self.color)
      self.highlight()
    else:
      self.surface.fill(self.color)

    if(self.piece):
      self.piece.draw()
      self.surface.blit(self.piece.surface, self.get_piece_bounds())
    
    self.draw_coords()
    self.fresh = True

    return self.surface

  def draw_coords(self):
    font = pg.font.SysFont('Arial', self.font_size)
    font_surface = None
    if(self.settings['draw_coords']):
      font_surface = font.render(self.label, False, self.text_color)
    elif(self.settings['draw_rankfile']):
      if(self.label == 'A1'):
        font_surface = font.render(self.label, False, self.text_color)
      elif(self.rank):
        font_surface = font.render(self.rank, False, self.text_color)
      elif(self.file):
        font_surface = font.render(self.file, False, self.text_color)

    if(font_surface):
      self.surface.blit(font_surface, (self.pad, self.size - (self.pad + self.font_size)))

  def get_piece_bounds(self):
    piece_rect = self.piece.piece_png.get_rect()
    return (self.size/2 - piece_rect[3]/2, self.size/2 - piece_rect[2]/2)

  def remove_piece(self):
    removed_piece = None
    if(self.piece):
      removed_piece = self.piece
      self.piece = None
      self.fresh = False
    return removed_piece

  def highlight(self):
    pg.draw.rect(self.surface, (255,255,153), self.surface.get_rect(), 6)
    self.fresh = False

  def place_piece(self, piece):
    self.piece = piece
    self.piece.x = self.x
    self.piece.y = self.y  
    self.fresh = False
    return piece

  def within(self, pos):
    is_within = False
    if(self.piece):
      piece_xy = self.get_piece_bounds()
      in_x = pos[0] > self.x + piece_xy[0] and pos[0] < self.x + self.size - piece_xy[0]
      in_y = pos[1] > self.y + piece_xy[1] and pos[1] < self.y + self.size - piece_xy[1]
      is_within = in_x and in_y
    return is_within
