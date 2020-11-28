#  2/17 by Irv Kalb
#

import pygame
import random
import sys
import pygwidgets
from pygame.locals import *

from Constants import *
from Square import *
from Line import *


# The following is a list of lists.  Each line corresponds to a single Box
# The numbers in each inner list are the line numbers of the lines that surround the Box
# The line numbers represent horizontal lines first,
# so the top row is box number 0, 1, 2, 3, 4, second row is 5, 6, 7, 8, 9
# When we reach the bottom, then the vertical lines are numbered accross
# This is, the vertical lines int he first row are 30, 31, 32, 33, 34, 35.
# And the last row is:  54, 55, 56, 57, 58, 59

SQUARES_TO_LINES_LIST = [
    [0, 30, 31, 5],
    [1, 31, 32, 6],
    [2, 32, 33, 7],
    [3, 33, 34, 8],
    [4, 34, 35, 9],
    [5, 36, 37, 10],
    [6, 37, 38, 11],
    [7, 38, 39, 12],
    [8, 39, 40, 13],
    [9, 40, 41, 14],
    [10, 42, 43, 15],
    [11, 43, 44, 16],
    [12, 44, 45, 17],
    [13, 45, 46, 18],
    [14, 46, 47, 19],
    [15, 48, 49, 20],
    [16, 49, 50, 21],
    [17, 50, 51, 22],
    [18, 51, 52, 23],
    [19, 52, 53, 24],
    [20, 54, 55, 25],
    [21, 55, 56, 26],
    [22, 56, 57, 27],
    [23, 57, 58, 28],
    [24, 58, 59, 29]
]

# This is a list of lists that tells us
# for every line, what squares is it attached to.
# A line may only affect one square if it is on the outside border
# (e.g., lines 0, 1, 2, 3, 4, 5, 9, etc.)
# Or it may affect two squares if it is an interior line
# e.g. line 5 affects squares 0 and 5.

LINES_TO_SQUARES_LIST = [
    [0], [1], [2], [3], [4],
    [0, 5], [1, 6], [2, 7], [3, 8], [4, 9],
    [5, 10], [6, 11], [7, 12], [8, 13], [9, 14],
    [10, 15], [11, 16], [12, 17], [13, 18], [14, 19],
    [15, 20], [16, 21], [17, 22], [18, 23], [19, 24],
    [20], [21], [22], [23], [24],
    [0], [0, 1], [1, 2], [2, 3], [3, 4], [4],
    [5], [5, 6], [6, 7], [7, 8], [8, 9], [9],
    [10], [10, 11], [11, 12], [12, 13], [13, 14], [14],
    [15], [15, 16], [16, 17], [17, 18], [18, 19], [19],
    [20], [20, 21], [21, 22], [22, 23], [23, 24], [24]
]

COMPUTER_TURN = USEREVENT + 1
HUMAN_TURN = USEREVENT + 2
HUMAN_TURN_AGAIN = USEREVENT + 3


### MAIN CODE ###

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Lines and Boxes')
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class SquareMgr(object):
    def __init__(self, window):
        # Layout Squares
        self.window = window
        emptySquareImage = pygame.image.load('images/squareEmpty.png')
        humanSquareImage = pygame.image.load('images/squareHuman.png')
        computerSquareImage = pygame.image.load('images/squareComputer.png')
        self.squaresList = []
        thisSquareNumber = 0
        for rowNum in range(0, NROWS):
            for colNum in range(0, NCOLS):

                thisSquaresToLinesList = SQUARES_TO_LINES_LIST[thisSquareNumber]
                thisX = STARTING_X  + LINE_SIZE+ ((BOX_AND_LINE_SIZE * colNum))
                thisY = STARTING_Y  + LINE_SIZE+ ((BOX_AND_LINE_SIZE * rowNum))

                oSquare = Square(self.window, thisSquaresToLinesList, thisX, thisY, \
                                 emptySquareImage, humanSquareImage, computerSquareImage)
                self.squaresList.append(oSquare)
                thisSquareNumber = thisSquareNumber + 1

        self.mReset()

    def mReset(self):
        for square in self.squaresList:
            square.mReset()

    def draw(self):
        for square in self.squaresList:
            square.draw()

    def mSetTaken(self, squareNumber, newOwner):
        oSquare = self.squaresList[squareNumber]
        oSquare.mSetOwner(newOwner)


    def mGetLinesList(self, squareNumber):
        oSquare = self.squaresList[squareNumber]
        linesList = oSquare.mGetLines()
        return linesList



class LineMgr(object):
    H_WIDTH = 46
    H_HEIGHT = 13
    V_WIDTH = 13
    V_HEIGHT = 46

    def __init__(self, window):
        # Layout Horizontal lines
        self.linesList = []
        thisLineNumber = 0
        for rowNum in range(0, NROWS + 1):
            for colNum in range(0, NCOLS):
                thisLinesToSquaresList = LINES_TO_SQUARES_LIST[thisLineNumber]

                thisX = STARTING_X + LINE_SIZE + (BOX_AND_LINE_SIZE * colNum)
                thisY = STARTING_Y + (BOX_AND_LINE_SIZE * rowNum)
                oLine = Line(window, "H", thisLineNumber, thisX, thisY, \
                             LineMgr.H_WIDTH, LineMgr.H_HEIGHT, thisLinesToSquaresList)

                self.linesList.append(oLine)
                thisLineNumber = thisLineNumber + 1


        # Layout Vertical lines
        for rowNum in range(0, NROWS):
            for colNum in range(0, NCOLS + 1):
                thisLinesToSquaresList = LINES_TO_SQUARES_LIST[thisLineNumber]
                thisX = STARTING_X + (BOX_AND_LINE_SIZE * colNum)
                thisY = STARTING_Y +  + LINE_SIZE + (BOX_AND_LINE_SIZE * rowNum)
                oLine = Line(window, "V", thisLineNumber, thisX, thisY, \
                             LineMgr.V_WIDTH, LineMgr.V_HEIGHT, thisLinesToSquaresList)
                self.linesList.append(oLine)
                thisLineNumber = thisLineNumber + 1



        self.animateList = [SELECT, SELECT, SELECT, SELECT, SELECT, SELECT, \
                             NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, \
                             SELECT, SELECT, SELECT, SELECT, SELECT, SELECT, \
                             NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, \
                             SELECT, SELECT, SELECT, SELECT, SELECT, SELECT, \
                             NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, \
                             SELECT, SELECT, SELECT, SELECT, SELECT, SELECT, \
                             NORMAL\
                             ]
        self.nAnimationFrames = len(self.animateList)


    def mReset(self):
        for line in self.linesList:
            line.mReset()
        self.atAnimationFrameNumber = 0
        self.animating = False

    def mStartComputerAnimation(self, lineNumber):
        self.oComputerLineChosen = self.linesList[lineNumber]
        self.atAnimationFrameNumber = 0
        self.animating = True

    def mAnimate(self):
        if not self.animating:
            return
        if self.atAnimationFrameNumber < self.nAnimationFrames:
            style = self.animateList[self.atAnimationFrameNumber]
            self.oComputerLineChosen.mAnimate(style)
            self.atAnimationFrameNumber = self.atAnimationFrameNumber + 1
        else:
            self.animating = False




    def mCheckForRollOvers(self, mousePos):

        self.lineNumberOver = None
        for line in self.linesList:
            whichLineNumberOrNone = line.mCheckForRollover(mousePos)
            if whichLineNumberOrNone != None:
                self.lineNumberOver = whichLineNumberOrNone

        #print 'Over line number:', self.lineNumberOver
        return self.lineNumberOver

    def mCheckForMakingMove(self, mousePos):
        if self.lineNumberOver != None:
            oLine = self.linesList[self.lineNumberOver]
            borderSquaresList = oLine.mSelect(HUMAN)
            # TODO:  test for square completed
            #print 'Took line number', self.lineNumberOver
            #print 'This borders these squares', borderSquaresList
            return self.lineNumberOver, borderSquaresList

        return None, None

    def mComputerTakesLine(self, lineNumber):
        oLine = self.linesList[lineNumber]   # was:  self.lineNumberOver]
        borderSquaresList = oLine.mSelect(COMPUTER)
        return borderSquaresList


    def mAreAllLinesNowTaken(self, linesToCheckList):

        # each array of lines is a set of 4 lines surrounding a square
        for lineNumberToCheck in linesToCheckList:
            oLine = self.linesList[lineNumberToCheck]
            bTaken = oLine.mGetTaken()
            if not bTaken:  # if any side is not taken, we're done
                return False

        return True  # all must be taken

    def mSetAvailableForHuman(self, TrueOrFalse):
        for line in self.linesList:
            line.mSetAvailableForHuman(TrueOrFalse)


    def draw(self):
        for line in self.linesList:
            line.draw()

    def mGetLinesTaken(self):
        takenList = []  # list of True or False
        for line in self.linesList:
            lineHasBeenTaken = line.mGetTaken()
            takenList.append(lineHasBeenTaken)
        return takenList

    def mGetBorderSquares(self, thisLineNumber):
        borderSquaresList = LINES_TO_SQUARES_LIST[thisLineNumber]
        return borderSquaresList




class Game:
    def __init__(self, window):

        self.window = window
        self.backgroundImage = pygame.image.load('images/background.png')
        self.dotImage = pygame.image.load('images/dot.png')
        self.arrowHuman = pygame.image.load('images/arrowHuman.png')
        self.arrowComputer = pygame.image.load('images/arrowComputer.png')
        self.humanImage = pygame.image.load('images/squareHuman.png')
        self.computerImage = pygame.image.load('images/squareComputer.png')
        self.dotLocList = []

        # Layout Dots
        for rowNum in range(0, NROWS + 1):
            for colNum in range(0, NCOLS + 1):
                thisX = STARTING_X + (BOX_AND_LINE_SIZE * colNum)
                thisY = STARTING_Y + (BOX_AND_LINE_SIZE * rowNum)
                self.dotLocList.append((thisX, thisY))


        self.oSquareMgr = SquareMgr(self.window)
        self.oLineMgr = LineMgr(self.window)
        self.humanScoreInGames = 0
        self.computerScoreInGames = 0

        self.humanScoreDisplay = pygwidgets.DisplayText(self.window, (534, 185), fontSize=36)
        self.computerScoreDisplay = pygwidgets.DisplayText(self.window, (652, 185), fontSize=36)
        self.humanGameScoreDisplay = pygwidgets.DisplayText(self.window, (538, 326), '0', fontSize=24)
        self.computerGameScoreDisplay = pygwidgets.DisplayText(self.window, (658, 326), '0', fontSize=24)
        self.winnerDisplay = pygwidgets.DisplayText(self.window, (500, 224), 'Test', fontSize=36, width=200, justified='center')

        self.humanBlipSound = pygame.mixer.Sound('sounds/humanBlip.wav')
        self.computerBlipSound = pygame.mixer.Sound('sounds/computerBlip.wav')
        self.applauseSound = pygame.mixer.Sound('sounds/applause.wav')
        self.gameOverSound = pygame.mixer.Sound('sounds/gameOver.wav')
        self.mReset()

    def mReset(self):
        self.lineNumberOver = None
        self.oSquareMgr.mReset()
        self.oLineMgr.mReset()
        self.nLinesTaken = 0
        self.whoseTurn = HUMAN
        self.humanScore = 0
        self.computerScore = 0
        self.humanScoreDisplay.setValue('0')
        self.computerScoreDisplay.setValue('0')
        self.winnerDisplay.setValue('')
        self.animatingComputerMove = False



    def draw(self):
        self.window.blit(self.backgroundImage, (0, 0))
        for loc in self.dotLocList:
            self.window.blit(self.dotImage, loc)
        self.oSquareMgr.draw()
        self.oLineMgr.draw()
        self.humanScoreDisplay.draw()
        self.computerScoreDisplay.draw()
        self.humanGameScoreDisplay.draw()
        self.computerGameScoreDisplay.draw()

        if self.whoseTurn == HUMAN:
            self.window.blit(self.arrowHuman, (560, 106))
        else:
            self.window.blit(self.arrowComputer, (560, 106))

        self.window.blit(self.humanImage, (510, 96))
        self.window.blit(self.computerImage, (650, 96))
        self.winnerDisplay.draw()


    def mCheckForRollOverLines(self, mousePos):
        self.oLineMgr.mCheckForRollOvers(mousePos)

    def mCheckForMakingMove(self, mousePos):
        lineNumber, borderSquaresList = self.oLineMgr.mCheckForMakingMove(mousePos)
        if lineNumber != None:  # took some line
            self.humanBlipSound.play()
            pygame.time.set_timer(HUMAN_TURN_AGAIN, 0)  # and kill the timer
            self.mCheckForCompletedSquares(lineNumber, borderSquaresList)


    def mCheckForCompletedSquares(self, lineNumber, borderSquaresList):
        # clickSound.play()

        atLeastOneBoxCompleted = False
        for squareNumber in borderSquaresList:
            linesToCheckList = self.oSquareMgr.mGetLinesList(squareNumber)

            thisBoxCompleted = self.oLineMgr.mAreAllLinesNowTaken(linesToCheckList)
            if thisBoxCompleted:
                atLeastOneBoxCompleted = True
                self.oSquareMgr.mSetTaken(squareNumber, self.whoseTurn)
                if self.whoseTurn == HUMAN:
                    self.humanScore = self.humanScore + 1

                else:
                    self.computerScore = self.computerScore + 1


            self.humanScoreDisplay.setValue(str(self.humanScore))
            self.computerScoreDisplay.setValue(str(self.computerScore))

        if self.mDidSomeBodyWin():
            return

        # if no box was completed, switch whose turn it is
        if not atLeastOneBoxCompleted:
            if self.whoseTurn == HUMAN:
                msWait = random.randrange(750, 1500)
                pygame.time.set_timer(COMPUTER_TURN, msWait)
                self.whoseTurn = COMPUTER
                self.oLineMgr.mSetAvailableForHuman(False)

            else:
                self.whoseTurn = HUMAN
                print('Switching to human turn')
                self.oLineMgr.mSetAvailableForHuman(True)

        else:  # box was completed,
            ## if it's the computer's turn, set up the timer to choose again
            if self.whoseTurn == COMPUTER:
                msWait = random.randrange(1200, 2000)  # make it seem like computer is thinking
                pygame.time.set_timer(COMPUTER_TURN, msWait)

            # for the human, set a timer to remind them that it is their turn again
            else:
                pygame.time.set_timer(HUMAN_TURN_AGAIN, 7500)    # Wait for some time before reming user



    def mDidSomeBodyWin(self):

        if ((self.computerScore + self.humanScore) < NSQUARES):
            return False

        # We have a winner
        if self.humanScore > self.computerScore: #TODO:  add code below here for winners
            self.winnerDisplay.setValue("YOU WIN!!")
            self.humanScoreInGames = self.humanScoreInGames + 1
            self.humanGameScoreDisplay.setValue(str(self.humanScoreInGames))
            self.applauseSound.play()

        else:
            self.winnerDisplay.setValue("Computer wins!!")
            self.computerScoreInGames = self.computerScoreInGames + 1
            self.computerGameScoreDisplay.setValue(str(self.computerScoreInGames))
            self.gameOverSound.play()

        return True


    def mMakeComputerMove(self):
        takenList = self.oLineMgr.mGetLinesTaken()

        lineWeightsList = []
        for lineNumber in range(0, NLINES):
            if takenList[lineNumber]:
                lineWeightsList.append(-1000)
            else:
                lineWeightsList.append(1000)  # High weight for line not taken

        for squareNumber in range(0, NSQUARES):
            # for each square, get the set of 4 lines surrounding it
            lineNumbersForThisSquareList = self.oSquareMgr.mGetLinesList(squareNumber)
            nSidesTaken = 0
            for lineNumber in lineNumbersForThisSquareList:
                if takenList[lineNumber]:
                    nSidesTaken = nSidesTaken + 1
                else:
                    sideNotTaken = lineNumber

            # If 3 sides of a square are taken, bump the weight of the fourth side
            if nSidesTaken == 3:
                lineWeightsList[sideNotTaken] = lineWeightsList[sideNotTaken] + 200


        # Find the highest weight for all possible squares
        highestWeight = 0
        for weight in lineWeightsList:
            if weight > highestWeight:
                highestWeight = weight
        #print 'highest weight found was', highestWeight


        # Make a new list of all lines that have this wieght
        highestWeightLineIndexList = []
        for lineNumber in range(0, NLINES):
            if lineWeightsList[lineNumber] == highestWeight:
                highestWeightLineIndexList.append(lineNumber)

        nChoices = len(highestWeightLineIndexList)

        if nChoices == 1:
            indexChosen = 0
        else:
            indexChosen = random.randrange(0, nChoices)

        lineNumberChoice = highestWeightLineIndexList[indexChosen]

        borderSquaresList = self.oLineMgr.mComputerTakesLine(lineNumberChoice)
        self.mCheckForCompletedSquares(lineNumberChoice, borderSquaresList)

        print('Computer chooses line number', lineNumberChoice)
        self.computerBlipSound.play()
        self.oLineMgr.mStartComputerAnimation(lineNumberChoice)

    def mPing(self):
        self.oLineMgr.mAnimate()




# Main code
oGame = Game(window)
startButton = pygwidgets.TextButton(window, (550, 255), 'New Game', width=100, height=35)
yourTurnAgainSound = buzz = pygame.mixer.Sound('sounds/yourTurnAgain.wav')


while True:
    # Handle events
    for event in pygame.event.get():
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            mousePos = event.pos
            oGame.mCheckForMakingMove(mousePos)

        if  startButton.handleEvent(event):
            oGame.mReset()

        if event.type == COMPUTER_TURN:
            pygame.time.set_timer(COMPUTER_TURN, 0)   # Kill the timer
            oGame.mMakeComputerMove()

        if event.type == HUMAN_TURN_AGAIN:  # time to tell the player that it is their turn

            yourTurnAgainSound.play()
            pygame.time.set_timer(HUMAN_TURN_AGAIN, 0)  # and kill the timer

    oGame.mPing()   # ping the game for anything it may need to do.

    mousePos = pygame.mouse.get_pos()
    oGame.mCheckForRollOverLines(mousePos)

    # Draw everything
    window.fill(GRAY)

    # Draw the game
    oGame.draw()

    # Draw  buttons
    startButton.draw()

    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)
