# SCENE_PLAY
#
# This is where the game play happens
#
# This is implemented as a Model-View-Controller style
#
# - The Controller is a Scene (as defined by pyghelpers).
#    It creates a Model and a View and communicates with both
# - The Model contains and manipulates all the data for the game
# - The View draws everything in the window

import random
import copy
import sys
from Constants import *
import pygame
import pygwidgets
import pyghelpers

BOARD_NROWS = 6 # number of rows
BOARD_NCOLS = 7  # number of columns
DIFFICULTY = 2

SPACE_SIZE = 50 # size of the tokens and individual board spaces in pixels
HALF_SPACE_SIZE = int(SPACE_SIZE / 2) # size of the tokens and individual board spaces in pixels
X_MARGIN = int((WINDOW_WIDTH - (BOARD_NCOLS * SPACE_SIZE)) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_NROWS * SPACE_SIZE)) / 2)

MOVING_TOKEN_Y = 30
RED_TOKEN_X = 50
BLACK_TOKEN_X = 545
RED_MOVING_TOKEN_LOC = (RED_TOKEN_X, MOVING_TOKEN_Y)
BLACK_MOVING_TOKEN_LOC = (BLACK_TOKEN_X, MOVING_TOKEN_Y)
RED_MOVING_TOKEN_RECT = pygame.Rect(RED_TOKEN_X, MOVING_TOKEN_Y, SPACE_SIZE, SPACE_SIZE)
BLACK_MOVING_TOKEN_RECT = pygame.Rect(BLACK_TOKEN_X, MOVING_TOKEN_Y, SPACE_SIZE, SPACE_SIZE)

STARTING_DROP_SPEED = 2
INCREMENTAL_DROP_SPEED = 2

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = 'Red'
BLACK = 'Black'
EMPTY = 'none'


class View():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        self.basicFont = pygame.font.SysFont(None, 36)
        self.messageTextField = pygwidgets.DisplayText(self.window, (0, 2), "",  fontSize=36,
                                                     width=WINDOW_WIDTH,  justified='center', textColor=WHITE)

        tokensDict = {RED: 'images/4row_red.png', BLACK: 'images/4row_black.png'}
        # This is a token that is used in dragging and in animating down
        self.movingToken = pygwidgets.ImageCollection(self.window, (0, 0), tokensDict, '')
        # Build the visual representation of the board
        self.fullBoardImage = pygwidgets.Image(self.window, (X_MARGIN, Y_MARGIN), 'images/fullBoard.png')
        self.boardTokens  = []
        for row in range(BOARD_NROWS):
            rowOfTokens = []
            for col in range(BOARD_NCOLS):
                loc = ((X_MARGIN + (col * SPACE_SIZE) + HALF_SPACE_SIZE, Y_MARGIN + (row * SPACE_SIZE) + HALF_SPACE_SIZE))
                oToken = pygwidgets.ImageCollection(self.window, loc, tokensDict, '')  # quote quote defaults to no image
                rowOfTokens.append(oToken)
            self.boardTokens.append(rowOfTokens)

    def startGame(self):
        for row in range(BOARD_NROWS):
            for col in range(BOARD_NCOLS):
                oToken = self.boardTokens[row][col]
                oToken.replace('')  # clear the board

    def setTurn(self, turn):
        self.turn = turn
        if self.turn == RED:
            self.setMessageText("Red's turn")
            self.movingToken.replace(RED)
            self.movingToken.setLoc(RED_MOVING_TOKEN_LOC)
        else:
            self.setMessageText("Black's turn")
            self.movingToken.replace(BLACK)
            self.movingToken.setLoc(BLACK_MOVING_TOKEN_LOC)

    def setMessageText(self, text):
        self.messageTextField.setText(text)

    def resetDragging(self):
        if self.turn == RED:
            self.movingToken.setLoc(RED_MOVING_TOKEN_LOC)
        else:
            self.movingToken.setLoc(BLACK_MOVING_TOKEN_LOC)

    def mouseDownOnMovingToken(self, clickPos):
        if self.turn == RED:
            movingTokenRect = RED_MOVING_TOKEN_RECT
        else:
            movingTokenRect = BLACK_MOVING_TOKEN_RECT
        return movingTokenRect.collidepoint(clickPos)

    def startDragging(self):
        if self.turn == RED:
            self.movingToken.replace(RED)
            self.movingTokenX = RED_TOKEN_X
        else:
            self.movingToken.replace(BLACK)
            self.movingTokenX = BLACK_TOKEN_X
        self.movingTokenY = MOVING_TOKEN_Y
        self.movingToken.setLoc((self.movingTokenX, self.movingTokenY))

    def dragging(self, x, y):
        self.movingTokenX = x
        self.movingTokenY = y
        self.movingToken.setLoc((self.movingTokenX - HALF_SPACE_SIZE, self.movingTokenY))

    def endDraggingGetColumn(self):
        if self.movingTokenX > X_MARGIN and self.movingTokenX < WINDOW_WIDTH - X_MARGIN:
            column = int((self.movingTokenX - X_MARGIN) / SPACE_SIZE)
        else: # not in valid range
            column = -1
        return column

    def startAnimatingDown(self, column):
        # Move was good, set up for animating the drop
        self.movingTokenX = X_MARGIN + (column * SPACE_SIZE)
        self.movingTokenY = Y_MARGIN - SPACE_SIZE
        self.dropSpeed = STARTING_DROP_SPEED

    def animatingDown(self, targetRow):
        self.movingTokenY = int(self.movingTokenY + self.dropSpeed)
        self.dropSpeed = self.dropSpeed + INCREMENTAL_DROP_SPEED
        if ((self.movingTokenY - Y_MARGIN) / SPACE_SIZE) >= targetRow:
            done = True
            self.movingToken.replace('')
        else:
            done = False

        self.movingToken.setLoc((self.movingTokenX, self.movingTokenY))
        return done

    def startComputerAnimatingLeft(self, targetColumn):
        self.movingToken.replace(BLACK)
        self.movingTokenX = BLACK_MOVING_TOKEN_RECT[0]
        self.movingTokenY = Y_MARGIN - SPACE_SIZE
        self.movingTokenXTarget = X_MARGIN + (targetColumn * SPACE_SIZE) + HALF_SPACE_SIZE

    def computerAnimatingLeft(self, targetColumn):
        self.movingTokenX -= 7  # move left 7 pixels, ... seems like a good speed
        if self.movingTokenX > self.movingTokenXTarget:
            self.movingToken.setLoc((self.movingTokenX - HALF_SPACE_SIZE, MOVING_TOKEN_Y))
            done = False
        else:
            self.movingTokenX = X_MARGIN + (targetColumn * SPACE_SIZE)
            self.movingTokenY = Y_MARGIN - SPACE_SIZE
            self.dropSpeed = STARTING_DROP_SPEED
            self.movingToken.setLoc((self.movingTokenX, self.movingTokenY))
            done = True
        return done

    def setPieceInGameBoard(self, row, col, color):
        oToken = self.boardTokens[row][col]
        oToken.replace(color)

    def draw(self, board):
        # Draw all tokens in the board on the screen
        for row in range(BOARD_NROWS):
            for col in range(BOARD_NCOLS):
                oToken = self.boardTokens[row][col]
                oToken.draw()

        self.movingToken.draw()
        self.fullBoardImage.draw()
        self.messageTextField.draw()

    def drawWinningLine(self, winningRowColStart, winningRowColEnd):
        fromCoords = [X_MARGIN + (winningRowColStart[1] * SPACE_SIZE) + HALF_SPACE_SIZE,
                      Y_MARGIN + (winningRowColStart[0] * SPACE_SIZE) + HALF_SPACE_SIZE]
        toCoords = [X_MARGIN + (winningRowColEnd[1] * SPACE_SIZE) + HALF_SPACE_SIZE,
                    Y_MARGIN + (winningRowColEnd[0] * SPACE_SIZE) + HALF_SPACE_SIZE]
        pygame.draw.line(self.window, GREEN, fromCoords, toCoords, 10)


class Model():
    def __init__(self):
        self.gameBoard = []

    def startGame(self):
        # Set up a 'gameBoard' nested list structure with every cell set to EMPTY.
        self.gameBoard = []
        for row in range(BOARD_NROWS):
            self.gameBoard.append([EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY])

    def setTurn(self, whoseTurn):
        self.turn = whoseTurn

    def getGameBoard(self):
        return self.gameBoard

    def setPieceInGameBoard(self, row, col, color):
        self.gameBoard[row][col] = color

    def getLowestEmptyRow(self, board, column):
        # Return the row number of the lowest empty row in the given column.  Or -1 for none
        for row in range(BOARD_NROWS - 1, -1, -1):
            # if this is the lowest empty, return it
            if board[row][column] == EMPTY:
                return row
        return -1  # All filled

    def isValidMove(self, board, column):
        # Returns True if there is an empty space in the given column.
        if (column < 0) or (column > (BOARD_NCOLS - 1)) or board[0][column] != EMPTY:
            return False
        else:
            return True

    def isBoardFull(self, board):
        # Returns True if there are no empty spaces anywhere on the board.
        for row in range(BOARD_NROWS):
            for col in range(BOARD_NCOLS):
                if board[row][col] == EMPTY:
                    return False
        return True

    def isWinner(self, board, tile):
        # check horizontal spaces
        for row in range(BOARD_NROWS):
            for col in range(BOARD_NCOLS - 3):
                if board[row][col] == tile and board[row][col + 1] == tile and  \
                        board[row][col + 2] == tile and board[row][col + 3] == tile:
                    self.winningRowColStart = [row, col]
                    self.winningRowColEnd = [row, col + 3]
                    return True

        # check vertical spaces
        for row in range(BOARD_NROWS - 3):
            for col in range(BOARD_NCOLS):
                if board[row][col] == tile and board[row + 1][col] == tile and \
                        board[row + 2][col] == tile and board[row + 3][col] == tile:
                    self.winningRowColStart = [row, col]
                    self.winningRowColEnd = [row + 3, col]
                    return True

        # for diagonal down right
        for row in range(BOARD_NROWS - 3):
            for col in range(BOARD_NCOLS - 3):
                if board[row][col] == tile and board[row + 1][col + 1] == tile and \
                        board[row + 2][col + 2] == tile and board[row + 3][col + 3] == tile:
                    self.winningRowColStart = [row, col]
                    self.winningRowColEnd = [row + 3, col + 3]
                    return True

        # for diagonal up right
        for row in range(3, BOARD_NROWS):
            for col in range(0, BOARD_NCOLS - 3):
                if board[row][col] == tile and board[row - 1][col + 1] == tile and \
                        board[row - 2][col + 2] == tile and board[row - 3][col + 3] == tile:
                    self.winningRowColStart = [row, col]
                    self.winningRowColEnd = [row - 3, col + 3]
                    return True

        return False  # No winner this time

    def getWinningRowColStartEnd(self):
        return self.winningRowColStart, self.winningRowColEnd

    # For development debugging
    def printBoard(self, message=''):
        print()
        if message != '':
            print(message)
        for row in range(BOARD_NROWS):
            print(self.gameBoard[row])

    #### FOR AUTOMATED COMPUTER MOVES ###############
    def getComputerMove(self):
        potentialMoves = self.getPotentialMoves(self.gameBoard, BLACK, DIFFICULTY)

        # Get the best fitness from the potential moves
        bestMoveFitness = -1000
        for col, thisMove in enumerate(potentialMoves):
            if self.isValidMove(self.gameBoard, col) and (thisMove > bestMoveFitness):
                bestMoveFitness = thisMove

        # find all potential moves that match this best fitness
        bestMoves = []
        for col, thisMove in enumerate(potentialMoves):
            if self.isValidMove(self.gameBoard, col) and thisMove == bestMoveFitness:
                bestMoves.append(col)

        # print '\nIn getComputerMove, potentialMoves, bestMoves, bestMoveFitness, and move chosen: '
        # print str(potentialMoves)
        # print str(bestMoves)
        # print str(bestMoveFitness)

        moveChosen = random.choice(bestMoves)
        return moveChosen

    def getPotentialMoves(self, board, tile, lookAhead):
        if lookAhead == 0 or self.isBoardFull(board):
            return [0] * BOARD_NCOLS

        if tile == RED:
            enemyTile = BLACK
        else:
            enemyTile = RED

        # Figure out the best move to make.
        potentialMoves = [0] * BOARD_NCOLS
        for firstMove in range(BOARD_NCOLS):
            dupeBoard = copy.deepcopy(board)
            if not self.isValidMove(dupeBoard, firstMove):
                continue
            self.makeMove(dupeBoard, tile, firstMove)
            if self.isWinner(dupeBoard, tile):
                # A winning move automatically gets a perfect fitness
                potentialMoves[firstMove] = 1
                break  # don't bother calculating other moves
            else:
                # Do other player's counter moves and determine best one
                if self.isBoardFull(dupeBoard):
                    potentialMoves[firstMove] = 0
                else:
                    for counterMove in range(BOARD_NCOLS):
                        dupeBoard2 = copy.deepcopy(dupeBoard)
                        if not self.isValidMove(dupeBoard2, counterMove):
                            continue
                        self.makeMove(dupeBoard2, enemyTile, counterMove)
                        if self.isWinner(dupeBoard2, enemyTile):
                            # A losing move automatically gets the worst fitness
                            potentialMoves[firstMove] = -1
                            break
                        else:
                            # Do the recursive call to getPotentialMoves()
                            results = self.getPotentialMoves(dupeBoard2, tile, lookAhead - 1)
                            potentialMoves[firstMove] += (sum(results) / BOARD_NCOLS) / BOARD_NCOLS

        return potentialMoves

    def makeMove(self, board, player, column):
        row = self.getLowestEmptyRow(board, column)
        if row != -1:
            board[row][column] = player

# States:
STATE_WAITING = 'waiting'
STATE_ANIMATING_DOWN = 'animating'
STATE_DRAGGING = 'dragging'
STATE_GAME_OVER = 'gameOver'
STATE_GAME_OVER_TIE = 'gameOverTie'
STATE_EVALUATE = 'evaluate'
STATE_COMPUTER_ANIMATING_LEFT = 'computer_animating_left'
STATE_START_GAME = 'start_game'

class ScenePlay(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.backButton = pygwidgets.CustomButton(self.window, (5, 407),
                                                up='images/backUp.png',
                                                over='images/backOver.png',
                                                down='images/backDown.png')
        self.quitButton = pygwidgets.CustomButton(window, (242, 407),
                                                  up='images/quitUp.png',
                                                  over='images/quitOver.png',
                                                  down='images/quitDown.png')
        self.restartButton = pygwidgets.CustomButton(self.window, (475, 407),
                                                up='images/restartUp.png',
                                                over='images/restartOver.png',
                                                down='images/restartDown.png')
        self.soundDrop = pygwidgets.SoundEffect('sounds/soundDrop.wav')
        self.soundHitBottom = pygwidgets.SoundEffect('sounds/hitBottom.wav')
        self.soundBuzz = pygwidgets.SoundEffect('sounds/buzz.wav')
        self.soundApplause = pygwidgets.SoundEffect('sounds/applause.wav')

        self.oView = View(WINDOW_WIDTH, WINDOW_HEIGHT)  # create the view
        self.oModel = Model()  # create the model

        self.state = STATE_START_GAME

    def enter(self, data):  # Arrived from start screen
        self.gameMode = data  # HUMAN_VS_HUMAN   or HUMAN_VS_COMPUTER
        self.startGame()    # sets self.turn

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if self.quitButton.handleEvent(event):
                pygame.quit()
                sys.exit()

            elif self.backButton.handleEvent(event):
                self.goToScene(SCENE_CHOOSE)

            elif self.restartButton.handleEvent(event):
                self.startGame()   # sets self.turn

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == STATE_WAITING:
                    if self.oView.mouseDownOnMovingToken(event.pos):
                        # Start dragging token.
                        self.oView.startDragging()
                        self.state = STATE_DRAGGING

            elif event.type == pygame.MOUSEMOTION:
                if self.state == STATE_DRAGGING:
                    # Update the position of the token being dragged
                    self.oView.dragging(event.pos[0], MOVING_TOKEN_Y)

            elif event.type == pygame.MOUSEBUTTONUP:
                # User let go of the token being dragged
                if self.state == STATE_DRAGGING:

                    col = self.oView.endDraggingGetColumn()
                    if col == -1:  # Dropped in invalid location
                        self.state = STATE_WAITING
                        self.soundBuzz.play()
                        self.oView.resetDragging()
                        return

                    row = self.oModel.getLowestEmptyRow(self.gameBoard, col)
                    if not (self.oModel.isValidMove(self.gameBoard, col)) or (row == -1): # Col is full
                        self.state = STATE_WAITING
                        self.soundBuzz.play()
                        self.oView.resetDragging()
                        return

                    # Legal move
                    self.soundDrop.play()
                    self.oView.startAnimatingDown(col)
                    self.row = row
                    self.col = col
                    self.state = STATE_ANIMATING_DOWN

    def update(self):  # Called in every frame
        self.gameBoard = self.oModel.getGameBoard()

        # GAME LOGIC HERE - based on state
        if self.state == STATE_WAITING:
            if (self.gameMode == HUMAN_VS_COMPUTER) and (self.turn == BLACK):  # choose computer move
                self.computerMoveColumn = self.oModel.getComputerMove()
                self.oView.startComputerAnimatingLeft(self.computerMoveColumn)
                self.state = STATE_COMPUTER_ANIMATING_LEFT

        elif self.state == STATE_COMPUTER_ANIMATING_LEFT:
            done = self.oView.computerAnimatingLeft(self.computerMoveColumn)
            if done:
                self.state = STATE_ANIMATING_DOWN
                self.row = self.oModel.getLowestEmptyRow(self.gameBoard, self.computerMoveColumn)
                self.col = self.computerMoveColumn
                self.soundDrop.play()

        elif self.state == STATE_ANIMATING_DOWN:
            done = self.oView.animatingDown(self.row)
            if done:
                self.state = STATE_EVALUATE
                self.soundHitBottom.play()
                self.oModel.setPieceInGameBoard(self.row, self.col, self.turn)  # Add in the new piece
                self.oView.setPieceInGameBoard(self.row, self.col, self.turn)

        elif self.state == STATE_EVALUATE:
            self.state = STATE_WAITING  # Can override below if game is over

            if self.turn == RED:
                if self.oModel.isWinner(self.gameBoard, RED):
                    self.oView.setMessageText('Red WINS!!')
                    self.state = STATE_GAME_OVER
                    self.soundApplause.play()
                else:
                    self.turn = BLACK
                    self.oModel.setTurn(BLACK)
                    self.oView.setTurn(BLACK)
                    self.oView.setMessageText("Black's turn")

            else:  # BLACK
                if self.oModel.isWinner(self.gameBoard, BLACK):
                    self.oView.setMessageText('Black WINS!!')
                    self.state = STATE_GAME_OVER
                    self.soundApplause.play()
                else:
                    self.turn = RED
                    self.oModel.setTurn(RED)
                    self.oView.setTurn(RED)
                    self.oView.setMessageText("Red's turn")

            if self.oModel.isBoardFull(self.gameBoard):
                # A completely filled board means it's a tie.
                self.oView.setMessageText("It's a tie")
                self.state = STATE_GAME_OVER_TIE

    def startGame(self):
        # Randomly choose who goes first.
        if random.randrange(0, 2) == 0:
            self.turn = RED
        else:
            self.turn = BLACK
        self.oModel.startGame()
        self.oView.startGame()
        self.oModel.setTurn(self.turn)
        self.oView.setTurn(self.turn)
        self.state = STATE_WAITING

    def draw(self):
        self.window.fill(BACKGROUND_COLOR)
        currentGameBoard = self.oModel.getGameBoard()
        self.oView.draw(currentGameBoard)
        if self.state == STATE_GAME_OVER:
            start, end = self.oModel.getWinningRowColStartEnd()
            self.oView.drawWinningLine(start, end)
        self.backButton.draw()
        self.quitButton.draw()
        self.restartButton.draw()
