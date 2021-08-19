from flask import Flask, render_template
from itertools import product

app = Flask(__name__)


@app.route("/game")
def game():
    coords = product(range(8), repeat=2)
    return render_template("game.html", coords=coords)


if __name__ == '__main__':
    app.run(port=8080)
