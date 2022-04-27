### The game is based on the flipping number game
### 

from turtle import *
from random import choice
from functools import partial

# set game dimension to be 5 x 5
g_dim = 5
# use random.choice() to create the color for the game
g_game = [choice(['#0000FF', '#FF0000', '#FFFF00', '#008000', '#00FFFF']) for i in range(25)]
# provide the option to flip during the game
optionColor = ['#0000FF', '#FF0000', '#FFFF00', '#008000', '#00FFFF']

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
    global userOption
    userOption = userChosenColor

def draw(game, rows=5, columns=5, height=100, width=100):
    x = -200  
    y = -200
    squares = []
    for column in range(columns):
        for row in range(rows):
            square = prototype.clone()
            square.goto(column * (5+width) + x , row * (5+height) + y)
            square.color('white', game[row*5+column])
            squares.append(square)
    return squares
    
def refreshScreen(game, rows=5, columns=5, height=100, width=100):
    for square in squares:
        square.onclick(partial(userChosenTile, squares.index(square)))
        if state['framed'] == squares.index(square):
            square.color('black', game[squares.index(square)])
        else:
            square.color('white', game[squares.index(square)])
    update()

def userChosenTile(count, x, y):
    global state, R, C
    state['framed'] = count
    R = count // 5
    C = count % 5

def flipColor(row, col, game, orig, to):
    global userOption, state, R, C
    if orig == to:
        return game
    if row < 0 or row >= g_dim:
        return
    if col < 0 or col >= g_dim:
        return

    idx = row*g_dim+col   

    if game[idx] != orig:
        return
    #print(idx, 'excuted')
    game[idx] = to
    flipColor(row-1, col, game, orig, to)
    flipColor(row+1, col, game, orig, to)
    flipColor(row, col-1, game, orig, to)
    flipColor(row, col+1, game, orig, to)
    
    state = {'framed':None}
    R = None
    C = None
    userOption = None

    return game

# initialize the game status
state = {'framed':None}     # stores the number of the last selected tile, which will be framed with a black border
R = None                    # the row of the last selected tile
C = None                    # the column of the last selected tile
userOption = None           # the index of the select-to-flip-to color in the optionColor list

# create a prototype of the tiles
prototype = Turtle()
prototype.shape('square')
prototype.shapesize(5, 5, 5)
prototype.penup()

if __name__ == '__main__':
    hideturtle()
    # disable auto screen refresh
    tracer(False)
    squares = draw(g_game)
    update()
    # run the game
    while True:
        # the try and except block here is to prevent error from raising when user terminate the progarm
        try:
            promptColorToFlip(optionColor)
            refreshScreen(g_game)
            if state['framed'] is not None and R is not None and C is not None and userOption is not None:
                g_game = flipColor(R, C, g_game, g_game[state['framed']], optionColor[userOption])
        except:
            pass