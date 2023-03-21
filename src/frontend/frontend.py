from flask import Flask, render_template, request

app = Flask(__name__)

import generator

color = 'white'
inverseColor = 'black'

@app.route("/next")
def createNextImage():
    return generator.getSingleImage(color, inverseColor, step=1)

@app.route("/prev")
def getPrevImage():
    return generator.getSingleImage(color, inverseColor, step=-1)

@app.route("/process_file", methods=['POST'])
def loadCSVFile():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            content = file.read().decode('utf-8')
            res = generator.openFromCSV(content)
            if res[0] == False:
                # TODO: Show error message
                return 'None'
            else:
                return generator.getSingleImage(color, inverseColor, step=0)
    return "Error", 400

@app.route("/savegif")
def saveGif():
    ###### TODO: Maybe set the duration of the gif ######
    return generator.createGIF(color, inverseColor, 0, 0, 1000)

@app.route("/darkmode_toggle", methods=['POST'])
def darkmodeToggle():
    if request.method == 'POST':
        global color
        global inverseColor
        
        data = request.get_json()
        if data['darkmode'] == True:
            color = 'black'
            inverseColor = 'white'
        else:
            color = 'white'
            inverseColor = 'black'
        
        return generator.getSingleImage(color, inverseColor, step=0)
    return "Error", 400
    # if 
    # return generator.createGIF('white', 'black', 0, 0)

@app.route("/")
def home():
    return render_template("./home.html")

if __name__ == "__main__":
    app.run(debug=True)