from flask import Flask, render_template
from flask_sockets import Sockets
from .game import AdkGame, AdkGameOptions
from .players.dumb import DumbPlayer
from .players.web_player import WebPlayer
import gevent

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/adk')
def echo_socket(ws):
    game = AdkGame([
        WebPlayer(ws),
        DumbPlayer()
    ], AdkGameOptions(
        width=500,
        height=300
    ))
    
    while game.turn():
        gevent.sleep(1 / game.opts.tps)


@app.route('/')
def hello():
    return render_template('index.html')