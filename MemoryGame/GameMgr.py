#  Game Manager Class

import pygame
from pygame.locals import *
import random
import pygwidgets
from Card import *

STATE_FIRST_CLICK = 'firstClick'
STATE_SECOND_CLICK = 'secondClick'
STATE_SHOWING_MISMATCH = 'mismatch'
STATE_DONE = 'done'

N_COLUMNS = 6
X_START = 196
Y_START = 112
X_SPACING = 70
Y_SPACING = 60

YELLOW = (255, 255, 0)

### GAME MANAGER
class GameMgr():
    def __init__(self, window):
        self.window = window
        self.cardNumberList = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
        self.nCards = len(self.cardNumberList)
        self.nMatchesToWin = self.nCards // 2

        self.cardList = []
        for cardIndex in range(0, self.nCards):
            nCurrentRow = cardIndex // N_COLUMNS
            nCurrentCol = cardIndex - (nCurrentRow * N_COLUMNS)
            cardX = X_START + (nCurrentCol * X_SPACING)
            cardY = Y_START + (nCurrentRow * Y_SPACING)
            oCard = Card(window, cardX, cardY)
            self.cardList.append(oCard)

        # Load images and sounds
        self.oYouWin = pygwidgets.Image(self.window, (400, 352), 'images/youWin.png')
        self.oApplauseSound = pygwidgets.SoundEffect('sounds/applause.wav')
        self.oBuzzSound = pygwidgets.SoundEffect('sounds/buzz.wav')
        self.oDingSound = pygwidgets.SoundEffect('sounds/ding.wav')

        # Set up display fields
        self.nTriesDisplay = pygwidgets.DisplayText(window, (332, 327), '0',
                                               fontName='monospace', fontSize=16, textColor=YELLOW)
        self.nMatchesDisplay = pygwidgets.DisplayText(window, (332, 353), '0',
                                                 fontName='monospace', fontSize=16, textColor=YELLOW)


        self.reset() # set up for first game

    def reset(self):
        random.shuffle(self.cardNumberList)  # shuffle the list of card numbers
        print(self.cardNumberList)    #  For debugging
        for index, oCard in enumerate(self.cardList):  #  Assign card numbers
            thisValue = self.cardNumberList[index]
            oCard.reset(thisValue)

        self.nTries = 0
        self.nMatches = 0
        self.nFrames = 0
        self.state = STATE_FIRST_CLICK

    def handleClick(self, mouseX, mouseY):
        clickedOnCard = False
        for oCard in self.cardList:
            if oCard.wasClicked(mouseX, mouseY):
                clickedOnCard = True
                break
        if not clickedOnCard:
            return  # no card was clicked on

        if self.state == STATE_FIRST_CLICK:
            self.oFirstCard = oCard
            self.oFirstCard.show()
            self.state = STATE_SECOND_CLICK

        elif self.state == STATE_SECOND_CLICK:
            self.oSecondCard = oCard
            self.oSecondCard.show()
            self.nTries = self.nTries + 1
            self.nTriesDisplay.setValue(str(self.nTries))   #update field

            firstCardValue = self.oFirstCard.getValue()
            secondCardValue = self.oSecondCard.getValue()
            if firstCardValue == secondCardValue:
                self.nMatches = self.nMatches + 1
                self.nMatchesDisplay.setValue(str(self.nMatches)) # update field
                print("It's a match")  # debugging
                if self.nMatchesToWin == self.nMatches:  # Game over
                    self.oApplauseSound.play()
                    self.state = STATE_DONE
                    print('Game over')

                else:
                    self.oDingSound.play()  # Correct, but not a win yet
                    self.state = STATE_FIRST_CLICK
            else:
                print('Not a match')
                self.oBuzzSound.play()
                self.nFrames = 0  # To allow cards to show for a short time
                self.state = STATE_SHOWING_MISMATCH

    def update(self):
        if self.state == STATE_SHOWING_MISMATCH:
            self.nFrames = self.nFrames + 1
            if self.nFrames == 50:  # less than 2 seconds
                self.oFirstCard.hide()
                self.oSecondCard.hide()
                self.state = STATE_FIRST_CLICK

    def draw(self):
        for oCard in self.cardList:
            oCard.draw()

        self.nTriesDisplay.draw()
        self.nMatchesDisplay.draw()

        if self.state == STATE_DONE:
            self.oYouWin.draw()