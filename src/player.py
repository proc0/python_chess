
class Player:
  history = []
  piece = None
  def __init__(self, props):
    for k, v in props.items():
      setattr(self, k, v)

  def move(self, player_action):
    if(player_action['board_click']):
      self.history.append({
        'pos': player_action['pos']
        })
