from flask import Flask, render_template
from chess.board import Board
from jinja2.filters import FILTERS

app = Flask(__name__)
board = Board()

FILTERS["enumerate"] = enumerate


@app.route("/game")
def game():
    return render_template("game.html", board=board)


if __name__ == '__main__':
    app.run(port=8080)
