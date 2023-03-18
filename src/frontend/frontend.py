from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO

app = Flask(__name__)

import generator

@app.route("/next")
def createNextImage():
    return generator.getImage('white', 'black', step=1)
   
@app.route("/prev")
def getPrevImage():
    return generator.getImage('white', 'black', step=-1)

@app.route("/process_file", methods=['POST'])
def loadCSVFile():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            content = file.read().decode('utf-8')
            generator.openFromCSV(content)
            return generator.getImage('white', 'black', step=0)
    return "Error", 400

@app.route("/savegif")
def saveGif():
    #imageBuffer[0].save("export.gif", format='GIF', append_images=imageBuffer[1:], save_all=True, duration=200, loop=0)
    
    ########### imageBuffer is deprecated, use generator.getImages('white', 'black', 0, 0) instead ###########

    with open("export.gif", 'rb') as f:
        gif_bytes = f.read()

    return gif_bytes



@app.route("/")
def home():
    return render_template("./home.html")

if __name__ == "__main__":
    app.run(debug=True)