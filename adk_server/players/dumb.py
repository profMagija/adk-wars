from ..game import AdkPlayer

class DumbPlayer(AdkPlayer):
    def get_turn(self, game_state, x: float, y: float, dir: float) -> int:
        return 0
