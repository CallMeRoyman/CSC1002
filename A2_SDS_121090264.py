# Based on Python 3.10.0 64-bit via VSC
# NOTICE!!!!! If you can see 30 tiles in your screen, it might be that your comupter screen is too small for the game, 
# TRY FULL SCREEN!!!
# In this game, rows are a group of tiles aligned horizontally starting from 0,
# columns are a group of tiles aligned vertically starting from 0.

from turtle import *
from random import choice
from functools import partial
 
# show a set of colors as option for user to flip
def promptColorToFlip(optionColor,  # a list that contains a set of the color for user to choose from
                    height=100,     # the height of the option tiles
                    width=100       # the width of the option tiles
                    ):
    # the coordinates of the first game tile
    x = -200
    y = -200

    # distribute option tiles to their position and fill colors
    for i in range(len(optionColor)):
        tile = prototypeForOptions[i]
        tile.goto(i * width + x, -(height+50) + y)      # 50 here is the distance between the option tiles and the game tiles at 0 row
        tile.color('black', optionColor[i])
 
# when the click event happen, it will return the index of the option tile in the optionColor list
# by changing the global variable userOption using the first input
def returnChosenColor(userChosenColor,  # the index of the select-to-flip-to color in the optionColor list
                        x, y            # take the positional arguments from the onclick() function to avoid raising errors, no significant meaning
                        ):
    global userOption
    userOption = userChosenColor
 
def refreshScreen(game,         # a list that contains the colors of the tiles
                rows=5,         # the numbers of the row in the game, defalut 5
                columns=5,      # the numbers of the columns in the game, default 5
                height=100,     # the height of the tiles, default 100
                width=100       # the width of the tiles, default 100
                ):
    # the coordinates of the first game tile
    x = -200  
    y = -200

    # distribute game tiles to their position and fill colors
    for column in range(columns):
        for row in range(rows):
            square = prototypeForScreens[row][column]
            square.goto(column * (5+width) + x , row * (5+height) + y)      # 5 here is the board width of every tile
            # if user click on a game tile, it will have a black borad else white
            if state['framed'] == row*g_dim+column:
                square.color('black', game[row*5+column])
            else:
                square.color('white', game[row*5+column])
    update()

# when the click event happen, it will return the row and column of the game tile
# by changing the global variable R, C using the first two input
def userChosenTile(ROW,         # the row of the clicked tile
                    COL,        # the column of the clicked tile
                    x, y        # take the positional arguments from the onclick() function to avoid raising errors, no significant meaning
                    ):
    global state, R, C
    state['framed'] = ROW*5+COL
    R = ROW
    C = COL

# the flipping color logic is the same as the flipping number logic taught in lecture
def flipColor(row,      # the row of the game tile
                col,    # the column of the game tile
                game,   # a list the store the color of the game tiles
                orig,   # the original color of the chosen game tile
                to      # the color of the chosen option tile
                ):
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

    game[idx] = to
    flipColor(row-1, col, game, orig, to)
    flipColor(row+1, col, game, orig, to)
    flipColor(row, col-1, game, orig, to)
    flipColor(row, col+1, game, orig, to)
    
    # reset the state of the game 
    state = {'framed':None}
    R = None
    C = None
    userOption = None
 
    return game

# Handle the case when user close the screen
def on_quit():
    global game_on
    game_on = False
 
if __name__ == '__main__':
    # set game dimension to be 5 x 5
    g_dim = 5
    # use random.choice() to create the color for the game
    g_game = [choice(['#0000FF', '#FF0000', '#FFFF00', '#008000', '#00FFFF']) for i in range(g_dim * g_dim)]
    # provide the option to flip during the game
    optionColor = ['#0000FF', '#FF0000', '#FFFF00', '#008000', '#00FFFF']
    
    # Prepare for the case when user close the screen directly
    screen = Screen()
    canvas = screen.getcanvas()
    root = canvas.winfo_toplevel()
    root.protocol("WM_DELETE_WINDOW", on_quit)
    game_on = True

    # set the screen size, in case some computer cannot see all the tiles
    screen.setup(600, 900)
    # initialize the state of the game
    state = {'framed':None}     # stores the number of the last selected tile, the last selected tile will be framed with a black border
    R = None                    # the row of the last selected tile
    C = None                    # the column of the last selected tile
    userOption = None           # the index of the select-to-flip-to color in the optionColor list
    
    # create a prototype of the tiles
    prototype = Turtle()
    prototype.shape('square')
    prototype.shapesize(5, 5, 5)
    prototype.penup()
    
    # disable auto screen refresh
    tracer(False)
    
    # create a list to store the option tiles
    prototypeForOptions = []
    for i in range(len(optionColor)):
        tile = prototype.clone()
        tile.onclick(partial(returnChosenColor, i))     #response to click event
        prototypeForOptions.append(tile)
    
    # create a list to store the game tiles
    prototypeForScreens = []
    for column in range(g_dim):
        prototypeForScreen = []
        for row in range(g_dim):
            square = prototype.clone()
            square.onclick(partial(userChosenTile, column, row))    # respond to click event
            prototypeForScreen.append(square)
        prototypeForScreens.append(prototypeForScreen)
    
    # run the game
    while game_on:
        # the try and except block here is to prevent error from raising when user terminate the progarm
        promptColorToFlip(optionColor)
        refreshScreen(g_game)
        if state['framed'] is not None and R is not None and C is not None and userOption is not None:
            # respond to the situation if the user flip to the same color
            if g_game[state['framed']] == optionColor[userOption]:
                state = {'framed':None}
                R = None
                C = None
                userOption = None
            else:
                g_game = flipColor(R, C, g_game, g_game[state['framed']], optionColor[userOption])
