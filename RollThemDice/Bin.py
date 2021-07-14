#  Roll Them Dice

import pygame
import random
import sys
import pygwidgets
from pygame.locals import *

MAX_BAR_HEIGHT = 400
BAR_BOTTOM = 350
BAR_WIDTH = 30
BAR_COLOR = (128, 128, 128)
COLUMN_LEFT_START = -20
COLUMN_OFFSET = 60

# Bin Class
class Bin():
    def __init__(self, window, id, nRounds):
        self.id = id
        self.window = window
        self.pixelsPerCount = MAX_BAR_HEIGHT

        self.left = COLUMN_LEFT_START + (self.id * COLUMN_OFFSET)
        self.oBinLabel = pygwidgets.DisplayText(window,
                                (self.left + 3, BAR_BOTTOM + 12), self.id,
                                fontName='arial', fontSize=24, width=25, justified='center')
        self.oBinCount = pygwidgets.DisplayText(window,
                                (self.left - 5, BAR_BOTTOM + 40), '',
                                fontName='arial', fontSize=18, width=45, justified='center')
        self.oBinPercent = pygwidgets.DisplayText(window,
                                (self.left - 5, BAR_BOTTOM + 60), '',
                                 fontName='arial', fontSize=18, width=50, justified='center')
        self.reset(nRounds)

    def reset(self, nTrials):
        self.count = 0
        self.oBinPercent.setValue('')
        # force float here, use int when drawing rects
        self.nPixelsPerTrial = float(MAX_BAR_HEIGHT)  / nTrials

    def increment(self):
        self.count = self.count + 1

    def updatePercent(self, nTrialsSoFar):
        self.percent = (self.count * 100.) / nTrialsSoFar

    def draw(self):
        # Calculate the real height, multiply by two to make it look better
        # All bars will certainly be less than 50%
        barHeight = int(self.count * self.nPixelsPerTrial)  * 2
        thisRect = pygame.Rect(self.left, BAR_BOTTOM - barHeight, BAR_WIDTH, barHeight)
        pygame.draw.rect(self.window, BAR_COLOR, thisRect, 0)

        self.oBinLabel.draw()

        self.oBinCount.setValue(str(self.count))
        self.oBinCount.draw()
        
        self.oBinPercent.setValue(format(self.percent, '.1f') + '%')
        self.oBinPercent.draw()