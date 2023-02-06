import sys
import pygame
import pyghelpers
from Constants import *
from Snake import *
from Apple import *
import pygwidgets

class ScenePlay(pyghelpers.Scene):

    def __init__(self, window, ):
        self.window = window
        self.oApple = Apple(self.window)
        self.oSnake = Snake(self.window, self.oApple)
        self.loseSound = pygame.mixer.Sound('sounds/lose.wav')

        # Build the grid to display as the background
        self.grid = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.Surface.fill(self.grid, BLACK)
        for x in range(0, WINDOW_WIDTH, CELLSIZE):  # draw vertical lines
            pygame.draw.line(self.grid, DARKGRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELLSIZE):  # draw horizontal lines
            pygame.draw.line(self.grid, DARKGRAY, (0, y), (WINDOW_WIDTH, y))

        self.gameTitle = pygwidgets.DisplayText(self.window, (300, 300), 'SNAKE!', textColor=WHITE,
                                                fontSize=50, fontName=GAME_FONT)
        self.scoreTitle = pygwidgets.DisplayText(self.window, (450, 10), 'Score', textColor=WHITE)
        self.scoreDisplay = pygwidgets.DisplayText(self.window, (490, 10), '', textColor=WHITE, justified='right')
        self.gameOver = pygwidgets.DisplayText(self.window, (300, 300), 'GAME OVER!', textColor=WHITE,
                                               fontSize=50, fontName=GAME_FONT)


    def getSceneKey(self):
        return SCENE_PLAY

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            self.oSnake.handleEvent(event)

    def update(self):
        self.oSnake.update()
        gameStatus = self.oSnake.checkGameOver()
        if gameStatus == GAME_OVER:
            score = self.oSnake.getScore()  # get the score before transitioning to results scene
            self.loseSound.play()
            self.oSnake.reset()
            time.sleep(.5)
            # Eliminate any events (especially keyboard key events) that may have happened
            throwAway = pygame.event.get()
            self.goToScene(SCENE_RESULTS, score)

    def draw(self):
        pygame.Surface.blit(self.window, self.grid, (0, 0))  # Draw the grid

        self.oSnake.draw()
        self.oApple.draw()
        self.scoreTitle.draw()
        score = self.oSnake.getScore()
        self.scoreDisplay.setValue(score)
        self.scoreDisplay.draw()






