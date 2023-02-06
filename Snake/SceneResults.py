# The Results scene
# The player is shown the results of the current round

import pygwidgets
import pyghelpers
import pygame
import sys
from Constants import *

class SceneResults(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        self.thisGameScore = 0
        self.highScore = 0

        self.gameOver = pygwidgets.DisplayText(
                                self.window, (0, 100), 'GAME OVER',
                                fontSize=50, textColor=WHITE, width=WINDOW_WIDTH, justified='center')

        self.scoreLabel = pygwidgets.DisplayText(
                                window, (240, 200),'Your score:', fontName=GAME_FONT,
                                fontSize=24, textColor=WHITE, width=610)

        self.scoreDisplay = pygwidgets.DisplayText(
                                window, (390, 200),'', fontName=GAME_FONT,
                                fontSize=24, textColor=WHITE, width=20, justified='right')

        self.highLabel = pygwidgets.DisplayText(
                                window, (240, 280),'High Score:', fontName=GAME_FONT,
                                fontSize=24, textColor=WHITE, width=610)

        self.highDisplay = pygwidgets.DisplayText(
                                self.window, (390, 280), '0', fontName=GAME_FONT,
                                fontSize=24, textColor=WHITE,
                                width=20, justified='right')

        self.newHighScoreMsg = pygwidgets.DisplayText(
                                self.window, (450, 285), '(New high score!)',
                                fontSize=20, textColor=WHITE)

        self.messageField = pygwidgets.DisplayText(window, (0, 380), '(Press any key to play again)', fontName=GAME_FONT, \
                                              fontSize=20, textColor=WHITE, width=WINDOW_WIDTH, justified='center')

        self.quitButton = pygwidgets.TextButton(self.window, (520, 420), 'Quit')

        self.showHighScore = True


    def getSceneKey(self):
        return SCENE_RESULTS

    def enter(self, score):
        # score is just the score from the game that just ended

        self.thisGameScore = score
        if self.thisGameScore > self.highScore:
            self.showHighScoreMsg = True
            self.highScore = self.thisGameScore
        else:
            self.showHighScoreMsg = False

        self.scoreDisplay.setValue(self.thisGameScore)
        self.highDisplay.setValue(self.highScore)

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if event.type == pygame.KEYDOWN:  # or key
                self.goToScene(SCENE_PLAY)
            if self.quitButton.handleEvent(event):
                pygame.quit()
                sys.exit()

    # No need to include update method,
    # defaults to inherited one which does nothing.

    def draw(self):
        self.window.fill(BLACK)
        self.gameOver.draw()
        self.scoreLabel.draw()
        self.scoreDisplay.draw()
        self.highLabel.draw()
        self.highDisplay.draw()
        if self.showHighScoreMsg:
            self.newHighScoreMsg.draw()
        self.messageField.draw()
        self.quitButton.draw()
