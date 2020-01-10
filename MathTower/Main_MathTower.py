#  2/17 by Irv Kalb
#

import pygame
import random
import sys
import pygwidgets
from pygame.locals import *
import time


COMPUTER_TURN = USEREVENT + 1
HUMAN_TURN = USEREVENT + 2

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
FRAMES_PER_SECOND = 30
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (0, 222, 222)

MAX_BLOCKS = 16

COMPUTER = 'computer'
HUMAN = 'human'
NEITHER = 'neither'



### MAIN CODE ###

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Math Tower')
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Game:
    def __init__(self, window):
        self.window = window
        self.blockImage = pygame.image.load('images/oneBlock.png')
        self.line = pygame.image.load('images/line.png')
        self.lowestY = 490
        self.blockHeight = 30
        self.towerX = 220
        self.computerWins = 0
        self.humanWins = 0
        self.lineBottomY = self.lowestY + self.blockHeight
        self.lineTopY = self.lowestY - ((MAX_BLOCKS - 1) * self.blockHeight) - 3
        self.newGameButton = pygwidgets.TextButton(window, (360, 460), 'New Game', width=100, height=35)
        self.quitButton = pygwidgets.TextButton(window, (360, 400), 'Quit', width=100, height=35)

        self.oneBlockButton = pygwidgets.CustomButton(window, (35, 230), up='images/oneBlock.png',\
                                                      over='images/OneBlockOver.png',\
                                                      down='images/OneBlockDown.png',\
                                                      disabled='images/OneBlockDisabled.png')
        self.twoBlocksButton = pygwidgets.CustomButton(window, (35, 300), up='images/twoBlocks.png', \
                                                       over='images/TwoBlocksOver.png', \
                                                       down='images/TwoBlocksDown.png', \
                                                       disabled='images/TwoBlocksDisabled.png')
        self.threeBlocksButton = pygwidgets.CustomButton(window, (35, 400), up='images/threeBlocks.png', \
                                                         over='images/ThreeBlocksOver.png', \
                                                         down='images/ThreeBlocksDown.png', \
                                                         disabled='images/ThreeBlocksDisabled.png')
        self.nBlocksDisplay = pygwidgets.DisplayText(window, (self.towerX, 530), '0 of ' + str(MAX_BLOCKS), \
                                               fontName='monospaces', fontSize=24, textColor=BLACK)
        self.messageDisplay = pygwidgets.DisplayText(window, (10, 572), '', \
                                                       fontName='monospaces', fontSize=28, textColor=BLACK)
        self.humanWinsDisplay = pygwidgets.DisplayText(window, (360, 230), 'Player:     0', \
                                               fontName='monospaces', fontSize=28, textColor=BLACK)
        self.computerWinsDisplay = pygwidgets.DisplayText(window, (360, 300), 'Computer: 0', \
                                               fontName='monospaces', fontSize=28, textColor=BLACK)
        self.humanBlip = pygame.mixer.Sound('sounds/humanBlip.wav')
        self.computerBlip = pygame.mixer.Sound('sounds/computerBlip.wav')
        self.applause = pygame.mixer.Sound('sounds/applause.wav')
        self.ding = pygame.mixer.Sound('sounds/ding.wav')



        self.reset()

    def reset(self):
        self.nBlocks = 0
        self.oneBlockButton.enable()
        self.twoBlocksButton.enable()
        self.threeBlocksButton.enable()
        zeroOrOne = random.randrange(0, 2)
        if zeroOrOne == 0:
            self.whoseTurn = HUMAN
        else:
            self.whoseTurn = COMPUTER
        self.gameOver = False
        self.messageDisplay.setValue('Choose 1, 2, or 3 blocks.  Take last block to win.')
        #self.animatingComputerMove = False

    def play(self, event):
        if  self.newGameButton.handleEvent(event):
            oGame.reset()
        madeMove = False

        if  self.quitButton.handleEvent(event):
            pygame.quit()
            sys.exit()

        if self.whoseTurn == HUMAN:
            if  self.oneBlockButton.handleEvent(event):
                self.gameOver = self.humanChoice(1)
                nBlocks = 1
                madeMove = True
                
            if  self.twoBlocksButton.handleEvent(event):
                self.gameOver = self.humanChoice(2)
                nBlocks = 2
                madeMove = True
                
            if  self.threeBlocksButton.handleEvent(event):
                self.gameOver = self.humanChoice(3)
                nBlocks = 3
                madeMove = True
                
            if madeMove:
                self.messageDisplay.setValue('You chose: ' + str(nBlocks))
                if self.gameOver:
                    self.humanWins = self.humanWins + 1
                    self.humanWinsDisplay.setValue('Player:     ' + str(self.humanWins))
                    self.messageDisplay.setValue('Game is over - player wins')
                    self.applause.play()
                    self.whoseTurn = NEITHER
                else:
                    self.whoseTurn = COMPUTER
                self.disableButtons()

        elif self.whoseTurn == COMPUTER:
            time.sleep(1)
            self.gameOver = self.computerChoice()
            if self.gameOver:
                self.computerWins = self.computerWins + 1
                self.computerWinsDisplay.setValue('Computer: ' + str(self.computerWins))
                self.messageDisplay.setValue('Game is over - computer wins')
                self.ding.play()
                self.whoseTurn = NEITHER
            else:
                self.whoseTurn = HUMAN
            self.disableButtons()

        self.nBlocksDisplay.setValue(str(self.nBlocks) + ' of ' + str(MAX_BLOCKS))

    def disableButtons(self):
        nBlocksLeft = MAX_BLOCKS - self.nBlocks
        if nBlocksLeft < 3:
            self.threeBlocksButton.disable()
        if nBlocksLeft < 2:
            self.twoBlocksButton.disable()
        if nBlocksLeft < 1:
            self.oneBlockButton.disable()


    def humanChoice(self, howManyBlocks):
        self.humanBlip.play()
        self.nBlocks = self.nBlocks + howManyBlocks
        if self.nBlocks == MAX_BLOCKS:
            return True
        else:
            return False

    def computerChoice(self):
        self.computerBlip.play()
        nRemaining = MAX_BLOCKS - self.nBlocks
        if nRemaining <= 3:
            howManyBlocks = nRemaining
            done = True
        else:
            howManyBlocks = random.randrange(1, 4)
            done= False

        self.nBlocks = self.nBlocks + howManyBlocks
        self.messageDisplay.setValue('Computer chooses: ' + str(howManyBlocks))

        return done


    def draw(self):
        self.window.blit(self.line, (self.towerX - 10, self.lineBottomY))
        self.window.blit(self.line, (self.towerX - 10, self.lineTopY))

        for i  in range(self.nBlocks):
            thisY = self.lowestY - (i * self.blockHeight)
            self.window.blit(self.blockImage, (self.towerX, thisY))

        # Draw  buttons
        self.oneBlockButton.draw()
        self.twoBlocksButton.draw()
        self.threeBlocksButton.draw()
        self.newGameButton.draw()
        self.quitButton.draw()
        self.nBlocksDisplay.draw()

        self.messageDisplay.draw()
        self.humanWinsDisplay.draw()
        self.computerWinsDisplay.draw()


# Main code
oGame = Game(window)


while True:
    # Handle events
    for event in pygame.event.get():
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()


#        if event.type == COMPUTER_TURN:
#            pygame.time.set_timer(COMPUTER_TURN, 0)   # Kill the timer
#            oGame.mMakeComputerMove()


    oGame.play(event)   # give the game time to do anything it may need to do.

    # Draw everything
    window.fill(BACKGROUND_COLOR)

    # Draw the game
    oGame.draw()


    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)
