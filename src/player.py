
class Player:
  history = []
  piece = None
  def __init__(self, props):
    for k, v in props.items():
      setattr(self, k, v)

  def move(self, square):
      self.history.append(square)
