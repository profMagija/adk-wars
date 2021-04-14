from ..game import AdkGameOptions, AdkPlayer
import numpy as np
import json
from gevent import Greenlet

class WebPlayer(AdkPlayer):
    def __init__(self, ws):
        self.ws = ws
        self._dir = 0
        
        self.t = Greenlet(self._webthread)
        self.t.start()
    
    def _webthread(self):
        while not self.ws.closed:
            d = self.ws.receive()
            if d is None: return
            self._dir = int(d)

    def init(self, player_id, opts: AdkGameOptions):
        self.ws.send(b's' + json.dumps(opts.__dict__).encode())
    
    def send_turn(self, game_state: np.ndarray, x: float, y: float, dir: float):
        self.ws.send(b'b' + np.abs(game_state).tobytes())

    def get_turn(self, game_state: np.ndarray, x: float, y: float, dir: float) -> int:
        return self._dir