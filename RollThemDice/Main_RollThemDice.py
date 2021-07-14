#  Roll Them Dice - Irv Kalb

import pygame
import random
import sys
import pygwidgets
from pygame.locals import *
from Bin import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 550
FRAMES_PER_SECOND = 60
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (0, 222, 222)

MAX_ROUNDS = 250
SIDES_PER_DIE = 6
SIDES_PER_DIE_PLUS_ONE = SIDES_PER_DIE + 1
STATE_WAITING = 'waiting'
STATE_RUNNING = 'running'

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Roll Them Dice')
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


state = STATE_RUNNING
nRoundsRolled = 0
nRoundsToRun = MAX_ROUNDS

oTitleDisplay = pygwidgets.DisplayText(window, (330, 30), 'Roll Them Dice!',
                       fontName='monospaces', fontSize=34)
oQuitButton = pygwidgets.TextButton(window, (20, 460), 'Quit', width=100, height=35)
oRunButton = pygwidgets.TextButton(window, (690, 460), 'Run', width=100, height=35)
oRunButton.disable()

oRoundsDisplay = pygwidgets.DisplayText(window, (315, 460), '0',
                          fontName='monospaces', fontSize=28, width=70, justified='right')
oOutOfDisplay = pygwidgets.DisplayText(window, (390, 460), 'out of',
                         fontName='monospaces', fontSize=28)

oMaxRoundsInput = pygwidgets.InputText(window, (454, 460), str(nRoundsToRun),
                             fontName='monospaces', fontSize=28, width=70, initialFocus=True)

oDiceImage = pygwidgets.Image(window, (28, 15), 'images/twoDice.png')
imagesDict =  {1:'images/dice1.png', 2:'images/dice2.png', 3:'images/dice3.png',
                      4:'images/dice4.png', 5:'images/dice5.png', 6:'images/dice6.png'}
oDie1 = pygwidgets.ImageCollection(window, (630, 15), imagesDict, 1)
oDie2 = pygwidgets.ImageCollection(window, (715, 15), imagesDict, 1)


binsList = []
for diceTotalForBin in range(0, (SIDES_PER_DIE + SIDES_PER_DIE + 1)):
    oBin = Bin(window, diceTotalForBin, nRoundsToRun)
    binsList.append(oBin)

while True:
    # Handle events
    for event in pygame.event.get():
        if oQuitButton.handleEvent(event) or (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()

        # If the user presses Enter or clickes the Run Button
        if oMaxRoundsInput.handleEvent(event) or oRunButton.handleEvent(event):
            nRoundsToRun = oMaxRoundsInput.getText()
            nRoundsToRun = int(nRoundsToRun)
            nRoundsRolled = 0
            state = STATE_RUNNING
            oRunButton.disable()
            for oBin in binsList:
                oBin.reset(nRoundsToRun)

    if state == STATE_RUNNING:
        die1 = random.randrange(1, SIDES_PER_DIE_PLUS_ONE)
        oDie1.replace(die1)
        die2 = random.randrange(1, SIDES_PER_DIE_PLUS_ONE)
        oDie2.replace(die2)
        nRoundsRolled = nRoundsRolled + 1
        oRoundsDisplay.setValue(str(nRoundsRolled))

        theSum = die1 + die2
        oBin = binsList[theSum]
        oBin.increment()

        for oBin in binsList:
            oBin.updatePercent(nRoundsRolled)

        if nRoundsRolled == nRoundsToRun:
            state = STATE_WAITING
            oRunButton.enable()

    # Draw everything
    window.fill(BACKGROUND_COLOR)

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
    oDie1.draw()
    oDie2.draw()

    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)
