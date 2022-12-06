from graphics import *
import math

def defaultAngleFunc(totalIterations, currentIteration):
    return (45/totalIterations)*(currentIteration+1) if currentIteration != 0 else 0

def render(width = 1200, height = 1200, offset = 50, iterations = 13, angleFunc = defaultAngleFunc, 
    startRColor = 0, endRColor = 255, startGColor = 0, endGColor = 255, startBColor = 0, endBColor = 255):
    
    win = GraphWin("The Void", width, height)
    phi = ( 1 + math.sqrt(5) ) / 2
    leftTopPointX = 0
    leftTopPointY = 0
    rightTopPointX = width
    rightTopPointY = 0
    rightBottomPointX = width
    rightBottomPointY = height
    leftBottomPointX = 0
    leftBottomPointY = height
    print('here')
    
    gen0 = Polygon(Point(leftTopPointX,leftTopPointY),
                   Point(rightTopPointX,rightTopPointY),
                   Point(rightBottomPointX,rightBottomPointY),
                   Point(leftBottomPointX,leftBottomPointY))
    
    gen0.setFill(color_rgb(int(startRColor),int(startGColor),int(startBColor)))
    gen0.draw(win)

    r,g,b = startRColor,startGColor,startBColor
    
    for x in range(iterations):
        
        previousTopLineCoords = bresenham(math.ceil(leftTopPointX),
                                       math.ceil(leftTopPointY), 
                                       math.ceil(rightTopPointX),
                                       math.ceil(rightTopPointY), win)
        
        previousRightLineCoords = bresenham(math.ceil(rightTopPointX),
                                       math.ceil(rightTopPointY), 
                                       math.ceil(rightBottomPointX),
                                       math.ceil(rightBottomPointY), win)
        
        previousBottomLineCoords = bresenham(math.ceil(leftBottomPointX),
                                       math.ceil(leftBottomPointY), 
                                       math.ceil(rightBottomPointX),
                                       math.ceil(rightBottomPointY), win)
        
        previousLeftLineCoords = bresenham(math.ceil(leftBottomPointX),
                                       math.ceil(leftBottomPointY), 
                                       math.ceil(leftTopPointX),
                                       math.ceil(leftTopPointY), win)
        
        angle = angleFunc(iterations, x)
        
        print(angle)
        rad = math.radians(angle)
        cAngle = (math.cos(rad))*offset
        sAngle = (math.sin(rad))*offset
        
        # Find closest points on previous rednered line
        leftTopPointX = leftTopPointX + cAngle
        leftTopPointY = leftTopPointY + sAngle
        rightTopPointX = rightTopPointX - sAngle
        rightTopPointY = rightTopPointY+ cAngle
        rightBottomPointX = rightBottomPointX - cAngle
        rightBottomPointY = rightBottomPointY - sAngle
        leftBottomPointX = leftBottomPointX+sAngle
        leftBottomPointY = leftBottomPointY - cAngle
        
        leftTopLinePoint = findClosestPointOnLine(leftTopPointX, leftTopPointY, previousTopLineCoords)
        rightTopLinePoint = findClosestPointOnLine(rightTopPointX, rightTopPointY, previousRightLineCoords)
        rightBottomLinePoint = findClosestPointOnLine(rightBottomPointX, rightBottomPointY, previousBottomLineCoords)
        leftBottomLinePoint = findClosestPointOnLine(leftBottomPointX, leftBottomPointY, previousLeftLineCoords)
        
        leftTopPointX = leftTopLinePoint[0]
        leftTopPointY = leftTopLinePoint[1]
        rightTopPointX = rightTopLinePoint[0]
        rightTopPointY = rightTopLinePoint[1]
        rightBottomPointX = rightBottomLinePoint[0]
        rightBottomPointY = rightBottomLinePoint[1]
        leftBottomPointX = leftBottomLinePoint[0]
        leftBottomPointY = leftBottomLinePoint[1]
        
        leftTopPoint = Point(leftTopPointX,leftTopPointY)
        rightTopPoint = Point(rightTopPointX,rightTopPointY)
        rightBottomPoint = Point(rightBottomPointX,rightBottomPointY)
        leftBottomPoint = Point(leftBottomPointX,leftBottomPointY)
        
        genX = Polygon(leftTopPoint,rightTopPoint, rightBottomPoint, leftBottomPoint)
        r,g,b = (((endRColor-startRColor)/iterations)*(x+1) + startRColor,((endGColor-startGColor)/iterations)*(x+1) + startGColor,((endBColor-startBColor)/iterations)*(x+1) + startBColor)
        fill = color_rgb(int(r),int(g),int(b))
        genX.setOutline(fill)
        genX.setFill(fill)
        genX.draw(win)


    
    win.getMouse() # pause for click in window
    win.postscript(file = "smoothie-bowl.eps")
    from PIL import Image as NewImage
    from PIL import EpsImagePlugin
    EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs10.00.0\bin\gswin64.exe'
    img = NewImage.open("smoothie-bowl.eps")
    img.save("smoothie-bowl.gif", "gif")
    win.close()


def findClosestPointOnLine(x, y, lineCoordinates):
    closestDistance = 100000 # arbitrary?
    transformedX = x
    transformedY = y
    for (xC, yC) in lineCoordinates:
        xDiff = pow(xC - x,2)
        yDiff = pow(yC - y,2)
        d = math.sqrt(xDiff + yDiff)
        if d < closestDistance:
            transformedX = xC
            transformedY = yC
            closestDistance = d
    return (transformedX, transformedY)    

def bresenham(x0, y0, x1, y1, win):
    """Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result will contain both the start and the end point.
    """
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy
