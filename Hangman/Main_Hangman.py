#  Hangman Game by Irv Kalb  1/17

import pygame
from pygame.locals import *
import sys
import random
import pygwidgets


# CONSTANTS
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FRAMES_PER_SECOND = 30


### ANSWER LETTER
class AnswerLetter():
    WIDTH = 60
    def __init__(self, window, loc, letterWidth, letterHeight, letter, notMatchedImage, font):
        self.window = window
        self.loc = loc
        self.letter = letter
        self.notMatchedImage = notMatchedImage
        self.font = font
        self.matched = False


        # create the surface to show
        self.matchedImage = pygame.Surface((letterWidth, letterHeight))
        self.matchedImage.fill(GREEN)
        pygame.draw.rect(self.matchedImage, BLACK, (0, 0, letterWidth, letterHeight), 1)


        # create the caption text for up states of  (to get the size)
        captionSurface = self.font.render(letter, True, BLACK)
        captionRect = captionSurface.get_rect()
        captionRect.center = (int(letterWidth / 2), int(letterHeight / 2))

        # draw caption on the surface
        self.matchedImage.blit(captionSurface, captionRect)

    def match(self, letterPressed):
        if letterPressed == self.letter:
            self.matched = True
            return True
        else:
            return False

    def setMatched(self):
        self.matched = True

    def hasLetterBeenMatched(self):
        return self.matched

    def draw(self):
        if self.matched:
            self.window.blit(self.matchedImage, self.loc)
        else:
            self.window.blit(self.notMatchedImage, self.loc)


### ANSWER MANAGER
class AnswerLetterMgr():
    WIDTH = 70
    HEIGHT = 70
    SPACING = 90
    LEFT = 50
    TOP = 420
    def __init__(self, window):
        self.window = window

        # Build a blank square for showing
        self.notMatchedYet = pygame.Surface((AnswerLetterMgr.WIDTH, AnswerLetterMgr.HEIGHT))
        self.notMatchedYet.fill(RED)
        pygame.draw.rect(self.notMatchedYet, BLACK, (0, 0, AnswerLetterMgr.WIDTH, AnswerLetterMgr.HEIGHT), 1)
        pygame.draw.line(self.notMatchedYet, BLACK, (10, 55), (AnswerLetterMgr.WIDTH - 10, 55))  # Blank line

        self.font = pygame.font.Font(None, 48)  # want to try ('monospaces', 36)

    def reset(self, answer):
        self.answer = answer
        self.nLetters = len(self.answer)
        self.answerLetterList = []
        sizeOfAnswerDisplay = AnswerLetterMgr.SPACING * self.nLetters
        left = (WINDOW_WIDTH - sizeOfAnswerDisplay) / 2
        for letter in self.answer:
            thisLoc = (left, AnswerLetterMgr.TOP)
            oAnswerLetter = AnswerLetter(window, thisLoc, AnswerLetterMgr.WIDTH, AnswerLetterMgr.HEIGHT, \
                                         letter, self.notMatchedYet, self.font)
            self.answerLetterList.append(oAnswerLetter)
            left = left + AnswerLetterMgr.SPACING

    def match(self, letter):
        matched = False
        for oAnswerLetter in self.answerLetterList:
            thisLetterMatched = oAnswerLetter.match(letter)
            if thisLetterMatched:
                matched = True
        return matched

    def userFoundAllLetters(self):
        for oAnswerLetter in self.answerLetterList:
            if not oAnswerLetter.hasLetterBeenMatched():
                return False

        return True

    def show(self):
        for oAnswerLetter in self.answerLetterList:
            oAnswerLetter.setMatched()

    def draw(self):
        for oAnswerLetter in self.answerLetterList:
            oAnswerLetter.draw()


### CHOOSE LETTER
class ChooseLetter():
    def __init__(self, window, myLetter, theLeft, theTop, theWidth, theHeight):
        self.window = window
        self.myLetter = myLetter
        self.loc = (theLeft, theTop)
        self.myRect = pygame.Rect(theLeft, theTop, theWidth, theHeight)
        self.oButton = pygwidgets.TextButton(window, self.loc, self.myLetter, width=theWidth, height=theHeight, fontSize=24)
        self.reset()

    def reset(self):
        self.available = True
        self.oButton.enable()

    def wasClicked(self, event):
        if  self.oButton.handleEvent(event):
            self.oButton.disable()  # Disable the button after choosing a letter
            return self.myLetter
        else:
            return None

    def disable(self):
        self.oButton.disable()

    def draw(self):
        self.oButton.draw()

### CHOOSE LETTER MGR
class ChooseLetterMgr():
    LETTER1_Y = 600
    LETTER2_Y = 670
    LETTER_X = 110
    LETTER_SPACING = 62
    LETTER_WIDTH = 50
    LETTER_HEIGHT = 50

    def __init__(self, window):
        self.window = window
        # Split alphabet in half so we can have two rows of buttons
        alphabet1 = 'abcdefghijklm'
        alphabet2 = 'nopqrstuvwxyz'

        self.chooseLetterList = []
        left = ChooseLetterMgr.LETTER_X
        for letter in alphabet1:
            oLetter = ChooseLetter(self.window, letter, \
                                   left, ChooseLetterMgr.LETTER1_Y, \
                                   ChooseLetterMgr.LETTER_WIDTH, ChooseLetterMgr.LETTER_HEIGHT)
            self.chooseLetterList.append(oLetter)
            left = left + ChooseLetterMgr.LETTER_SPACING

        left = ChooseLetterMgr.LETTER_X
        for letter in alphabet2:
            oLetter = ChooseLetter(self.window, letter, \
                                   left, ChooseLetterMgr.LETTER2_Y, \
                                   ChooseLetterMgr.LETTER_WIDTH, ChooseLetterMgr.LETTER_HEIGHT)
            self.chooseLetterList.append(oLetter)
            left = left + ChooseLetterMgr.LETTER_SPACING

    def reset(self):
        for oLetter in self.chooseLetterList:
            oLetter.reset()

    def checkLetters(self, event):
        for oLetter in self.chooseLetterList:
            letterOrNone = oLetter.wasClicked(event)
            if letterOrNone != None:
                return letterOrNone

        return None  # no letter was clicked on

    def disableAll(self):
        for chooseLetter in self.chooseLetterList:
            chooseLetter.disable()

    def draw(self):
        for chooseLetter in self.chooseLetterList:
            chooseLetter.draw()


### GAME MANAGER
class GameMgr():
    MAX_GUESSES = 6
    def __init__(self, window):
        self.window = window
        self.wordList = ['anteater', 'beaver', 'cat', 'deer', 'eagle', 'fieldmouse', 'giraffe', 'horse']
        self.nWords = len(self.wordList)

        self.oAnswerLetterMgr = AnswerLetterMgr(window)
        self.oChooseLetterMgr = ChooseLetterMgr(window)

        # Load up pictures of the hanging man
        self.manImageList = []
        for number in range(GameMgr.MAX_GUESSES + 1):
            thisImage = pygame.image.load('images/man' + str(number) + '.png')
            self.manImageList.append(thisImage)
        self.manLoc = (480, 164)

        self.reset() # set up for first game

    def reset(self):
        self.nGuesses = 0
        self.answer = random.choice(self.wordList)
        self.oChooseLetterMgr.reset()
        self.oAnswerLetterMgr.reset(self.answer)
        print('Answer is', self.answer)   #  FOR DEVELOPMENT


    def checkLetters(self, event):
        letterOrNone = self.oChooseLetterMgr.checkLetters(event)
        if letterOrNone !=None:
            matchedAtLeastOne = self.oAnswerLetterMgr.match(letterOrNone)
            if matchedAtLeastOne:
                dingSound.play()
                if self.oAnswerLetterMgr.userFoundAllLetters():
                    applauseSound.play()
                    self.oChooseLetterMgr.disableAll()

            else:
                buzzSound.play()
                self.nGuesses = self.nGuesses + 1
                if self.nGuesses == GameMgr.MAX_GUESSES:
                    self.oChooseLetterMgr.disableAll()
                    self.oAnswerLetterMgr.show()  # show the correct answer
                    doneSound.play()

    def draw(self):
        self.oChooseLetterMgr.draw()
        self.oAnswerLetterMgr.draw()
        manImage = self.manImageList[self.nGuesses]
        self.window.blit(manImage, self.manLoc)



# Initialization Code
pygame.font.init()
pygame.init()
window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

oGameMgr = GameMgr(window)

clock = pygame.time.Clock()  # set the speed (frames per second)

# Load images and sounds
background = pygame.image.load("images/background.png")
applauseSound = pygame.mixer.Sound('sounds/applause.wav')
buzzSound = pygame.mixer.Sound('sounds/buzz.wav')
dingSound = pygame.mixer.Sound('sounds/ding.wav')
doneSound = pygame.mixer.Sound('sounds/done.wav')
newGameButton = pygwidgets.CustomButton(window, (475, 750),\
                up='images/newGame.png', over='images/newGameOver.png', down='images/newGameDown.png')


### MAIN LOOP
while True:

    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            sys.exit()

        if  newGameButton.handleEvent(event):
             oGameMgr.reset()

        letterClicked = oGameMgr.checkLetters(event)


    # Draw everything
    window.blit(background, (0, 0))
    oGameMgr.draw()
    newGameButton.draw()
       
    # update the window
    pygame.display.update()

    # slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make PyGame wait the correct amount
