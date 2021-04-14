from ..game import AdkGameOptions, AdkPlayer

class WallAvoidingPlayerr(AdkPlayer):
    def init(self, opts: AdkGameOptions):
        self.w = opts.width
        self.h = opts.height
        self.turn_radius = opts.player_speed * (90 / opts.turn_speed) * 0.84

    def get_turn(self, game_state, x: float, y: float, dir: float) -> int:

        going_up = 0 < dir <= 180
        going_down = not going_up

        going_left = 90 < dir <= 270
        going_right = not going_left
        
        if x < self.turn_radius and going_left:
            if going_up:
                return -1
            else:
                return 1
        if x > self.w - self.turn_radius and going_right:
            if going_up:
                return 1
            else:
                return -1
        if y < self.turn_radius and going_down:
            if going_left:
                return -1
            else:
                return 1
        if y > self.h - self.turn_radius and going_up:
            if going_left:
                return 1
            else:
                return -1