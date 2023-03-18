from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import generator

@app.route("/next")
def createNextImage():
    return generator.getSingleImage('white', 'black', step=1)
   
@app.route("/prev")
def getPrevImage():
    return generator.getSingleImage('white', 'black', step=-1)

@app.route("/process_file", methods=['POST'])
def loadCSVFile():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            content = file.read().decode('utf-8')
            generator.openFromCSV(content)
            return generator.getSingleImage('white', 'black', step=0)
    return "Error", 400

@app.route("/savegif")
def saveGif():
    return generator.createGIF('white', 'black', 0, 0)



@app.route("/")
def home():
    return render_template("./home.html")

if __name__ == "__main__":
    app.run(debug=True)