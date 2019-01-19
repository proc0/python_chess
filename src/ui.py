
class UI():
    def __init__(self):
        self.font = pg.font.Font(None, 30)
        self.ui = pg.Surface((self.win_size[0]-board.size[0], board.size[0]))

    def draw(self, fps):
      fps = font.render(str(int(fps)), True, pg.Color('white'))
      self.ui.fill((0,0,0))
      self.ui.blit(fps, (20,20))