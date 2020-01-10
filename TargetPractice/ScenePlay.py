# Target Practice Play Scene

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import pygwidgets
import pyghelpers
from Game import *
from Constants import *


class ScenePlay(pyghelpers.Scene):
    def __init__(self, window, sceneKey):
        self.window = window
        self.sceneKey = sceneKey
        self.backgroundImage = pygwidgets.Image(self.window, (0, 0), "images/gridBG.png")
        self.oGame = Game(window, WINDOW_WIDTH, WINDOW_HEIGHT)

    def enter(self, data):
        self.oGame.reset()


    def handleInputs(self, events, keyPressedList):

        for event in events:

            # If the event was a click on the close box, quit pygame and the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # See if user clicked
            if event.type == MOUSEBUTTONDOWN:
                self.oGame.handleClick(event.pos)

    def update(self):
        gameOver, data = self.oGame.update()
        if gameOver:
            self.goToScene(SCENE_SCORE, data)

    def draw(self):
        self.backgroundImage.draw()
        self.oGame.draw()







