const WIDTH = 1200
const HEIGHT = 1200
const ITERATIONS = 25
const OFFSET = 82

// Define the min() method for the Array object
Array.prototype.min = function (callback) {
    // Initialize the minimum value to null and the element to null
    let min = null;
    let element = null;

    // Loop through each element in the array
    this.forEach((currentElement) => {
        // Get the value for the current element by calling the
        // provided callback function
        const value = callback(currentElement);

        // Check if the value is less than the current minimum
        if (min === null || value < min) {
            // Update the minimum value and the element
            min = value;
            element = currentElement;
        }
    });

    // Return the element with the minimum value
    return element;
};


SVG.on(document, 'DOMContentLoaded', function () {
    const degrees_to_radians = deg => (deg * Math.PI) / 180.0;

    const width = WIDTH;
    const height = HEIGHT;
    const iterations = ITERATIONS;
    const startRColor = 78, endRColor = 255, startGColor = 89, endGColor = 255, startBColor = 100, endBColor = 255
    const offset = OFFSET

    // Create an SVG canvas
    const canvas = SVG().addTo('body').size(width, height);
    let leftTopPointX = 0
    let leftTopPointY = 0
    let rightTopPointX = width
    let rightTopPointY = 0
    let rightBottomPointX = width
    let rightBottomPointY = height
    let leftBottomPointX = 0
    let leftBottomPointY = height

    const gen0Polygon = canvas.polygon(`${leftTopPointX},${leftTopPointY} ${rightTopPointX},${rightTopPointY} ` +
        `${rightBottomPointX},${rightBottomPointY} ${leftBottomPointX},${leftBottomPointY}`).fill(rgbToHex(startRColor, startGColor, startBColor));

    let r = startRColor
    let g = startGColor
    let b = startBColor

    for (let i = 0; i < iterations; i++) {
        const previousTopLineCoords = bresenhamLine(Math.ceil(leftTopPointX),
            Math.ceil(leftTopPointY),
            Math.ceil(rightTopPointX),
            Math.ceil(rightTopPointY))

        const previousRightLineCoords = bresenhamLine(Math.ceil(rightTopPointX),
            Math.ceil(rightTopPointY),
            Math.ceil(rightBottomPointX),
            Math.ceil(rightBottomPointY))

        const previousBottomLineCoords = bresenhamLine(Math.ceil(leftBottomPointX),
            Math.ceil(leftBottomPointY),
            Math.ceil(rightBottomPointX),
            Math.ceil(rightBottomPointY))

        const previousLeftLineCoords = bresenhamLine(Math.ceil(leftBottomPointX),
            Math.ceil(leftBottomPointY),
            Math.ceil(leftTopPointX),
            Math.ceil(leftTopPointY))

        const angle = (45 / iterations) * (i)
        const rad = degrees_to_radians(angle)

        const cAngle = (Math.cos(rad)) * offset
        const sAngle = (Math.sin(rad)) * offset

        leftTopPointX = leftTopPointX + cAngle
        leftTopPointY = leftTopPointY + sAngle
        rightTopPointX = rightTopPointX - sAngle
        rightTopPointY = rightTopPointY + cAngle
        rightBottomPointX = rightBottomPointX - cAngle
        rightBottomPointY = rightBottomPointY - sAngle
        leftBottomPointX = leftBottomPointX + sAngle
        leftBottomPointY = leftBottomPointY - cAngle

        const leftTopLinePoint = closestPoint(leftTopPointX, leftTopPointY, previousTopLineCoords);
        const rightTopLinePoint = closestPoint(rightTopPointX, rightTopPointY, previousRightLineCoords)
        const rightBottomLinePoint = closestPoint(rightBottomPointX, rightBottomPointY, previousBottomLineCoords)
        const leftBottomLinePoint = closestPoint(leftBottomPointX, leftBottomPointY, previousLeftLineCoords)

        leftTopPointX = leftTopLinePoint.x
        leftTopPointY = leftTopLinePoint.y
        rightTopPointX = rightTopLinePoint.x
        rightTopPointY = rightTopLinePoint.y
        rightBottomPointX = rightBottomLinePoint.x
        rightBottomPointY = rightBottomLinePoint.y
        leftBottomPointX = leftBottomLinePoint.x
        leftBottomPointY = leftBottomLinePoint.y

        const nextFill = rgbToHex(((endRColor - startRColor) / iterations) * (i + 1) + startRColor,
            ((endGColor - startGColor) / iterations) * (i + 1) + startGColor,
            ((endBColor - startBColor) / iterations) * (i + 1) + startBColor)


        const poly = canvas.polygon(`${leftTopPointX},${leftTopPointY} ${rightTopPointX},${rightTopPointY} ` +
            `${rightBottomPointX},${rightBottomPointY} ${leftBottomPointX},${leftBottomPointY}`).fill(nextFill)
    }
    // let rectWidth = 100;
    // let rectHeight = 100;

    // // Define the initial position of the rectangles
    // let rectX = 200;
    // let rectY = 200;

    // // Define the x/y offset for the rectangles
    // const offsetX = 100;
    // const offsetY = 100;

    // // Define the initial rotation angle for the rectangles
    // let rectAngle = 0;

    // // Create a loop to draw the rectangles
    // for (let i = 0; i < 13; i++) {
    //     // Determine the fill color for the rectangle
    //     const fillColor = i === 0 ? '#000000' : `hsl(0, 0%, ${i * 8}%)`;

    //     // Determine the rotation angle for the rectangle
    //     rectAngle = (45 / (13 * (i + 1)));

    //     // Determine the dimensions of the rectangle
    //     rectWidth = 100 - i * 6;
    //     rectHeight = 100 - i * 6;

    //     // Draw the rectangle
    //     const rect = canvas
    //         .rect(rectWidth, rectHeight)
    //         .attr({ fill: fillColor })
    //         .rotate(rectAngle);
    // }
})

function closestPoint(x, y, coordinates) {
    return coordinates.min((point) => {
        // Calculate the distance between the given x and y values
        // and the current point
        const distance = Math.hypot(point.x - x, point.y - y);

        // Return the distance
        return distance;
    });
}

function rgbToHex(r, g, b) {
    return "#" + (1 << 24 | r << 16 | g << 8 | b).toString(16).slice(1);
}


function bresenhamLine(x0, y0, x1, y1) {
    // Set the starting and ending points for the line
    let x = x0;
    let y = y0;
    const endX = x1;
    const endY = y1;

    // Calculate the deltas for the x and y axes
    const deltaX = Math.abs(endX - x);
    const deltaY = Math.abs(endY - y);

    // Determine the direction of the line
    const sx = (x < endX) ? 1 : -1;
    const sy = (y < endY) ? 1 : -1;

    // Initialize the error variable
    let err = deltaX - deltaY;

    // Create an array to store the points on the line
    const points = [];

    // Loop until the line is drawn
    while (true) {
        // Add the current point to the array
        points.push({ x, y });

        // Check if we've reached the end of the line
        if (x === endX && y === endY) {
            break;
        }

        // Calculate the error value
        const e2 = 2 * err;

        // Check which direction to move in
        if (e2 > -deltaY) {
            err -= deltaY;
            x += sx;
        }
        if (e2 < deltaX) {
            err += deltaX;
            y += sy;
        }
    }

    // Return the array of points
    return points;
}