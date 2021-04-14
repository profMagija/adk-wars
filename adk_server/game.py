from dataclasses import dataclass
import dataclasses
from typing import Iterable
import numpy as np
import random
import math


@dataclass
class AdkGameOptions:
    width: int = 300
    height: int = 300

    player_speed: float = 30
    turn_speed: float = 90
    snake_radius: float = 2.5

    tps: float = 30


class AdkPlayer:
    def init(self, player_id: int, opts: AdkGameOptions):
        pass

    send_turn = None

    def get_turn(self, game_state: np.ndarray, x: float, y: float, dir: float) -> int:
        raise NotImplementedError


class AdkGame:
    def __init__(self, players: Iterable[AdkPlayer], opts: AdkGameOptions):
        self.players = tuple(players)
        self.num_players = len(players)
        self.opts = opts
        self._state = np.zeros(
            (self.opts.width, self.opts.height), dtype=np.int8)
        self._player_pos = [
            (random.uniform(self.opts.width / 4, self.opts.width * 3 / 4),
             random.uniform(self.opts.height / 4, self.opts.height * 3 / 4))
            for _ in self.players]
        self._player_alive = [True for _ in self.players]
        # self._player_dir = [90 for _ in self.players]
        self._player_dir = [random.uniform(0, 360) for _ in self.players]

        for i, p in enumerate(self.players):
            p.init(i+1, AdkGameOptions(**dataclasses.asdict(opts)))

    def _draw_snakes(self):
        R = self.opts.snake_radius
        R2 = R*R

        for i, ((px, py), pr) in enumerate(zip(self._player_pos, self._player_dir)):
            # rx, ry = math.sin(math.radians(pr)), math.cos(math.radians(pr))
            for cx in range(math.floor(px - 2*R), math.ceil(px + 2*R)):
                for cy in range(math.floor(py - 2*R), math.ceil(py + 2*R)):
                    if cx < 0 or cx >= self.opts.width or cy < 0 or cy >= self.opts.height:
                        continue
                    dx, dy = cx - px, cy - py
                    if dx*dx + dy*dy <= R2:
                        if self._state[cx, cy] == 0:
                            self._state[cx, cy] = -(i+1)
                    elif self._state[cx, cy] == -(i+1):
                        self._state[cx, cy] = i+1

    def _move_snakes(self):
        for pi, (player, (px, py), pr, p_alive) in enumerate(zip(self.players, self._player_pos, self._player_dir, self._player_alive)):
            if player.send_turn:
                player.send_turn(self._state.copy(), px, py, pr)
            if not p_alive:
                continue
            answer = player.get_turn(self._state.copy(), px, py, pr)
            if answer == -1:
                pr -= self.opts.turn_speed / self.opts.tps
            elif answer == 1:
                pr += self.opts.turn_speed / self.opts.tps

            pr %= 360
            if pr < 0:
                pr += 360

            px += math.cos(math.radians(pr)) * \
                self.opts.player_speed / self.opts.tps
            py += math.sin(math.radians(pr)) * \
                self.opts.player_speed / self.opts.tps

            self._player_pos[pi] = (px, py)
            self._player_dir[pi] = pr

    def _check_colision(self):
        for pi, ((px, py), p_alive) in enumerate(zip(self._player_pos, self._player_alive)):
            if not p_alive:
                continue

            cx, cy = math.floor(px), math.floor(py)

            # print(px, py, cx, cy)

            if (px > self.opts.width or px < 0
                or py > self.opts.height or py < 0
                    or self._state[cx, cy] not in (0, -(pi+1))):
                self._player_alive[pi] = False

    def turn(self):
        self._draw_snakes()
        self._move_snakes()
        self._check_colision()

        # print(self._state)

        return sum(self._player_alive) > 1

    def get_winner(self):
        if sum(self._player_alive) != 1:
            return None

        return self._player_alive.index(True) + 1
