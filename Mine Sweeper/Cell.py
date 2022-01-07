# Cell class

import pygame
import pygwidgets
from Constants import *

class Cell():
    tile = pygame.image.load('images/tile.jpg')
    mine = pygame.image.load('images/mine.jpg')
    mineShow = pygame.image.load('images/mineShow.jpg')
    flag = pygame.image.load('images/flag.jpg')
    zero = pygame.image.load('images/0.jpg')
    one = pygame.image.load('images/1.jpg')
    two = pygame.image.load('images/2.jpg')
    three = pygame.image.load('images/3.jpg')
    four = pygame.image.load('images/4.jpg')
    five = pygame.image.load('images/5.jpg')
    six = pygame.image.load('images/6.jpg')
    seven = pygame.image.load('images/7.jpg')
    eight = pygame.image.load('images/8.jpg')
    imagesDict = {'tile':tile, 'mine':mine, 'mineShow':mineShow, 'flag':flag, \
                         0:zero, 1:one, 2:two, 3:three, 4:four, 5:five, 6:six, 7:seven, 8:eight}
    flagSound = None
    unFlagSound = None
    explosionSound = None
    revealSound = None
    dingSound = None
    buzzSound = None

    def __init__(self, window, rowIndex, colIndex):
        self.window = window

        # Instance variables:
        self.value = None
        self.revealed = False
        self.flagged = False

        self.rowIndex = rowIndex
        self.colIndex = colIndex
        self.x = self.colIndex * CELL_WIDTH_HEIGHT
        self.y = self.rowIndex * CELL_WIDTH_HEIGHT
        #print('x and y', self.x, self.y)
        self.rect = pygame.Rect(self.x, self.y, CELL_WIDTH_HEIGHT, CELL_WIDTH_HEIGHT)
        self.images = pygwidgets.ImageCollection(window, (self.x, self.y), Cell.imagesDict, 'tile')
        if Cell.flagSound is None:
            Cell.flagSound = pygame.mixer.Sound('sounds/flag.wav')
        if Cell.unFlagSound is None:
            Cell.unFlagSound = pygame.mixer.Sound('sounds/unflag.wav')
        if Cell.explosionSound is None:
            Cell.explosionSound = pygame.mixer.Sound('sounds/explosion.wav')
        if Cell.revealSound is None:
            Cell.revealSound = pygame.mixer.Sound('sounds/reveal.wav')
        if Cell.buzzSound is None:
            Cell.buzzSound = pygame.mixer.Sound('sounds/buzz.wav')
        if Cell.dingSound is None:
            Cell.dingSound = pygame.mixer.Sound('sounds/ding.wav')

        self.neighborsList = []
        for offset in NEIGHBOR_OFFSETS:
            neighborRow = rowIndex + offset[0]
            neighborCol = colIndex + offset[1]
            if (neighborRow >= 0) and (neighborRow < N_ROWS) and \
                (neighborCol >= 0) and (neighborCol < N_COLS):
                # Valid neighbor
                self.neighborsList.append((neighborRow, neighborCol))

        self.reset()

    def reset(self):
        self.revealed = False
        self.flagged = False
        self.value = None
        self.images.replace('tile')

    def handleEvent(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        else:
            return False

    def getNeighbors(self):
        return self.neighborsList

    def handleClick(self, event, allowHelp):
        if self.revealed:
            return ALREADY_REVEALED  # already showing
        if event.button == 1: # Left mouse button
            #print('Hit cell', self.rowIndex, self.colIndex)
            if self.flagged:
                return ALREADY_REVEALED  # Must "unflag" before revealing
            self.revealed = True
            self.images.replace(self.value)
            if self.value == MINE:
                Cell.explosionSound.play()
                return GAME_OVER  # game is over
            Cell.revealSound.play()
            return REVEALED_CELL

        elif event.button == 3:  # Right mouse button
            self.flagged = not self.flagged
            if self.flagged:
                self.images.replace('flag')
                Cell.flagSound.play()
                # Used during development to test if flagged a mine correctly
                if allowHelp:
                    if self.value == MINE:
                        Cell.dingSound.play()
                    else:
                        Cell.buzzSound.play()

                return FLAGGED
            else:
                self.images.replace('tile')
                Cell.unFlagSound.play()
                return UNFLAGGED
        print('NOT SURE WHAT TO RETURN HERE')

    def getValue(self):
        return self.value

    def setValue(self, newValue):
        self.value = newValue

    def isRevealable(self):
        """Returns False if cell is already revealed, a mine or a flag, otherwise True to say revealable"""
        if self.revealed:
            return False
        if self.value in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            return True
        else:
            return False

    def isHidden(self):
        if self.revealed or self.flagged:
            return False
        else:
            return True


    def isEmpty(self):
        if self.value == 0:
            return True
        else:
            return False

    def reveal(self):
            self.revealed = True
            self.images.replace(self.value)

    def showIfMine(self, killer):
        if self.value == MINE:
            if killer:
                self.images.replace('mine')
            else:
                self.images.replace('mineShow')

    def draw(self):
        self.images.draw()

