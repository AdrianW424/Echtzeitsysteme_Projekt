from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

import generator

@app.route("/next")
def createNextImage():
    generator.getNextFrame()
    return(generator.getCurrentImage())
   
# @app.route("/prev")
# imageBuffer = []
# position = 0
# def getPrevImage():
#     global position
#     position -= 1
#     if position >= 0:
#         return imageBuffer[position]
#     return imageBuffer[0]

@app.route("/process_file", methods=['POST'])
def loadCSVFile():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            content = file.read().decode('utf-8')
            generator.openFromCSV(content)
            return(generator.getCurrentImage())
    return "Error", 400

@app.route("/")
def home():
    return render_template("./home.html")

if __name__ == "__main__":
    app.run(debug=True)