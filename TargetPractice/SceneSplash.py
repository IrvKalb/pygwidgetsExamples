#
# This the Splash Scene
#

import pygwidgets
import pyghelpers
from Constants import *


class SceneSplash(pyghelpers.Scene):
    def __init__(self, window):
        # Save window in instance variable
        self.window = window

        self.backgroundImage = pygwidgets.Image(self.window, (0, 0), "images/gridBG.png")
        self.dialogImage = pygwidgets.Image(self.window, (150, 30), "images/splash.jpg")

        self.startButton = pygwidgets.TextButton(self.window, (430, 380), 'Start')

    def getSceneKey(self):
        return SCENE_SPLASH

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.startButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)


    def draw(self):
        self.backgroundImage.draw()
        self.dialogImage.draw()
        self.startButton.draw()


