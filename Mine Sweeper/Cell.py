# Cell class

import pygame
import pygwidgets
from Constants import *

class Cell():
    tile = pygame.image.load('images/tile.jpg')
    mine = pygame.image.load('images/mine.jpg')
    mineExploded = pygame.image.load('images/mineExploded.jpg')
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
    imagesDict = {'tile':tile, 'mine':mine, 'mineExploded':mineExploded, 'flag':flag,
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

    def clickedInside(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

    def getNeighbors(self):
        return self.neighborsList

    def handleClick(self, leftOrRightClick, debug):
        if debug:  # Debugging, check if the cell is a mine
            if self.value == MINE:
                Cell.dingSound.play()
            else:
                Cell.buzzSound.play()
            return  None # End debugging

        if self.revealed:
            return None # already showing
        if leftOrRightClick == LEFT_CLICK: # Left mouse button
            #print('Hit cell', self.rowIndex, self.colIndex)
            if self.flagged:
                return None  # Must "unflag" before revealing

            self.revealed = True
            self.images.replace(self.value)

            if self.value == MINE:
                return HIT_MINE  # game is over
            Cell.revealSound.play()
            return REVEALED_CELL

        elif leftOrRightClick == RIGHT_CLICK:  # Right mouse button
            self.flagged = not self.flagged
            if self.flagged:
                self.images.replace('flag')
                Cell.flagSound.play()
                # Used during development to test if flagged a mine correctly

            else:
                self.images.replace('tile')
                Cell.unFlagSound.play()
                self.revealed = False
                return None

    def getValue(self):
        return self.value

    def setValue(self, newValue):
        self.value = newValue

    def isRevealable(self):
        """Returns False if cell is already revealed, a mine or a flag, otherwise True to say revealable"""
        if self.revealed or self.flagged:
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

    def __str__(self):
        output = 'Cell ' + str(self.rowIndex) + ', ' + str(self.colIndex) + '\n' + \
                        '    self.value ' + str(self.value) + '\n' + \
                        '    self.flagged ' + str(self.flagged) + '\n' + \
                        '    self.revealed ' + str(self.revealed) + '\n'
        return output

    def reveal(self):
            self.revealed = True
            self.flagged = False
            self.images.replace(self.value)

    def showIfMine(self, mineType):
        if self.value == MINE:
            if mineType == UNEXPLODED:
                self.images.replace('mine')
            else:
                self.images.replace('mineExploded')

    def isFlagged(self):
        return self.flagged

    def draw(self):
        self.images.draw()

