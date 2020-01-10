# Rewritten into Model View Controller OOP approach 7/15 by Irv Kalb
# IrvKalb1@gmail.com
#_____________________________

# HEAVILY MODIFIED (maybe 90% re-write) BY IRV KALB    08/14
# IrvKalb1@gmail.com
#
# New version includes: instruction screen, choice of who goes first (with enhanced button code),
# drag and drop interface, new board representation data structure, winning line designation,
# choice to "play again", bug fixes in artifical intellegence algorithm, constants, implementation of
# state machine, addition of sounds, text message at bottom of screen, human vs human mode.
#_____________________________


#ORIGINAL INSPIRATION:
# Four-In-A-Row (a Connect Four clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license


import random
import copy
import sys
import pygame
import pygwidgets


HUMAN_VS_HUMAN = 'human vs human'
HUMAN_VS_COMPUTER = 'human vs computer'

DIFFICULTY = 2

BOARD_NROWS = 6 # number of rows
BOARD_NCOLS = 7  # number of columns

SPACE_SIZE = 50 # size of the tokens and individual board spaces in pixels
HALF_SPACE_SIZE = int(SPACE_SIZE / 2) # size of the tokens and individual board spaces in pixels

FPS = 30 # frames per second to update the screen
WINDOW_WIDTH = 640 # width of the program's window, in pixels
WINDOW_HEIGHT = 480 # height in pixels

    
X_MARGIN = int((WINDOW_WIDTH - (BOARD_NCOLS * SPACE_SIZE)) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_NROWS * SPACE_SIZE)) / 2)
    
BRIGHT_BLUE = (0, 50, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BGCOLOR = BRIGHT_BLUE
TEXTCOLOR = WHITE

RED = 'Red'
BLACK = 'Black'
EMPTY = 'none'

PILE_Y = 30
RED_PILE_RECT = pygame.Rect(HALF_SPACE_SIZE, PILE_Y, SPACE_SIZE, SPACE_SIZE)
BLACK_PILE_RECT = pygame.Rect(WINDOW_WIDTH - int(3 * HALF_SPACE_SIZE), PILE_Y, SPACE_SIZE, SPACE_SIZE)

STARTING_DROP_SPEED = 3
INCREMENTAL_DROP_SPEED = 1



RED_TOKEN_IMG = pygame.image.load('images/4row_red.png')
RED_TOKEN_IMG = pygame.transform.smoothscale(RED_TOKEN_IMG, (SPACE_SIZE, SPACE_SIZE))
RED_TOKEN_DISABLED_IMG = pygame.image.load('images/4row_redDisabled.png')
RED_TOKEN_DISABLED_IMG = pygame.transform.smoothscale(RED_TOKEN_DISABLED_IMG, (SPACE_SIZE, SPACE_SIZE))
BLACK_TOKEN_IMG = pygame.image.load('images/4row_black.png')
BLACK_TOKEN_IMG = pygame.transform.smoothscale(BLACK_TOKEN_IMG, (SPACE_SIZE, SPACE_SIZE))
BLACK_TOKEN_DISABLED_IMG = pygame.image.load('images/4row_blackDisabled.png')
BLACK_TOKEN_DISABLED_IMG = pygame.transform.smoothscale(BLACK_TOKEN_DISABLED_IMG, (SPACE_SIZE, SPACE_SIZE))
BOARD_IMG = pygame.image.load('images/4row_board.png')
BOARD_IMG = pygame.transform.smoothscale(BOARD_IMG, (SPACE_SIZE, SPACE_SIZE))
HUMAN_UP_IMG = pygame.image.load('images/humanUp.png')
HUMAN_DOWN_IMG = pygame.image.load('images/humanDown.png')
COMPUTER_UP_IMG = pygame.image.load('images/computerUp.png')
COMPUTER_DOWN_IMG = pygame.image.load('images/computerDown.png')
BOX_WITH_RULES_IMG = pygame.image.load('images/boxWithRules.png')




# States:
STATE_WAITING = 'waiting'
STATE_ANIMATING_DOWN = 'animating'
STATE_DRAGGING = 'dragging'
STATE_GAME_OVER = 'gameOver'
STATE_GAME_OVER_TIE = 'gameOverTie'
STATE_EVALUATE = 'evaluate'
STATE_COMPUTER_ANIMATING_LEFT = 'computer_animating_left'
STATE_START_GAME = 'start_game'



class View():
# Read in images and scale down
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        self.basicFont = pygame.font.SysFont(None, 36)
        self.messageTextField = pygwidgets.DisplayText(self.window, (20, 405), "", textColor=WHITE)
        self.restartButton = pygwidgets.CustomButton(self.window, (514, 440), \
                                        up='images/RestartButtonUp.png', down='images/RestartButtonDown.png', over='images/RestartButtonOver.png', disabled= 'images/RestartButtonDisabled.png')
        self.humanHumanButton = pygwidgets.CustomButton(self.window, (162, 192), \
                                        up='images/humanUp.png', down='images/humanDown.png', over='images/humanUp.png')
        self.humanComputerButton = pygwidgets.CustomButton(self.window, (341, 192), \
                                        up='images/computerUp.png', down='images/computerDown.png', over='images/computerUp.png')

    
    def mClear(self):
        self.window.fill(BGCOLOR)

    def mStartGame(self, turn):

        if turn == RED:
            self.mSetMessageText("Red's turn")
        else:
            self.mSetMessageText("Black's turn")


    def mDrawPiles(self, whoseTurn):  # could be RED, BLACK, or None
        if whoseTurn == RED:
            self.window.blit(RED_TOKEN_IMG, RED_PILE_RECT) #red on the left
        else:
            self.window.blit(RED_TOKEN_DISABLED_IMG, RED_PILE_RECT)
        if whoseTurn == BLACK:
            self.window.blit(BLACK_TOKEN_IMG, BLACK_PILE_RECT) #black on the right
        else:
            self.window.blit(BLACK_TOKEN_DISABLED_IMG, BLACK_PILE_RECT)


    def mDrawBoard(self, board, turn):
    # draw tokens

        spaceRect = pygame.Rect(0, 0, SPACE_SIZE, SPACE_SIZE)
        for row in range(BOARD_NROWS):
            for col in range(BOARD_NCOLS):
                spaceRect.topleft = (X_MARGIN + (col * SPACE_SIZE), Y_MARGIN + (row * SPACE_SIZE))
                if board[row][col] != EMPTY:
                    if board[row][col] == RED:
                        self.window.blit(RED_TOKEN_IMG, spaceRect)
                    else:
                        self.window.blit(BLACK_TOKEN_IMG, spaceRect)

                
                self.window.blit(BOARD_IMG, spaceRect)


        # draw board over the tokens
        spaceRect = pygame.Rect(0, 0, SPACE_SIZE, SPACE_SIZE)
        for row in range(BOARD_NROWS):
            for col in range(BOARD_NCOLS):
                spaceRect.topleft = (X_MARGIN + (col * SPACE_SIZE), Y_MARGIN + (row * SPACE_SIZE))
                self.window.blit(BOARD_IMG, spaceRect)
                
        # Don't draw the red and black - already drawn earlier
        
        self.messageTextField.draw()
        self.restartButton.draw()

    def mSetMessageText(self, text):
        self.messageTextField.setText(text)


    def mDrawWinningLine(self, winningRowColStart, winningRowColEnd):        
        fromCoords = [X_MARGIN + (winningRowColStart[1] * SPACE_SIZE) + HALF_SPACE_SIZE, \
                              Y_MARGIN + (winningRowColStart[0] * SPACE_SIZE) + HALF_SPACE_SIZE]
        toCoords = [X_MARGIN + (winningRowColEnd[1] * SPACE_SIZE) + HALF_SPACE_SIZE, \
                           Y_MARGIN + (winningRowColEnd[0] * SPACE_SIZE) + HALF_SPACE_SIZE]
        pygame.draw.line(self.window, GREEN, fromCoords, toCoords, 10)

    def mButtonClicked(self, button, event):
        if button == 'restart':
            if self.restartButton.handleEvent(event):
                return True
            else:
                return False

        elif button == 'humanHuman':
            if self.humanHumanButton.handleEvent(event):
                return True
            else:
                return False

        elif button == 'humanComputer':
            if self.humanComputerButton.handleEvent(event):
                return True
            else:
                return False
            

    def mShowRules(self):
        self.window.blit(BOX_WITH_RULES_IMG, (120, 40, 400, 400))
        self.humanHumanButton.draw()
        self.humanComputerButton.draw()

    def mStartDragging(self, x, y):
        self.tokenx = x
        self.tokeny = y

    def mDragging(self, turn, x, y):
        self.tokenx = x
        self.tokeny = y
        if turn == RED:
            tokenimg = RED_TOKEN_IMG
        else:
            tokenimg = BLACK_TOKEN_IMG

        self.window.blit(tokenimg, (self.tokenx - HALF_SPACE_SIZE, self.tokeny, SPACE_SIZE, SPACE_SIZE))


    def mEndDraggingGetColumn(self):        
        column = -1
        if self.tokenx > X_MARGIN and self.tokenx < WINDOW_WIDTH - X_MARGIN:
            column = int((self.tokenx - X_MARGIN) / SPACE_SIZE)

        return column


    def mStartAnimiatingDown(self, column):     
        # Move was good, set up for animating the drop
        self.animatedTokenX = X_MARGIN + (column * SPACE_SIZE)
        self.animatedTokenY = Y_MARGIN - SPACE_SIZE
        self.dropSpeed = STARTING_DROP_SPEED


    def mAnimatingDown(self, turn, targetRow, targetCol):
        done = False
        self.animatedTokenY += int(self.dropSpeed)
        self.dropSpeed += INCREMENTAL_DROP_SPEED
        if int((self.animatedTokenY - Y_MARGIN) / SPACE_SIZE) >= targetRow:
            done = True

        else:
            if turn == RED:
                tokenImg = RED_TOKEN_IMG
            else:
                tokenImg = BLACK_TOKEN_IMG
            self.window.blit(tokenImg, (self.animatedTokenX, self.animatedTokenY, SPACE_SIZE, SPACE_SIZE))

        return done


    def mStartComputerAnimatingLeft(self, targetColumn):
        self.animatedTokenX = WINDOW_WIDTH - int(3 * HALF_SPACE_SIZE)
        self.animatedTokenY = Y_MARGIN - SPACE_SIZE
        self.animatedTokenXTarget = X_MARGIN + (targetColumn * SPACE_SIZE) + HALF_SPACE_SIZE


    def mComputerAnimatingLeft(self, targetColumn):
        done = False
        self.animatedTokenX -= 7  # move left 7 pixels, ... seems OK
        if self.animatedTokenX > self.animatedTokenXTarget:
            self.window.blit(BLACK_TOKEN_IMG, (self.animatedTokenX - HALF_SPACE_SIZE, PILE_Y, SPACE_SIZE, SPACE_SIZE))
        else:
            self.animatedTokenX = X_MARGIN + (targetColumn * SPACE_SIZE)
            self.animatedTokenY = Y_MARGIN - SPACE_SIZE
            self.dropSpeed = STARTING_DROP_SPEED
            done = True
        return done

    

class Model():
    def __init__(self):
        pass
    
    def mInitGame(self):
        # Set up a 'gameBoard' data structure with every cell set to EMPTY.

        #Original code as setting up an empty list, and adding rows through a for loop
 #       self.gameBoard = []
 #       for row in range(BOARD_NROWS):
 #           self.gameBoard.append([EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY])

        # Now as a list comprehension

        self.gameBoard = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY] for row in range(BOARD_NROWS)]

        self.turn = None

    def mGetGameBoard(self):
        return self.gameBoard

    def mSetPieceInGameBoard(self, row, col, color):
        self.gameBoard[row][col] = color


    def mStartGame(self):
        # Randomly choose who goes first.  (Set turn)
        if random.randrange(0,2) == 0:
            self.turn = RED
        else:
            self. turn = BLACK
        return self.turn

    def mSetTurn(self, whoseTurn):
        self.turn = whoseTurn

    def mGetTurn(self):
        return self.turn

    def mGetLowestEmptyRow(self, board, column):
    # Return the row number of the lowest empty row in the given column.  Or -1 for none
        for row in range(BOARD_NROWS-1, -1, -1):
            # if this is the lowest empty, return it
            if board[row][column] == EMPTY:
                return row
        return -1


    def mIsValidMove(self, board, column):
        # Returns True if there is an empty space in the given column.
        # Otherwise returns False.

        #If move is not valid, return False, else return TRUE
        if (column < 0) or (column > (BOARD_NCOLS -1)) or board[0][column] != EMPTY:
            return False

        return True


    def mIsBoardFull(self, board):
        # Returns True if there are no empty spaces anywhere on the board.
        for row in range(BOARD_NROWS):
            for col in range(BOARD_NCOLS):
                if board[row][col] == EMPTY:
                    return False
        return True


    def mIsWinner(self, board, tile):

        # check horizontal spaces
        for row in range (BOARD_NROWS):
            for col in range (BOARD_NCOLS-3):
                #print 'Board tile at ' + str(row) + ' ' + str(col) + ' is ' + board[row][col]
                if board[row][col] == tile and board[row][col+1] == tile and board[row][col+2] == tile and board[row][col+3] == tile:
                    self.winningRowColStart = [row, col]
                    self.winningRowColEnd = [row, col + 3]
                    return True
                
        #check vertical spaces
        for row in range(BOARD_NROWS-3):
            for col in range (BOARD_NCOLS):
                if board[row][col] == tile and board[row+1][col] == tile and board[row+2][col] == tile and board[row+3][col] == tile:
                    self.winningRowColStart = [row, col]
                    self.winningRowColEnd = [row + 3, col]
                    return True

        #for diagonal down right
        for row in range(BOARD_NROWS-3):
            for col in range (BOARD_NCOLS-3):
                if board[row][col] == tile and board[row+1][col+1] == tile and board[row+2][col+2] == tile and board[row+3][col+3] == tile:
                    self.winningRowColStart = [row, col]
                    self.winningRowColEnd = [row + 3, col + 3]
                    return True

        #for diagonal up right
        for row in range(3, BOARD_NROWS):
            for col in range (0,BOARD_NCOLS-3):
                if board[row][col] == tile and board[row-1][col+1] == tile and board[row-2][col+2] == tile and board[row-3][col+3] == tile:
                    self.winningRowColStart = [row, col]
                    self.winningRowColEnd = [row - 3, col + 3]
                    return True
 
        return False  # No winner this time

    def mGetWinningRowColStartEnd(self):
        return self.winningRowColStart, self.winningRowColEnd


    # For development debugging
    def mPrintBoard(self, message = ''):
         print()
         if message != '':
             print(message)
         for row in range (BOARD_NROWS):
             print(self.gameBoard[row])


    #### FOR AUTOMATED COMPUTER MOVES ###############

    def mGetComputerMove(self):
        potentialMoves = self.mGetPotentialMoves(self.gameBoard, BLACK, DIFFICULTY)
        
        # get the best fitness from the potential moves
        bestMoveFitness = -1000
        for i in range(BOARD_NCOLS):
            if self.mIsValidMove(self.gameBoard, i) and (potentialMoves[i] > bestMoveFitness):
                bestMoveFitness = potentialMoves[i]
                
        # find all potential moves that match this best fitness
        bestMoves = []
        for i in range(len(potentialMoves)):
            if self.mIsValidMove(self.gameBoard, i) and (potentialMoves[i] == bestMoveFitness):
                bestMoves.append(i)

        #print '\nIn mGetComputerMove, potentialMoves, bestMoves, bestMoveFitness, and move chosen: '
        #print str(potentialMoves)
        #print str(bestMoves)
        #print str(bestMoveFitness)
                
        moveChosen = random.choice(bestMoves)
        print(str(moveChosen))
        return moveChosen


    def mGetPotentialMoves(self, board, tile, lookAhead):
        if lookAhead == 0 or self.mIsBoardFull(board):
            return [0] * BOARD_NCOLS

        if tile == RED:
            enemyTile = BLACK
        else:
            enemyTile = RED

        # Figure out the best move to make.
        potentialMoves = [0] * BOARD_NCOLS
        for firstMove in range(BOARD_NCOLS):
            dupeBoard = copy.deepcopy(board)
            if not self.mIsValidMove(dupeBoard, firstMove):
                continue
            self.mMakeMove(dupeBoard, tile, firstMove)
            if self.mIsWinner(dupeBoard, tile):
                # a winning move automatically gets a perfect fitness
                potentialMoves[firstMove] = 1
                break # don't bother calculating other moves
            else:
                # do other player's counter moves and determine best one
                if self.mIsBoardFull(dupeBoard):
                    potentialMoves[firstMove] = 0
                else:
                    for counterMove in range(BOARD_NCOLS):
                        dupeBoard2 = copy.deepcopy(dupeBoard)
                        if not self.mIsValidMove(dupeBoard2, counterMove):
                            continue
                        self.mMakeMove(dupeBoard2, enemyTile, counterMove)
                        if self.mIsWinner(dupeBoard2, enemyTile):
                            # a losing move automatically gets the worst fitness
                            potentialMoves[firstMove] = -1
                            break
                        else:
                            # do the recursive call to mGetPotentialMoves()
                            results = self.mGetPotentialMoves(dupeBoard2, tile, lookAhead - 1)
                            potentialMoves[firstMove] += (sum(results) / BOARD_NCOLS) / BOARD_NCOLS

        #print 'Potential moves: ' + str(potentialMoves)
        return potentialMoves

    def mMakeMove(self, board, player, column):
        row = self.mGetLowestEmptyRow(board, column)
        if row != -1:
            board[row][column] = player



# MAIN PROGRAM
def main():
    pygame.init()
    pygame.mixer.init()  #initialize the sound mixer
    pygame.display.set_caption("Irv Kalb's Connect 4 game")
    soundDrop = pygame.mixer.Sound('sounds/soundDrop.wav')
    soundHitBottom = pygame.mixer.Sound('sounds/hitBottom.wav')
    soundBuzz = pygame.mixer.Sound('sounds/buzz.wav')
    soundApplause = pygame.mixer.Sound('sounds/applause.wav')

    oView = View(WINDOW_WIDTH, WINDOW_HEIGHT)  # create the view
    oModel = Model()   #  create the model
    fpsClock = pygame.time.Clock()

    oModel.mInitGame()
    oView.mSetMessageText('')
    state = STATE_START_GAME

    while True: # main game loop

        oView.mClear()
        turn = oModel.mGetTurn()
        oView.mDrawPiles(turn)
        
        if turn == RED:
            pileRect = RED_PILE_RECT
        if turn == BLACK:
            pileRect = BLACK_PILE_RECT

        currentGameBoard = oModel.mGetGameBoard()

        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif oView.mButtonClicked('restart', event):      
                oModel.mInitGame()
                oView.mSetMessageText('')
                state = STATE_START_GAME

            elif (state == STATE_START_GAME) and oView.mButtonClicked('humanHuman', event):
                gameMode = HUMAN_VS_HUMAN
                turn = oModel.mStartGame()
                oView.mStartGame(turn)
                state = STATE_WAITING


            elif (state == STATE_START_GAME) and oView.mButtonClicked('humanComputer', event):
                gameMode = HUMAN_VS_COMPUTER 
                turn = oModel.mStartGame()
                oView.mStartGame(turn)
                state = STATE_WAITING

            elif (state == STATE_WAITING) and (event.type == pygame.MOUSEBUTTONDOWN) and pileRect.collidepoint(event.pos):
                #start of dragging on token pile.
                state = STATE_DRAGGING
                theX, theY = event.pos
                theY = PILE_Y
                oView.mStartDragging(theX, theY)
                
            elif  (state == STATE_DRAGGING) and (event.type == pygame.MOUSEBUTTONUP):
                # User let go of the token being dragged
                moveOK = False   # assume bad move
                col = oView.mEndDraggingGetColumn()
                if col >= 0:   #valid move
                    row = oModel.mGetLowestEmptyRow(currentGameBoard, col)
                    if oModel.mIsValidMove(currentGameBoard, col) and (row != -1):
                        moveOK = True
                        soundDrop.play()
                        oView.mStartAnimiatingDown(col)                    

                if moveOK:
                    state = STATE_ANIMATING_DOWN
                    
                else:
                    state = STATE_WAITING
                    soundBuzz.play()

         
        #GAME LOGIC HERE - based on state                   

        if state == STATE_WAITING:
            if (gameMode == HUMAN_VS_COMPUTER) and (turn == BLACK):  #chose computer move
                computerMoveColumn = oModel.mGetComputerMove()
                #print 'Computer move: ' + str(computerMoveColumn)

                oView.mStartComputerAnimatingLeft(computerMoveColumn)
                state = STATE_COMPUTER_ANIMATING_LEFT

        elif state == STATE_DRAGGING:
            if event.type == pygame.MOUSEMOTION:
                #update the position of the token being dragged
                theX, theY= event.pos
                theY = PILE_Y  #overwrite, to restrict Y
            oView.mDragging(turn, theX, theY)

        elif state == STATE_COMPUTER_ANIMATING_LEFT:
            done = oView.mComputerAnimatingLeft(computerMoveColumn)
            if done:
                state = STATE_ANIMATING_DOWN
                row = oModel.mGetLowestEmptyRow(currentGameBoard, computerMoveColumn)
                col = computerMoveColumn
                soundDrop.play()


        elif state == STATE_ANIMATING_DOWN:
                done = oView.mAnimatingDown(turn, row, col)
                if done:
                    state = STATE_EVALUATE
                    soundHitBottom.play()
                    oModel.mSetPieceInGameBoard(row, col, turn)  # add in the new piece
                    #Update our copy of the board:
                    currentGameBoard = oModel.mGetGameBoard()

        elif state == STATE_EVALUATE:
            state = STATE_WAITING  # can overide below if game is over
            
            if turn == RED:
                if oModel.mIsWinner(currentGameBoard, RED):
                    oView.mSetMessageText('Red WINS!!')
                    state = STATE_GAME_OVER
                    soundApplause.play()
                else:    
                    oModel.mSetTurn(BLACK) # switch to other player's turn
                    oView.mSetMessageText("Black's turn")
                    if gameMode == HUMAN_VS_COMPUTER:
                        oView.mDrawPiles(turn)  #drawn while the computer is 'thinking'

            else:  #BLACK                         
                if oModel.mIsWinner(currentGameBoard, BLACK):
                    oView.mSetMessageText('Black WINS!!')
                    state = STATE_GAME_OVER
                    soundApplause.play()
                else:    
                    oModel.mSetTurn(RED) # switch to other player's turn
                    oView.mSetMessageText("Red's turn")
                
            if oModel.mIsBoardFull(currentGameBoard):
                # A completely filled board means it's a tie.
                oView.mSetMessageText("It's a tie")
                state = STATE_GAME_OVER_TIE
                    
    # DRAW ALL GAME ELEMENTS:

        oView.mDrawBoard(currentGameBoard, turn)

        if state == STATE_GAME_OVER:
            start, end = oModel.mGetWinningRowColStartEnd()
            oView.mDrawWinningLine(start, end)

        elif state == STATE_START_GAME:
            turn = None
            oView.mShowRules()
                       
        pygame.display.update()
        fpsClock.tick(FPS)

# Check for main name
if __name__ == '__main__':
    main()
