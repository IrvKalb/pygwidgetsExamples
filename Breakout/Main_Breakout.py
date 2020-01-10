#  BreakOut
import pygame
import sys
from pygame.locals import *
import random
import pygwidgets

# CONSTANTS

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 532

FRAMES_PER_SECOND = 30

STATE_PLAYING = 'playingGame'
STATE_GAMEOVER = 'gameOver'

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RANDOMCOLOR = (123, 34, 235)
GRAY = (128, 128, 128)





### BALL CLASS ###

class Ball(object):
    START_BALL_Y = 430
    DIAMETER = 10
    STARTINGSPEED = 4

    def __init__(self, window, startingX):
        self.window = window
        self.radius = self.DIAMETER //2
        self.maxX = WINDOW_WIDTH - (self.radius)    
        self.mReset(startingX, 1)

    def mReset(self, startX, currentRoundNumber):
        # randomly, decide to move ball left or right
        if random.randrange(0, 2) == 0:
            self.xSpeed = self.STARTINGSPEED + currentRoundNumber
        else:
            self.xSpeed = -self.STARTINGSPEED - currentRoundNumber
        self.ySpeed = -self.STARTINGSPEED - currentRoundNumber  # moving up
        #print 'ball speed is:', self.xSpeed

        self.rect = pygame.Rect(startX, self.START_BALL_Y, self.DIAMETER, self.DIAMETER)

    def mMove(self):
        if (self.rect.left < self.radius) or (self.rect.left > self.maxX):
            self.xSpeed = -self.xSpeed
        if (self.rect.top < self.radius):
            self.ySpeed = -self.ySpeed

        self.rect.left= self.rect.left + self.xSpeed
        self.rect.top = self.rect.top + self.ySpeed
        return self.rect

    def mSwitchYDirection(self, hitBrickOrPaddle):
        self.ySpeed = -self.ySpeed
        if hitBrickOrPaddle == 'brick':
            # If collided with a brick,1 out of 4 chance of changing the x direction also
            if random.randrange(0, 4) == 1:
                self.xSpeed = -self.xSpeed
                
    def mIsGoingDown(self):
        goingDown = (self.ySpeed > 0)
        return goingDown
    
    def mDraw(self):
        pygame.draw.circle(window, WHITE, (self.rect.left, self.rect.top), self.radius, 0) 


    
        
### PADDLE CLASS ###
    
class Paddle(object):
    START_PADDLE_Y = 460
    SHRINKAGE = 5
    PADDLE_STARTING_WIDTH = 100 + SHRINKAGE  # will shrink to 100 first time.
    PADDLE_HEIGHT = 10
    COLOR = WHITE
    STARTING_SPEED = 9
    MINIMUM_WDTH = 20


    def __init__(self, window):
        self.window = window
        self.firstTime = True
        self.paddleWidth = self.PADDLE_STARTING_WIDTH
        self.mReset(1)  # starting at round 1

    def mReset(self, currentRoundNumber):
        self.paddleWidth = self.PADDLE_STARTING_WIDTH - (self.SHRINKAGE * currentRoundNumber)
        print('paddle width is:', self.paddleWidth)
        if self.paddleWidth < self.MINIMUM_WDTH:
            self.paddleWidth = self.MINIMUM_WDTH   # minimum
        self.maxX = WINDOW_WIDTH - self.paddleWidth
        self.nPixelsToMove = self.STARTING_SPEED + currentRoundNumber

        if self.firstTime:
            x = random.randrange(0, self.maxX)
            self.firstTime = False
        else:
            x = self.rect.left  # leave the paddle where the user left it
        self.rect = pygame.Rect(x, self.START_PADDLE_Y, self.paddleWidth, self.PADDLE_HEIGHT)

    def mMove(self, direction):
        if direction == 'left':
            potentialX = self.rect.left - self.nPixelsToMove
            if potentialX <= 0:
                self.rect.left = 0
            else:
                self.rect.left = potentialX

        else:  # move right
            potentialX = self.rect.left + self.nPixelsToMove
            if potentialX > self.maxX:
                self.rect.left = self.maxX
            else:
                self.rect.left = potentialX

        return self.rect

    def mGetCenter(self):
        center = self.rect.left + (self.paddleWidth / 2)
        return center

    def mGetRect(self):
        return self.rect

    def mDraw(self):
        pygame.draw.rect(window, self.COLOR, self.rect) #paddle




### BRICK CLASS ###

class Brick(object):
    BRICK_WIDTH = 100
    BRICK_HEIGHT = 30

    def __init__(self, window, x, y, color):
        self.window = window
        self.x = x
        self.y = y
        self.loc = (self.x, self.y)
        self.color = color
        self.showing = True
        self.brickRect = pygame.Rect(self.x, self.y, self.BRICK_WIDTH, self.BRICK_HEIGHT)

    def mDraw(self):
            if self.showing:
                pygame.draw.rect(window, self.color, self.brickRect)

    def mCollideRect(self, aRect):
        collided = aRect.colliderect(self.brickRect)
        return collided

    def mGetShowing(self):
        return self.showing

    def mSetShowing(self, trueOrFalse):
        self.showing = trueOrFalse



### BRICKMGR CLASS

class BrickMgr(object):
# Brick coordinates on window and color
# Each element is a list of x, y, color
    BRICK_INFO_LIST = [(110, 75, RED), (215, 75, RED), (320, 75, RED), (425, 75, RED),\
                              (55, 108, YELLOW), (160, 108, YELLOW), (265, 108, YELLOW), (370, 108, YELLOW), (475, 108, YELLOW), 
                              (110, 141, GREEN), (215, 141, GREEN), (320, 141, GREEN),(425, 141, GREEN), \
                              (55, 174, BLUE), (160, 174, BLUE), (265, 174, BLUE), (370, 174, BLUE), (475, 174, BLUE)]

    
    def __init__(self, window):
        self.window = window
        self.bricksList = []
        self.nBricks = len(BrickMgr.BRICK_INFO_LIST)
        for brickInfo in BrickMgr.BRICK_INFO_LIST:
            brickX = brickInfo[0]
            brickY = brickInfo[1]
            brickColor = brickInfo[2]

            oBrick = Brick(self.window, brickX, brickY, brickColor)
            self.bricksList.append(oBrick)

    def getNBricks(self):
        return self.nBricks

    def mSetAllShowing(self):
        for oBrick in self.bricksList:
            oBrick.mSetShowing(True)

    def mDraw(self):
        for oBrick in self.bricksList:
            oBrick.mDraw()


    def mCheckForCollision(self, ballRect):

        for oBrick in self.bricksList:
            brickShowing = oBrick.mGetShowing()
            if brickShowing:
                if oBrick.mCollideRect(ballRect):
                    oBrick.mSetShowing(False)
                    return True  #  collided with a brick

        return False  # no collision


    


###  MAIN CODE  ####
        
# Initialize pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
#pygame.font.SysFont(None, 36)
roundDisplay = pygwidgets.DisplayText(window, (20, 490), '', \
                                    fontSize=36, textColor=WHITE)
scoreDisplay = pygwidgets.DisplayText(window, (500, 490), '', \
                                    fontSize=36, textColor=WHITE, justified='right', width=130)

roundNumber = 1

# Load pics and sounds
gameOver = pygame.image.load('images/GameOver.png')
winner = pygame.image.load('images/Winner.png')

restartButton = pygwidgets.CustomButton(window, (280, 486), \
                                        up='images/RestartButtonUp.png', down='images/RestartButtonDown.png', over='images/RestartButtonOver.png', disabled= 'images/RestartButtonDisabled.png')
paddleBlip = pygame.mixer.Sound('sounds/paddleBlip.wav')
brickBlip = pygame.mixer.Sound('sounds/brickBlip.wav')
applause = pygame.mixer.Sound('sounds/applause.wav')
buzz = pygame.mixer.Sound('sounds/buzz.wav')

# Create the brick manager
oBrickMgr = BrickMgr(window)
nBricks = oBrickMgr.getNBricks()

# Create the paddle and the ball
oPaddle = Paddle(window)
paddleRect = oPaddle.mGetRect()
startingXForBall = oPaddle.mGetCenter()
oBall = Ball(window, startingXForBall)

clock = pygame.time.Clock()
state = STATE_PLAYING
nBricksHit = 0



# Main loop
while True:

    for event in pygame.event.get(): #loop through events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    if state == STATE_GAMEOVER:
        if restartButton.handleEvent(event):
            state = STATE_PLAYING
            if wonTheRound:
                roundNumber = roundNumber + 1
            else:
                roundNumber = 1
                

            oBrickMgr.mSetAllShowing()

            oPaddle.mReset(roundNumber)
            startingXForBall = oPaddle.mGetCenter()
            oBall.mReset(startingXForBall, roundNumber)
            nBricksHit = 0
  
    
    if state == STATE_PLAYING:
        # Tell the ball to move
        ballRect = oBall.mMove()
        if ballRect.top > WINDOW_HEIGHT:
            state = STATE_GAMEOVER
            buzz.play()
            wonTheRound = False

        # Handle paddle movement
        keyPressedList = pygame.key.get_pressed()
         
        # Moving Left       
        if keyPressedList[pygame.K_LEFT]:
            paddleRect = oPaddle.mMove('left')

        # Moving Right
        if keyPressedList[pygame.K_RIGHT]:
            paddleRect = oPaddle.mMove('right')

        # Cheat win!
        if keyPressedList[pygame.K_UP]:
            state = STATE_GAMEOVER
            wonTheRound = True
            


        if paddleRect.colliderect(ballRect):
            if oBall.mIsGoingDown():
                oBall.mSwitchYDirection('paddle')
                paddleBlip.play()

        else:  # check to see if we hit any brick
            hitABrick = oBrickMgr.mCheckForCollision(ballRect)
            if hitABrick:
                brickBlip.play()
                oBall.mSwitchYDirection('brick')
                #brickShowing = False
                nBricksHit = nBricksHit + 1

                if nBricksHit == nBricks:
                    state = STATE_GAMEOVER
                    applause.play()
                    wonTheRound = True

        roundDisplay.setValue('Round: ' + str(roundNumber))
        scoreDisplay.setValue('Score: ' + str(nBricksHit))
    
    
    # Draw everything
    window.fill(BLACK)


    oBrickMgr.mDraw()
        
    oPaddle.mDraw()
    roundDisplay.draw()
    scoreDisplay.draw()
        
    #state check
    if state == STATE_GAMEOVER:
        restartButton.draw()
        if wonTheRound:
            window.blit(winner, (190, 200))
        else:
            window.blit(gameOver, (190, 200))


    else:
        oBall.mDraw()


    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

