#  Memory Game

import pygame
from pygame.locals import *
import sys
import pygwidgets
from GameMgr import *

WINDOW_WIDTH = 780
WINDOW_HEIGHT = 400
FRAMES_PER_SECOND = 30

# Initialization
pygame.init()
window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
clock = pygame.time.Clock()  # set the speed (frames per second)

# Create variables
oGameMgr = GameMgr(window)
oBackground = pygwidgets.Image(window, (0, 0), 'images/background.png')
oNewGameButton = pygwidgets.CustomButton(window, (490, 323),
                                        up='images/newGame.png', over='images/newGameOver.png',
                                        down='images/newGameDown.png')

### MAIN LOOP
while True:

    for event in pygame.event.get():
        # check if the event is the close button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif oNewGameButton.handleEvent(event):
            oGameMgr.reset()

        elif event.type == MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            oGameMgr.handleClick(mouseX, mouseY)


    oGameMgr.update()  # To allow for timing to reset incorrect guess and update fields

    # Draw everything
    oBackground.draw()
    oGameMgr.draw()
    oNewGameButton.draw()
       
    # Update the window
    pygame.display.update()

    # Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make pygame wait the correct amount