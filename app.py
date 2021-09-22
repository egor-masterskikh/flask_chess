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


@socketio.on("move")
def move_handler(data):
    row, col = map(int, data["from"])
    row1, col1 = map(int, data["to"])
    state = board.move(row, col, row1, col1)
    if state == board.SUCCESS_STATE:
        socketio.emit("success", data)
    elif state == board.FAIL_STATE:
        socketio.emit("fail", data)


if __name__ == '__main__':
    socketio.run(app, log_output=True)
