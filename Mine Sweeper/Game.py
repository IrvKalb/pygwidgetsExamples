#  Game class

from pygame.locals import *
import pyghelpers
import random

from Cell import *

class Game():
    neighborOffsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    def __init__(self, window):
        self.window = window

        # Instance variables:
        self.nMinesLeft = 0
        self.clickedInCell = False
        self.gameOver = False
        self.timerRunning = False
        self.firstClick = True
        self.gameOver = False
        # Toggles with esc key.  When on, plays sound on flagging mines
        self.helperMode = False

        self.oMinesLabel = pygwidgets.DisplayText(self.window, (20, 570),
                                                  'Mines left:', fontSize=36)
        self.oMinesLeftDisplay = pygwidgets.DisplayText(self.window, (150, 570),
                                                    str(N_MINES), fontSize=36, justified='left')

        self.oRestartButton = pygwidgets.TextButton(self.window, (235, 560), 'Restart')
        self.oTimer = pyghelpers.CountUpTimer()
        self.oTimeLabel = pygwidgets.DisplayText(self.window, (380, 570),
                                                    'Time: ', fontSize = 36)
        self.oTimeDisplay = pygwidgets.DisplayText(self.window, (452, 570),
                                                    '0', fontSize = 36, justified='left')
        self.applauseSound = pygame.mixer.Sound('sounds/applause.wav')

        # Build the board as a two dimensional list of Cell objects
        self.board = []
        for rowIndex in range(0, N_ROWS):
            oneRowList = []
            for colIndex in range(0, N_COLS):
                # Instantiate a cell object telling it its row and column indeces
                # aso it can calculate where to draw, and also find its neighbors
                oCell = Cell(self.window, rowIndex, colIndex)
                oneRowList.append(oCell)
            self.board.append(oneRowList)
        self.reset()

    def reset(self):
        for rowIndex in range(0, N_ROWS):
            for colIndex in range(0, N_COLS):
                self.board[rowIndex][colIndex].reset()
        self.gameOver = False
        self.timerRunning = False
        self.nMinesLeft = N_MINES
        self.oTimeDisplay.setValue(0)
        self.firstClick = True
        self.gameOver = False


    def placeMines(self, rowClicked, colClicked):
        nMinesPlaced = 0
        while True:
            randomRow = random.randrange(0, N_ROWS)
            randomCol = random.randrange(0, N_COLS)
            if (randomRow == rowClicked) and (randomCol == colClicked):
                continue  # cannot place a mine in the first clicked square
            oCell = self.board[randomRow][randomCol]
            value = oCell.getValue()
            if value is None:
                oCell.setValue(MINE)
                nMinesPlaced = nMinesPlaced + 1
                if nMinesPlaced == N_MINES:
                    break

    def handleEvent(self, event):
        if self.oRestartButton.handleEvent(event):
            self.reset()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.helperMode = not self.helperMode  #  Cheat code!

            if event.key == pygame.K_0:
                for row in range(N_ROWS):
                    for col in range(N_COLS):
                        oCell = self.board[row][col]
                        print(oCell.getValue(), end='')
                    print('\n')

        if event.type == MOUSEBUTTONDOWN:
            if self.gameOver:
                return
            for rowIndex in range(0, N_ROWS):
                for colIndex in range(0, N_COLS):
                    oCellClicked = self.board[rowIndex][colIndex]
                    self.clickedInCell = oCellClicked.handleEvent(event)
                    if not self.clickedInCell:
                        continue  # nothing to do
                    # Got a click in a cell
                    if self.firstClick:
                        # Only place mines on the first click
                        self.placeMines(rowIndex, colIndex)
                        self.placeNumbers()
                        self.oTimer.start()
                        self.timerRunning = True
                        self.firstClick = False
                    result = oCellClicked.handleClick(event, self.helperMode)
                    if result == GAME_OVER:
                        self.gameOver = True
                        for row in range(0, N_ROWS):
                            for col in range(0, N_COLS):
                                oCell = self.board[row][col]
                                oCell.showIfMine(False)  # show black mines
                        oCellClicked.showIfMine(True)  # show red mine that ended the game
                        self.oTimer.stop()
                        return
                    elif result == FLAGGED:
                        self.nMinesLeft = self.nMinesLeft - 1
                    elif result == UNFLAGGED:
                        self.nMinesLeft = self.nMinesLeft + 1
                    elif result == REVEALED_CELL:
                        self.revealNeighbors(oCellClicked)
                    elif result == ALREADY_REVEALED:
                        return  # nothing to do
                    else:
                        raise ValueError('Unexpected result from click: ' + str(result))

            self.checkForWin()


    def checkForWin(self):
        if self.nMinesLeft != 0:
            return  # Not cleared all mines
        for rowIndex in range(0, N_ROWS):
            for colIndex in range(0, N_COLS):
                oCell = self.board[rowIndex][colIndex]
                if oCell.isHidden():  # if any cell is hidden, then no win
                    return False
       # Game is over - player wins!!
        self.applauseSound.play()
        self.gameOver = True
        self.oTimer.stop()
        return True


    def revealNeighbors(self, oCenterCell):
        neighborsList = oCenterCell.getNeighbors()
        #print('neighborsList', neighborsList)
        revealedNeighborsList = []
        for neighborTuple in neighborsList:
            theRow = neighborTuple[0]
            theCol = neighborTuple[1]
            oNeighborCell = self.board[theRow][theCol]
            if oNeighborCell.isRevealable():
                oNeighborCell.reveal()
                if oNeighborCell.isEmpty():
                    revealedNeighborsList.append(oNeighborCell)
        if revealedNeighborsList == []:
            return  # no more neighbors to deal with

        # Use recursion to find neighbors of neighbors
        for oNewCenterCell in  revealedNeighborsList:
            self.revealNeighbors(oNewCenterCell)

                   
    def update(self):
        self.oMinesLeftDisplay.setValue(self.nMinesLeft)
        if self.timerRunning:
            formattedTime = self.oTimer.getTimeInHHMMSS()
            self.oTimeDisplay.setValue(formattedTime)

    def placeNumbers(self):
        for row in range(0, N_ROWS):
            for col in range(0, N_COLS):
                oCell = self.board[row][col]
                if oCell.getValue() != MINE:
                    count = self.countNeighborMines(row, col)
                    oCell.setValue(count)

    def countNeighborMines(self, theRow, theCol):
        mineCount = 0
        oCell = self.board[theRow][theCol]
        neighborsList = oCell.getNeighbors()
        for neighborsTuple in neighborsList:
            oNeighborCell = self.board[neighborsTuple[0]][neighborsTuple[1]]
            contents = oNeighborCell.getValue()
            if contents == MINE:
                mineCount = mineCount + 1

        return mineCount

    def draw(self):
        for rowIndex in range(0, N_ROWS):
            for colIndex in range(0, N_COLS):
                oCell = self.board[rowIndex][colIndex]
                oCell.draw()

        self.oMinesLabel.draw()
        self.oMinesLeftDisplay.draw()
        self.oRestartButton.draw()
        self.oTimeLabel.draw()
        self.oTimeDisplay.draw()