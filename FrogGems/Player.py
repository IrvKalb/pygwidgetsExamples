import pygame
from Constants import *
import pygwidgets
import random
from pygame.locals import *


class Player():
    def __init__(self, window):
        self.window = window
        self.minRow = 0
        self.maxRow = 5
        self.minCol = 0
        self.maxCol = 4
        self.hOffset = 10  # horizontal pixels to offset frog to be in center of cell
        self.vOffset = 13  # vertical pixels to offset frog to be in center of cell

        self.image = pygwidgets.ImageCollection(window, (0, 0),
                                {'alive':'images/frog.png', 'dead':'images/frogDead.png'}, 'alive')

        self.newRound(1)
        
    def setLocFromRowCol(self):
        # Convert row and column to X, Y location
        loc = ((self.col * COL_WIDTH) + self.hOffset), (ROW_OFFSET + (self.row * ROW_HEIGHT) + self.vOffset)
        self.image.setLoc(loc)

    def newRound(self, levelNumber):
        self.row = random.choice([self.maxRow - 1, self.maxRow])
        self.col = random.choice(range(0, self.maxCol))
        self.setLocFromRowCol()
        self.image.replace('alive')

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == K_LEFT:
                if self.col > self.minCol:
                    self.col = self.col - 1
            elif event.key == K_RIGHT:
                if self.col < self.maxCol:
                    self.col = self.col + 1
            elif event.key == K_UP:
                if self.row > self.minRow:
                    self.row = self.row - 1
            elif event.key == K_DOWN:
                if self.row < self.maxRow:
                    self.row = self.row + 1
            #print(self.row, self.col)
            self.setLocFromRowCol()

    def showDead(self):
        self.image.replace('dead')

    def getRect(self):
        return self.image.getRect()

    def getRowCol(self):
        return (self.row, self.col)

    def draw(self):
        self.image.draw()
        