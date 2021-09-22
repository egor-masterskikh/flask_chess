from flask import Flask, render_template
from chess.board import Board
from jinja2.filters import FILTERS
from flask_socketio import SocketIO


app = Flask(__name__)
app.config["SECRET_KEY"] = "some_secret_key"
socketio = SocketIO(app)

board = Board()

FILTERS["enumerate"] = enumerate


@app.route("/game")
def game():
    return render_template("game.html", board=board)


@socketio.on("my event")
def my_event_handler(message):
    print(f"received message: {message['data']}")


if __name__ == '__main__':
    socketio.run(app, log_output=True)
