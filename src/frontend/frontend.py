from flask import Flask, render_template
import os

import generator

from io import BytesIO
from PIL import Image

app = Flask(__name__)


@app.route("/next")
def next():
    return(generator.next_frame())

@app.route("/prev")
def prev():
    return(generator.prev_frame())

@app.route("/")
def home():
    return render_template("./home.html")

if __name__ == "__main__":
    app.run(debug=True)