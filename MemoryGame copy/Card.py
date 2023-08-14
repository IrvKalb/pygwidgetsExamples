#  Card Class

import pygame
from pygame.locals import *
import pygwidgets

### CARD
class Card():
    WIDTH = 54
    HEIGHT = 54

    def __init__(self, window, locX, locY):
        self.window = window
        self.locTuple = (locX, locY)
        self.rect = pygame.Rect(locX, locY, Card.WIDTH, Card.HEIGHT)
        cardBackPath = 'images/cardBack.png'
        self.oBackImage = pygwidgets.Image(self.window, self.locTuple, cardBackPath)

    def reset(self, value):
        self.cardValue = value
        cardPath = 'images/card' + str(self.cardValue) + '.png'
        self.oFrontImage = pygwidgets.Image(self.window, self.locTuple, cardPath)
        self.hide()

    def hide(self):
        self.showing = False

    def show(self):
        self.showing = True

    def draw(self):
        if self.showing:
            self.oFrontImage.draw()
        else:
            self.oBackImage.draw()

    def wasClicked(self, mouseX, mouseY):
        if self.showing:
            return False   #  if already matched (showing), ignore click

        if self.rect.collidepoint(mouseX, mouseY):
            return True
        else:
            return False

    def getValue(self):
        return self.cardValue

