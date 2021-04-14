# ADK Wars

This is a reimplementation of _Achtung, die Kurve_ / _Curve Fever_ / ..., but aimed towards being played in a bot-vs-bot setup.

## Component overview

### Game logic

Each player is an object subclassing `adk_server.game.AdkPlayer`. On game start, the `init` method is invoked with following parameters:

- `player_id` an integer representing our own ID (1 - 127)
- `opts` an options object of type `adk_server.game.AdkGameOptions`, with following properties:
  - `width`, `height`: width/height of the play area in units
  - `player_speed`: Speed of the snake in units per second
  - `turn_speed`: Turning speed in degrees per second
  - `snake_radius`: radius of the snake in units
  - `tps`: Ticks per second (state is updated once per tick)

As game progresses (and as long as the player is alive) the `get_turn` is invoked with following parameters:

- `game_state` a NumPy `NdArray` of signed bytes representing the play area. The values in the matrix represent the following:
  - `0`: empty space
  - `i > 0`: body of player `i` (will kill anyone if collided with)
  - `i < 0`: head of player `-i` (will kill anyone but that player)
- `x`, `y`: position of the snake head (float numbers)
- `dir`: rotation of the snake (in degrees, 0 - 360). 0 is in +x direction, 90 is in +y direction.

The `get_turn` should return 1, 0 or -1, representing a left, straight or right turn. Any other value is treated as 0. **It is not possible to do a partial turn.**

### Web server

The game is currently hosted on a WSGI web-server, and is only playable that way. The frontend communicates with the server using WebSockets.

## Setup

Clone the repo:

```sh
git clone https://github.com/profMagija/adk-wars
cd adk-wars
```

Install dependencies

```sh
pip install Flask Flask-Sockets
```

Start the server:

```sh
python -m adk_server
```