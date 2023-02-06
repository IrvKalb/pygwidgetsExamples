#
# This is the Splash Scene
#
# This is where the player sees the intro screen
#

import pygwidgets
import pyghelpers
import pygame
from pygame.locals import *
from Constants import *


class SceneSplash(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        self.titleField = pygwidgets.DisplayText(window, (0, 140), 'SNAKE!', fontName=GAME_FONT, \
                                              fontSize=80, textColor=WHITE, width=WINDOW_WIDTH, justified='center')
        self.messageField = pygwidgets.DisplayText(window, (0, 260), '(Press any key to start)', fontName=GAME_FONT, \
                                              fontSize=18, textColor=WHITE, width=WINDOW_WIDTH, justified='center')

        self.pythonImage =   pygwidgets.Image(window, (270, 320), 'images/pythonLogo.png')

    def getSceneKey(self):
        return SCENE_SPLASH

    def enter(self, data):
        pass

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == pygame.KEYDOWN:
                self.goToScene(SCENE_PLAY)

    def update(self):
        pass

    def draw(self):
        self.window.fill(BLACK)
        self.titleField.draw()
        self.messageField.draw()
        self.pythonImage.draw()

    def leave(self):
        return None
