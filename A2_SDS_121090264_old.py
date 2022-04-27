import turtle
import random

gameDimension = gameColumn = gameRow = 5
colorRange = 5
tilesSize = 100
tilesBorder = 20

screen = turtle.Screen()
screen.setup(800, 800)
screen.setworldcoordinates(-800, -800, 500, 500)
screen.title('Color Flipping Game')
turtle.speed(0)
turtle.hideturtle()
screen.tracer(0, 0)

def drawRectangle(x, y, width, height, color):
    turtle.up()
    turtle.goto(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.up()
    for _ in range(2):
        turtle.fd(width)
        turtle.right(90)
        turtle.fd(height)
        turtle.right(90)
    turtle.end_fill()
    turtle.down()

def createGame(column, row, color_range):
    gameBoard = []
    for _ in range(column):
        rowColor = []
        for _ in range(row):
            rowColor.append(random.randint(0, color_range-1))
        gameBoard.append(rowColor)
    return gameBoard

def findCoordinate(column, row, dimension, width, height, border):
    x = -(dimension*width+(dimension-1)*border)/2 + row*width + (row-1)*border
    y = -(dimension*height+(dimension-1)*border)/2 + column*width + (column-1)*border
    return x, y

def getColor(colorNum):
    colorDic = {
        '0': '#0000FF',
        '1': '#FF0000',
        '2': '#FFFF00',
        '3': '#008000',
        '4': '#00FFFF'
    }
    return colorDic[colorNum]

def draw():
    global gameBoard
    gameBoard = createGame(gameColumn, gameRow, colorRange)
    for column in range(gameColumn):
        for row in range(gameRow):
            color = getColor(str(gameBoard[column][row]))
            x, y = findCoordinate(column, row, gameDimension, tilesSize, tilesSize, tilesBorder)
            drawRectangle(x, y, tilesSize, tilesSize, color)

def findRow(x, dimension, width, border):
    row = 0
    for i in range (dimension):
        if (x >= -(dimension*width+(dimension-1)*border)/2 + i*(width+border)) and (x <= -(dimension*width+(dimension-1)*border)/2 + (i+1)*width):
            row = i+1
    return row

def findColumn(y, dimension, height, border):
    column = 0
    for i in range (dimension):
        if (y >= -(dimension*height+(dimension-1)*border)/2 + i*(height+border)) and (y <= -(dimension*height+(dimension-1)*border)/2 + (i+1)*height):
            column = i+1
    return column

def highlight(column, row, dimension, width, height, border):
    x, y = findCoordinate(column, row, dimension, width, height, border)
    turtle.pensize(5)
    turtle.up()
    turtle.goto(x, y)
    turtle.setheading(0)
    turtle.down()
    for _ in range(2):
        turtle.fd(width)
        turtle.right(90)
        turtle.fd(height)
        turtle.right(90)

def play(x, y):
    column = findColumn(y, gameDimension, tilesSize, tilesBorder)
    row = findRow(x, gameDimension, tilesSize, tilesBorder)
    highlight(column, row, gameDimension, tilesSize, tilesSize, tilesBorder)
    #flipColor(row, column, gameBoard, 0, 0)

def refreshScreen():
    pass

def showOption():
    pass

def flipColor(row, column, game, orig, to): 
    if orig == to:
        return game
    if row < 0 or row >= gameDimension:
        return
    if column < 0 or column >= gameDimension:
        return

    idx = row*gameDimension+column   
    if game[idx] != orig:
        return
    
    game[idx] = to
    flipColor(row-1, column, game, orig, to)
    flipColor(row+1, column, game, orig, to)
    flipColor(row, column-1, game, orig, to)
    flipColor(row, column+1, game, orig, to)
    
    return game


draw()
screen.onclick(play)
screen.mainloop()