# Target Practice Score Scene


import pygame
import pygwidgets
import pyghelpers
from Constants import *
import sys


class SceneScore(pyghelpers.Scene):
    def __init__(self, window):
        # Save window in instance variables
        self.window = window

        self.backgroundImage = pygwidgets.Image(self.window, (0, 0), "images/gridBG.png")
        self.dialogImage = pygwidgets.Image(self.window, (150, 30), "images/score.jpg")

        self.quitButton = pygwidgets.TextButton(self.window, (270, 420), 'Quit')
        self.restartButton = pygwidgets.TextButton(self.window, (570, 420), 'Restart')

        self.clicksField = pygwidgets.DisplayText(self.window, (500, 223), '', fontSize=30)
        self.hitsField = pygwidgets.DisplayText(self.window, (500, 250), '', fontSize=30)
        self.missesField = pygwidgets.DisplayText(self.window, (500, 278), '', fontSize=30)
        self.missedTargetsField = pygwidgets.DisplayText(self.window, (500, 306), '', fontSize=30)
        self.scoreField = pygwidgets.DisplayText(self.window, (500, 362), '', fontSize=30)

    def getSceneKey(self):
        return SCENE_SCORE

    def enter(self, data):
        # Expects a list of
        # [clicks, hits, misses, missedTargets, score]
        self.clicksField.setValue(str(data[0]))
        self.hitsField.setValue(str(data[1]))
        self.missesField.setValue(str(data[2]))
        self.missedTargetsField.setValue(str(data[3]))
        self.scoreField.setValue(str(data[4]))



    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.quitButton.handleEvent(event):
                pygame.quit()
                sys.exit()

            if self.restartButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)


    def draw(self):
        self.backgroundImage.draw()
        self.dialogImage.draw()

        self.clicksField.draw()
        self.hitsField.draw()
        self.missesField.draw()
        self.missedTargetsField.draw()
        self.scoreField.draw()

        self.quitButton.draw()
        self.restartButton.draw()



