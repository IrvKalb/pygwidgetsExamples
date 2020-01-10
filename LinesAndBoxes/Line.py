import pygame
from Constants import *

class Line(object):

    def __init__(self, window, HorV, lineNumber, x, y, width, height, borderSquaresList):
        self.window = window

        self.imageAvailable = pygame.image.load('images/line' + HorV + '.png')
        self.imageOver = pygame.image.load('images/line' + HorV + 'Over.png')
        self.imageSelect = pygame.image.load('images/line' + HorV + 'Select.png')
        self.imageTaken = pygame.image.load('images/line' + HorV + 'Taken.png')

        self.lineNumber = lineNumber
        self.loc = (x, y)
        self.rect = pygame.Rect(x, y, width, height)
        self.borderSquaresList = borderSquaresList
        self.mReset()


    def mReset(self):
        self.taken = False
        self.rolledOver = False
        self.image =  self.imageAvailable
        self.availableForHuman = True



    def mCheckForRollover(self, mousePos):
        if self.taken:
            return None

        if not self.availableForHuman:  # Computer's turn
            return None

        if self.rect.collidepoint(mousePos):
            if not self.rolledOver:
                self.rolledOver = True
                self.image = self.imageOver
            return self.lineNumber

        else:   # not rolled over
            if self.rolledOver:
                self.rolledOver = False
                self.image = self.imageAvailable
            return None

    def draw(self):
        self.window.blit(self.image, self.loc)


    def mSelect(self, humanOrComputer):

        self.taken = True

        self.image = self.imageTaken  # For now, just show the taken image

        return self.borderSquaresList

    def mAnimate(self, normalOrSelect):
        if normalOrSelect == NORMAL:
            self.image = self.imageTaken
        else:
            self.image = self.imageSelect


    def mGetTaken(self):
        return self.taken

    def mGetLineNumber(self):
        return self.lineNumber

    def mSetAvailableForHuman(self, TrueOrFalse):
        self.availableForHuman = TrueOrFalse



