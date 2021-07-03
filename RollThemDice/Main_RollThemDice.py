#  2/17 by Irv Kalb
#

import pygame
import random
import sys
import pygwidgets
from pygame.locals import *

MAX_ROUNDS = 250

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 550
FRAMES_PER_SECOND = 60
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (0, 222, 222)


MAX_BAR_HEIGHT = 400
BAR_BOTTOM = 350
BAR_WIDTH = 30
BAR_COLOR = (128, 128, 128)
COLUMN_LEFT_START = -20
COLUMN_OFFSET = 60
SIDES_PER_DIE = 6
SIDES_PER_DIE_PLUS_ONE = SIDES_PER_DIE + 1


STATE_WAITING = 'waiting'
STATE_RUNNING = 'running'



pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Roll Them Dice')
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))



# Bin Class

class Bin():
    def __init__(self, window, id, nRounds):
        self.id = id
        self.window = window
        self.count = 0
        self.nTrialsSoFar = 0
        self.pixelsPerCount = MAX_BAR_HEIGHT

        self.left = COLUMN_LEFT_START + (self.id * COLUMN_OFFSET)
        self.oBinLabel = pygwidgets.DisplayText(window, (self.left + 3, BAR_BOTTOM + 12), str(self.id), \
                        fontName='arial', fontSize=24, textColor=BLACK, width=25, justified='center')
        self.oBinCount = pygwidgets.DisplayText(window, (self.left - 5, BAR_BOTTOM + 36), '', \
                        fontName='arial', fontSize=18, textColor=BLACK, width=45, justified='center')
        self.oBinPercent = pygwidgets.DisplayText(window, (self.left - 5, BAR_BOTTOM + 50), '', \
                        fontName='arial', fontSize=18, textColor=BLACK, width=50, justified='center')
        self.changeNumberOfTrials(nRounds)

        self.reset()


    def reset(self):
        self.count = 0
        self.nTrialsSoFar = 0
        self.oBinPercent.setValue('')

    def increment(self):
        self.count = self.count + 1

    def setNumberOfTrials(self, nTrials):
        self.nTrialsSoFar = nTrials

    def changeNumberOfTrials(self, nTrials):
        # force float here, use int when drawing rects
        self.nPixelsPerTrial = float(MAX_BAR_HEIGHT)  / nTrials

    def draw(self):
        if self.nTrialsSoFar == 0:
            percent = 0
        else:
            percent = (self.count * 100)/ self.nTrialsSoFar

        # calculate the real height, multiply by two to make it look better
        # All bars will certainly be less than 50%
        barHeight = int(self.count * self.nPixelsPerTrial) * 2
        thisRect = pygame.Rect(self.left, BAR_BOTTOM - barHeight, BAR_WIDTH, barHeight)
        pygame.draw.rect(self.window, BAR_COLOR, thisRect, 0)

        self.oBinLabel.draw()

        self.oBinCount.setValue(str(self.count))
        self.oBinCount.draw()
        
        self.oBinPercent.setValue(format(percent, '.1f') + '%')
        self.oBinPercent.draw()



state = STATE_RUNNING
nRoundsRolled = 0
nRoundsToRun = MAX_ROUNDS

oTitleDisplay = pygwidgets.DisplayText(window, (330, 30), 'Roll Them Dice!', \
                fontName='monospaces', fontSize=34, textColor=BLACK)
oQuitButton = pygwidgets.TextButton(window, (20, 460), 'Quit', width=100, height=35)
oRunButton = pygwidgets.TextButton(window, (690, 460), 'Run', width=100, height=35)
oRunButton.disable()

oRoundsDisplay = pygwidgets.DisplayText(window, (315, 460), '0', \
                fontName='monospaces', fontSize=28, textColor=BLACK, width=70, justified='right')
oOutOfDisplay = pygwidgets.DisplayText(window, (390, 460), 'out of', \
                fontName='monospaces', fontSize=28, textColor=BLACK)

oMaxRoundsInput = pygwidgets.InputText(window, (454, 460), str(nRoundsToRun), \
                                       fontName='monospaces', fontSize=28, width=70, initialFocus=True)

oDiceImage = pygwidgets.Image(window, (15, 15), "images/dice.png")




binsList = []
for diceTotalForBin in range(0, (SIDES_PER_DIE + SIDES_PER_DIE + 1)):
    oBin = Bin(window, diceTotalForBin, nRoundsToRun)
    binsList.append(oBin)


while True:
    # Handle events
    for event in pygame.event.get():
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

        if oQuitButton.handleEvent(event):
            pygame.quit()
            sys.exit()

        if oRunButton.handleEvent(event):
            nRoundsToRun = oMaxRoundsInput.getText()
            nRoundsToRun = int(nRoundsToRun)
            nRoundsRolled = 0
            state = STATE_RUNNING
            oRunButton.disable()
            for oBin in binsList:
                oBin.reset()

        if oMaxRoundsInput.handleEvent(event):
            nRoundsToRun = oMaxRoundsInput.getText()
            nRoundsToRun = int(nRoundsToRun)
            nRoundsRolled = 0
            state = STATE_RUNNING
            oRunButton.disable()
            for oBin in binsList:
                oBin.reset()
                oBin.changeNumberOfTrials(nRoundsToRun)

    if state == STATE_RUNNING:
        die1 = random.randrange(1, SIDES_PER_DIE_PLUS_ONE)
        die2 = random.randrange(1, SIDES_PER_DIE_PLUS_ONE)
        nRoundsRolled = nRoundsRolled + 1
        oRoundsDisplay.setValue(str(nRoundsRolled))
        for oBin in binsList:
            oBin.setNumberOfTrials(nRoundsRolled)

        theSum = die1 + die2
        binsList[theSum].increment()

        if nRoundsRolled == nRoundsToRun:
            state = STATE_WAITING
            oRunButton.enable()



    # Draw everything
    window.fill(BACKGROUND_COLOR)

    # Draw the game
    oTitleDisplay.draw()
    oDiceImage.draw()
    oRunButton.draw()
    oRoundsDisplay.draw()
    oOutOfDisplay.draw()
    oMaxRoundsInput.draw()
    oQuitButton.draw()
    for number, oBin in enumerate(binsList):
        if number >= 2:
            oBin.draw()


    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)
