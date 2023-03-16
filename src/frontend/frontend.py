from flask import Flask, render_template, request
app = Flask(__name__)

import generator


@app.route("/next")
def createNextImage():
    generator.getNextFrame()
    return(generator.getCurrentImage())
   
imageBuffer = []
position = 0
@app.route("/prev")
def getPrevImage():
    global position
    position -= 1
    if position >= 0:
        return imageBuffer[position]
    return imageBuffer[0]

generator.openFromCSV("src/frontend/dataTest2.csv")
@app.route("/process_file", methods=['POST'])
def loadCSVFile():
    path = request.form.get('path')
    generator.openFromCSV(path)

@app.route("/")
def home():
    return render_template("./home.html")

if __name__ == "__main__":
    app.run(debug=True)