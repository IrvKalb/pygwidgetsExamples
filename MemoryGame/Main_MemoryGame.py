#  Memory Game

import pygame
from pygame.locals import *
import sys
import random
import pygwidgets


# CONSTANTS
WINDOW_WIDTH = 780
WINDOW_HEIGHT = 400
YELLOW = (255, 255, 0)

NROWS = 3
NCOLUMNS = 6
XSTART = 196
YSTART = 112
XSPACING = 70
YSPACING = 60
FRAMES_PER_SECOND = 30
STATE_FIRST_CLICK = 'firstClick'
STATE_SECOND_CLICK = 'secondClick'
STATE_SHOWING_MISMATCH = 'mismatch'
STATE_DONE = 'done'


### CARD
class Card(object):
    WIDTH = 54
    HEIGHT = 54

    def __init__(self, window, locX, locY):
        self.window = window
        self.locTuple = (locX, locY)
        self.rect = pygame.Rect(locX, locY, Card.WIDTH, Card.HEIGHT)
        cardBackPath = 'images/cardBack.png'
        self.backImage = pygame.image.load(cardBackPath)

    def mReset(self, value):
        self.cardValue = value
        cardPath = 'images/card' + str(self.cardValue) + '.png'
        self.cardImage = pygame.image.load(cardPath)

        self.mHide()

    def mHide(self):
        self.showing = False

    def mShow(self):
        self.showing = True

    def mDraw(self):
        if self.showing:
            self.window.blit(self.cardImage, self.locTuple)
        else:
            self.window.blit(self.backImage, self.locTuple)

    def mWasClicked(self, mouseX, mouseY):
        if self.showing:
            return False   # can't click it if it is already matched
        if self.rect.collidepoint(mouseX, mouseY):
            return True
        else:
            return False

    def mGetValue(self):
        return self.cardValue

### GAME MANAGER
class GameMgr(object):
    def __init__(self, window):
        self.cardNumberList = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
        self.nCards = len(self.cardNumberList)

        self.cardList = []
        for cardIndex in range(0, self.nCards):
            nCurrentRow = cardIndex // NCOLUMNS
            nCurrentCol = cardIndex - (nCurrentRow * NCOLUMNS)
            cardX = XSTART + (nCurrentCol * XSPACING)
            cardY = YSTART + (nCurrentRow * YSPACING);
            oCard = Card(window, cardX, cardY);
            self.cardList.append(oCard)
        self.mReset() # set up for first game

    def mReset(self):
        random.shuffle(self.cardNumberList)  # shuffle the list of card numbers
        print(self.cardNumberList)    #  For debugging  TEMPORARY
        for index, card in enumerate(self.cardList):
            thisValue = self.cardNumberList[index]
            card.mReset(thisValue)

    def mWasClicked(self, mouseX, mouseY):
        for card in self.cardList:
            if card.mWasClicked(mouseX, mouseY):
                return card  # return the object that was clicked on

        return None  # no card was clicked on

    def mDraw(self):
        for card in self.cardList:
            card.mDraw()

    def mGetNMatches(self):
        return self.nCards // 2


# Initialization Code
pygame.init()
window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

oGameMgr = GameMgr(window)
nMatchesToWin = oGameMgr.mGetNMatches()
nMatches = 0
nTries = 0
state = STATE_FIRST_CLICK

clock = pygame.time.Clock()  # set the speed (frames per second)

# Load images and sounds
background = pygame.image.load("images/background.png")
youWin = pygame.image.load("images/youWin.png")
applause = pygame.mixer.Sound('sounds/applause.wav')
buzz = pygame.mixer.Sound('sounds/buzz.wav')
ding = pygame.mixer.Sound('sounds/ding.wav')


# Set up fields and buttons
#gameFont = pygame.font.SysFont("monospaces", 24)

nTriesDisplay = pygwidgets.DisplayText(window, (332, 327), '0', \
                                    fontName='monospaces', fontSize=24, textColor=YELLOW)
nMatchesDisplay = pygwidgets.DisplayText(window, (332, 353), '0', \
                                    fontName='monospaces', fontSize=24, textColor=YELLOW)
newGameButton = pygwidgets.CustomButton(window, (490, 323),\
                up='images/newGame.png', over='images/newGameOver.png', down='images/newGameDown.png')


### MAIN LOOP
while True:

    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            sys.exit()

        if  newGameButton.handleEvent(event):
            nTries = 0
            nMatches = 0
            state = STATE_FIRST_CLICK
            oGameMgr.mReset()

        if event.type == MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if state == STATE_FIRST_CLICK:
                # This returns -1 if no click, or the card number of card clicked
                oFirstCard = oGameMgr.mWasClicked(mouseX, mouseY)
                if oFirstCard != None:
                    oFirstCard.mShow()
                    firstCardValue = oFirstCard.mGetValue()
                    state = STATE_SECOND_CLICK
                    break
            elif state == STATE_SECOND_CLICK:
                oSecondCard = oGameMgr.mWasClicked(mouseX, mouseY)
                if oSecondCard != None:
                    nTries = nTries + 1
                    oSecondCard.mShow()
                    secondCardValue = oSecondCard.mGetValue()
                    if firstCardValue == secondCardValue:
                        nMatches = nMatches + 1
                        print('Its a match')
                        if nMatchesToWin == nMatches:
                            applause.play()
                            state = STATE_DONE
                            print('Game over')

                        else:
                            ding.play()
                            state = STATE_FIRST_CLICK

                    else:
                        print('Not a match')
                        buzz.play()
                        nFrames = 0
                        state = STATE_SHOWING_MISMATCH
                    break

    if state == STATE_SHOWING_MISMATCH:
        nFrames = nFrames + 1
        if nFrames == 50:  #  less than 2 seconds
            oFirstCard.mHide()
            oSecondCard.mHide()
            state = STATE_FIRST_CLICK

    nTriesDisplay.setValue(str(nTries))
    nMatchesDisplay.setValue(str(nMatches))

    #Draw everything
    window.blit(background, (0, 0))
    oGameMgr.mDraw()
    newGameButton.draw()
    nTriesDisplay.draw()
    nMatchesDisplay.draw()
    if state == STATE_DONE:
        window.blit(youWin, (400, 352))

       
    # update the window
    pygame.display.update()

    # slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make PyGame wait the correct amount
