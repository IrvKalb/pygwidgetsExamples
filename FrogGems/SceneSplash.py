#
# This is the Splash Scene
#

import pygwidgets
import pyghelpers
from Constants import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 200)

class SceneSplash(pyghelpers.Scene):
    def __init__(self, window, sceneKey):
        # Save window and sceneKey in instance variables
        self.window = window
        self.sceneKey = sceneKey

        #self.backgroundImage = pygwidgets.Image(self.window, (0, 0), "images/splashBackground.jpg")
        #self.frogGemsImage = pygwidgets.Image(self.window, (150, 30), "images/fromGems.png")

        
        self.startButton = pygwidgets.CustomButton(self.window, (250, 500), \
                                                   up='images/startNormal.png',\
                                                   down='images/startDown.png',\
                                                   over='images/startOver.png',\
                                                   disabled='images/startDisabled.png',\
                                                   enterToActivate=True)

        self.quitButton = pygwidgets.CustomButton(self.window, (30, 650), \
                                                   up='images/quitNormal.png',\
                                                   down='images/quitDown.png',\
                                                   over='images/quitOver.png',\
                                                   disabled='images/quitDisabled.png')

        self.highScoresButton = pygwidgets.CustomButton(self.window, (360, 650), \
                                                   up='images/gotoHighScoresNormal.png',\
                                                   down='images/gotoHighScoresDown.png',\
                                                   over='images/gotoHighScoresOver.png',\
                                                   disabled='images/gotoHighScoresDisabled.png')
        self.intro = pygwidgets.DisplayText(self.window, (30, 30), \
                                            'Welcome to FrogGems\n\n\n' + \
                                            'The object is to get to the water while\n' + \
                                            'collecting as many gems as you can, \n' + \
                                            'without getting squashed.\n\n' + \
                                            'If you grab all the gems on any screen,\n' + \
                                            'you get a bonus equal to the level number.\n\n'+ \
                                            'Every heart gives you an extra life.\n\n' + \
                                            'Good luck!', textColor=WHITE, fontSize=24, fontName='Arial')


    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.startButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)

            elif self.quitButton.handleEvent(event):
                self.quit()

            elif self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

    def draw(self):
        #self.backgroundImage.draw()
        self.window.fill(BLUE)
        self.startButton.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.intro.draw()


