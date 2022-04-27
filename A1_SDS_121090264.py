from random import randint

welcomeMessage = '''
        Welcome to 121090264's odd-ball game! You are given
        an even number of balls, labelled, and among
        the balls one is heavier than the rest, called the odd
        ball.

        Your goal is to find out which one is the odd one.
        You are given a weighing scale!

        Good Luck and Have Fun!

'''

weighingTips = '''
You are prompt to enter the balls
to be placed on the pans of the scale,
seperate each ball identifier with one
minimun space, e.g. 1 2 3
'''

inputErrorMessage = '''
Please ensure correct ball identifiers (1-{})
are entered on each pan, no duplicate balls on either
or both pans. Both pans should have the same number of
balls and must have at least one ball.
'''

# Create the number of balls player want
# Use randint() to choose one ball to be the odd ball
def createBalls():
    # Prompt user to enter the numbers of balls for the game
    check=True
    while check:
        preNumber=input('Enter the number of balls for the game:')
        try:
          int(preNumber)
          check=False
        except:
          print('Invalid input! Please input an integer!')
    ballNumbers = int(preNumber)

    # Prevent inproper input
    while ballNumbers % 2 != 0 or ballNumbers < 2:
        print('You have to enter an EVEN number with minimum 2 to continue the game!')
        ballNumbers = int(input('Enter the number of balls for the game:'))

    # Randomly choosees one ball as the odd ball
    specialBall = randint(1, ballNumbers)

    # Create a dictionary to store ball number and weight as key and value
    ballWithWeight = {}
    for i in range(1, ballNumbers+1):
        ballWithWeight[i] = 1
    ballWithWeight[specialBall] = 2

    # return the number of the odd ball and the dictionary
    return specialBall, ballWithWeight, ballNumbers

# Check if the inputs from promptWeighing() are valid
def verifyInput(leftInput,          # variable leftInput is the identifier(s) of the ball to be place on the left pan inputted by player
                rightInput,         # variable righttInput is the identifier(s) of the ball to be place on the right pan inputted by player
                leftBallKeyList,    # variable leftBallKeyList is a list that is created by using split() function on variable leftInput
                rightBallKeyList,   # variable rightBallKeyList is a list that is created by using split() function on variable rightInput
                ballNumbers         # variabke ballNumbers is the number of all the balls in the game inputted by player
                ):
    # check if players input consisent numbers of balls
    if len(leftBallKeyList) != len(rightBallKeyList) and (len(leftBallKeyList) != 0 and len(rightBallKeyList) != 0):
        print('Your inputs for left:{}, right:{}\n'.format(leftInput, rightInput))
        print('Invalid input!!!')
        print(inputErrorMessage.format(ballNumbers))
        return True
    # check if player inputs nothing
    if len(leftBallKeyList) == 0 or len(rightBallKeyList) == 0:
        print('You input nothing!')
        print('Invalid input!!!')
        print(inputErrorMessage.format(ballNumbers))
        return True
    # check if player inputs the same number on both sides
    for i in range(len(leftBallKeyList)):
        if leftBallKeyList[i] in rightBallKeyList:
            print('Your inputs for left:{}, right:{}\n'.format(leftInput, rightInput))
            print('You can\'t put one ball on both pans at the same time.')
            print('Invalid input!!!')
            print(inputErrorMessage.format(ballNumbers))
            return True
    # check if player inputs the same number on one side
    for element in leftBallKeyList:
        if leftBallKeyList.count(element) > 1:
            print('Your inputs for left:{}, right:{}\n'.format(leftInput, rightInput))
            print('Duplicate balls are not expected!')
            print('Invalid input!!!')
            print(inputErrorMessage.format(ballNumbers))
            return True
    for element in rightBallKeyList:
        if rightBallKeyList.count(element) > 1:
            print('Your inputs for left:{}, right:{}\n'.format(leftInput, rightInput))
            print('Duplicate balls are not expected!')
            print('Invalid input!!!')
            print(inputErrorMessage.format(ballNumbers))
            return True
    # check if player inputs other elements other than integer
    try:
        for element in (leftBallKeyList + rightBallKeyList):
            int(element)
            # check if player inputs numbers out of range
            if int(element) > ballNumbers:
                print('Your inputs for left:{}, right:{}\n'.format(leftInput, rightInput))
                print('Input out of range!')
                print('Invalid input!!!')
                print(inputErrorMessage.format(ballNumbers))
                return True
    except:
        print('Your inputs for left:{}, right:{}\n'.format(leftInput, rightInput))
        print('Invalid input!!!')
        print(inputErrorMessage.format(ballNumbers))
        return True

# prompt player to input the balls he wants to put on the pans
# variable ballWithWeight is all the balls in the game, it's a dictionary that contains ball number and weight as key and value
def promptWeighing(ballWithWeight):
    leftInput = input('Enter the ball identifiers(s) to be place on the left pan:')
    leftBallKeyList = leftInput.split()
    rightInput = input('Enter the ball identifiers(s) to be place on the right pan:')
    rightBallKeyList = rightInput.split()
    while verifyInput(leftInput, rightInput, leftBallKeyList, rightBallKeyList, ballNumbers):
        leftInput = input('Enter the ball identifiers(s) to be place on the left pan:')
        leftBallKeyList = leftInput.split()
        rightInput = input('Enter the ball identifiers(s) to be place on the right pan:')
        rightBallKeyList = rightInput.split()
    # Create two dictionary to store the identifier(s) and weight of the balls
    leftPan = {}
    rightPan = {}
    for i in leftBallKeyList:
        leftPan[i] = ballWithWeight[int(i)]
    for i in rightBallKeyList:
        rightPan[i] = ballWithWeight[int(i)]
    # return the dictionary with identifier(s) and weight of the balls as key(s) and value(s)
    return leftPan, rightPan

# add the weight of the balls to compare which side of the pan is heavier
def weighingScale(leftPan,  # variable leftPan is the ball(s) to be weight on the left pan, it's a dictionary
                rightPan    # variable rightPan is the ball(s) to be weight on the right pan, it's a dictionary
                ):
    weighingBallNumbers = len(leftPan)      # get the number of the ball(s) on the pan
    leftWeight = 0              # initialize the weight of the left pan
    rightWeight = 0             # initialize the weight of the right pan

    # Use the values of the dictionaries to create lists that store the weight of the ball(s)
    leftWeightList = list(leftPan.values())
    rightWeightList = list(rightPan.values())
    
    # add the weight of the balls together
    for i in range(weighingBallNumbers):
        leftWeight += leftWeightList[i]
        rightWeight += rightWeightList[i]

    # compare the weight of the balls
    if leftWeight == rightWeight:
        print('Balanced')
    elif leftWeight >= rightWeight:
        print('Left Heavier')
    else:
        print('Right Heavier')

# start a new game
def newGame():
    # global the numbers of all the balls
    global ballNumbers
    # global the identifier of the odd ball
    global specialBall
    # initialize the times of using the scale
    times = 0
    # initialize the player's input of odd ball
    result = None
    # welcome message of player interface
    print(welcomeMessage)
    # get the identifiers of the odd balls, 
    #   the dictionary with with identifiers and weight of the balls as keys and values, 
    #       the total number of the balls
    specialBall, ballWithWeight, ballNumbers = createBalls()
    # tips to instruct player to input the correct identifiers
    print(weighingTips)
    # loop to continue the guessing process until the odd ball is discovered
    while result != str(specialBall):
        # place the ball(s) on the pan
        leftPan, rightPan = promptWeighing(ballWithWeight)
        # weigh the balls
        weighingScale(leftPan, rightPan)
        # initialize the verification of the result
        verification = True
        while verification:
            # result is player's input about the odd ball
            result = input('Enter the odd ball number or press Enter to weigh:')
        # inquire if the player want to guess the odd ball or not
            if result == '':
                verification = False
            else:
                verification = verifyResult(result, ballNumbers, specialBall)
        print('\n')
        times += 1
    print('You use scale for {} time(s)'.format(times))

# check if the result is valid
def verifyResult(result,        # variable result is player's input about the odd ball
                ballNumbers,    # variable ballNumbers is the numbers of all the balls
                specialBall     # variable specialBall is the identifier of the odd ball
                ):
    try:
        # check if player enter a number bigger than the identifier of the odd ball 
        if int(result) > ballNumbers:
            print('Input out of range!')
            return True
        # check if the player enter the correct identifier of the odd ball
        else:
            if int(result) != specialBall:
                print('Wrong Guess! Try Again!')
                return False
            else:
                print('Correct! You Win!')
                return False
    # handle the situation when player input something other than number
    except:
        print('Invalid input!!!')
        return True


if '__main__' == __name__:
    # initialize the game
    status = True
    # run the game
    while status:
        newGame()
        # inquire if the player wants to start a new game, return True if yes, False otherwise
        answer = input('\nDo you want to start a new game?\nEnter \'Yes\' or \'Y\' to continue\nEnter \'No\' or \'N\' or anything to quit\n')
        if answer == 'Yes' or answer == 'Y':
            status = True
        else:
            status = False

# End of the code