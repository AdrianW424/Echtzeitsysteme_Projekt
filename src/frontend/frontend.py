from flask import Flask, render_template, request, jsonify
from PIL import Image
import os

app = Flask(__name__)

import generator

imageBuffer = []
position = 0

@app.route("/next")
def createNextImage():
    global imageBuffer
    global position
    position += 1
    if (position < len(imageBuffer)-1):
        return imageBuffer[position]
    generator.getNextFrame()
    imageBuffer.append(generator.getCurrentImage())
    return(imageBuffer[-1])
   
@app.route("/prev")
def getPrevImage():
    global position
    global imageBuffer
    if (position > 0):
        position -= 1
    if position >= 0:
        return imageBuffer[position]
    position = 0
    return imageBuffer[0]

@app.route("/process_file", methods=['POST'])
def loadCSVFile():
    global imageBuffer
    if request.method == 'POST':
        file = request.files['file']
        if file:
            content = file.read().decode('utf-8')
            generator.openFromCSV(content)
            imageBuffer = []
            imageBuffer.append(generator.getCurrentImage())
            return(imageBuffer[0])
    return "Error", 400

@app.route("/savegif", methods=['POST'])
def saveGif():
    imageBuffer[0].save("export.gif", format='GIF', append_images=imageBuffer[1:], save_all=True, duration=200, loop=0)
    with open(imageBuffer[0].save("export.gif", format='GIF', append_images=imageBuffer[1:], save_all=True, duration=200, loop=0), 'rb') as f:
        gif_bytes = f.read()

    return gif_bytes



@app.route("/")
def home():
    return render_template("./home.html")

if __name__ == "__main__":
    app.run(debug=True)