from turtle import *
from random import choice
from functools import partial

# set game dimension to be 5 x 5
g_dim = 5

# provide the option to flip during the game
optionColor = ['#0000FF', '#FF0000', '#FFFF00', '#008000', '#00FFFF']

# show a set of colors as option for user to flip #
def createGame(n, option):
    COLORS = []
    for i in range(n*n):
        COLORS.append(choice(option))
    return  COLORS
# show a set of colors as option for user to flip
def promptColorToFlip(optionColor,  # a list that contains a set of the color for user to choose from
                    height=100,     # the height of the option tiles
                    width=100       # the width of the option tiles
                    ):
    # the coordinates of the first tile
    x = -200
    y = -200

    for i in range(len(optionColor)):
        tile = prototype.clone()
        tile.goto(i * width + x, -(height+50) + y)
        tile.color('white', optionColor[i])
        tile.onclick(partial(returnChosenColor, i))

# return the index of the select-to-flip-to color in the optionColor list
def returnChosenColor(userChosenColor,  # the index of the select-to-flip-to color in the optionColor list
                        x, y            # take the positional arguments from the onclick() function to avoid errors, no significant meaning
                        ):
    global playerOption
    playerOption = userChosenColor

def refreshScreen(game, rows=5, columns=5, height=100, width=100):
    x = -200  
    y = -200

    for column in range(columns):
        for row in range(rows):
            square = prototype.clone()
            square.goto(column * (5+width) + x , row * (5+height) + y)
            square.onclick(partial(userChosenTile, row, column))
            if frameTile['framed'] == row*5+column:
                square.color('black', game[row*5+column])
            else:
                square.color('white', game[row*5+column])
    update()

def userChosenTile(ROW, COL, x, y):
    global frameTile, gameRow, gameCol
    frameTile['framed'] = ROW*5+COL
    gameRow = ROW
    gameCol = COL

def colorFlipping(row, col, game, orig, to):
    global playerOption, frameTile, gameRow, gameCol
    if orig == to:
        return game
    if row < 0 or row >= g_dim:
        return
    if col < 0 or col >= g_dim:
        return

    idx = row*g_dim+col   

    if game[idx] != orig:
        return

    game[idx] = to
    colorFlipping(row-1, col, game, orig, to)
    colorFlipping(row+1, col, game, orig, to)
    colorFlipping(row, col-1, game, orig, to)
    colorFlipping(row, col+1, game, orig, to)
    
    frameTile = {'framed':None}
    gameRow = None
    gameCol = None
    playerOption = None

    return game

# initialize the game status
frameTile = {'framed':None}     # stores the number of the last selected tile, which will be framed with a black border
gameRow = None                    # the row of the last selected tile
gameCol = None                    # the column of the last selected tile
playerOption = None           # the index of the select-to-flip-to color in the optionColor list

# create game
g_game = createGame(g_dim, optionColor)

# create a prototype of the tiles
prototype = Turtle()
prototype.shape('square')
prototype.shapesize(5, 5, 5)
prototype.penup()

if __name__ == '__main__':
    # disable auto screen refresh
    tracer(False)
    # run the game
    while True:
        # the try and except block here is to prevent error from raising when user terminate the progarm
        try:
            promptColorToFlip(optionColor)
            refreshScreen(g_game)
            if frameTile['framed'] is not None and gameRow is not None and gameCol is not None and playerOption is not None:
                g_game = colorFlipping(gameRow, gameCol, g_game, g_game[frameTile['framed']], optionColor[playerOption])
        except:
            pass