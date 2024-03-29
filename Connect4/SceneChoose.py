# SCENE_CHOOSE
#
# User chooses between human vs human or human vs computer

import random
import copy
import sys
from Constants import *
import pygame
import pygwidgets
import pyghelpers

class SceneChoose(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        self.boxWithRules = pygwidgets.Image(window, (120, 30), 'images/boxWithRules.png')
        self.humanButton = pygwidgets.CustomButton(self.window, (140, 170),
                                                up='images/humanUp.png',
                                                over='images/humanOver.png',
                                                down='images/humanDown.png')
        self.computerButton = pygwidgets.CustomButton(self.window, (320, 170),
                                                up='images/computerUp.png',
                                                over='images/computerOver.png',
                                                down='images/computerDown.png')
        self.quitButton = pygwidgets.CustomButton(window, (242, 407),
                                                  up='images/quitUp.png',
                                                  over='images/quitOver.png',
                                                  down='images/quitDown.png')

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if self.quitButton.handleEvent(event):
                pygame.quit()
                sys.exit()
            elif self.humanButton.handleEvent(event):
                self.goToScene(SCENE_PLAY, HUMAN_VS_HUMAN)

            elif self.computerButton.handleEvent(event):
                self.goToScene(SCENE_PLAY, HUMAN_VS_COMPUTER)

    def draw(self):
        self.window.fill(BACKGROUND_COLOR)
        self.boxWithRules.draw()
        self.humanButton.draw()
        self.computerButton.draw()
        self.quitButton.draw()
