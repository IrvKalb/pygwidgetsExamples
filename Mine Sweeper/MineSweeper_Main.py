# Minesweeper

import pygame
import pygwidgets
import pyghelpers
from pygame.locals import *
import sys
from Game import *
import random

from Constants import *
from Cell import *

FRAMES_PER_SECOND = 60
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (222, 222, 222)

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Main code
oGame = Game(window)

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        oGame.handleEvent(event)

    oGame.update()

    window.fill(BACKGROUND_COLOR)
    oGame.draw()

    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)
