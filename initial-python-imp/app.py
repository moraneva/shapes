from flask import Flask, render_template, request
from render import render as render_graphic, defaultAngleFunc
from PIL import Image as NewImage, EpsImagePlugin
app = Flask(__name__)

EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs10.00.0\bin\gswin64.exe'

@app.route("/")
def render():
    width = request.args.get('width', 1200, int)
    height = request.args.get('height', 1200, int)
    offset = request.args.get('offset', 50, int)
    iterations = request.args.get('iterations', 13, int)
    startRColor = request.args.get('startRColor', 0, int)
    endRColor = request.args.get('endRColor', 0, int)
    startGColor = request.args.get('startGColor', 0, int)
    endGColor = request.args.get('endGColor', 0, int)
    startBColor = request.args.get('startBColor', 0, int)
    endBColor = request.args.get('endBColor', 0, int)

    graphicWindow = render_graphic(width, height, offset, iterations, defaultAngleFunc, startRColor,
           endRColor, startGColor, endGColor, startBColor, endBColor)


    graphicWindow.postscript(file = "temp.eps")

    img = NewImage.open("temp.eps")
    img.save("temp.gif", "gif")
    graphicWindow.close()
    return render_template('render.html')
