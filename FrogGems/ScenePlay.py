#
# This is the Play Scene
#

import pygwidgets
import pyghelpers
import pygame
import sys
from Constants import *
from Player import *
from Grid import *
from Bug import *


class ScenePlay(pyghelpers.Scene):  # Inherits from the Scene class in the SceneMgr file
    NBUGS = 4
    STATE_PLAYING = 'state playing'
    STATE_ROUND_OVER = 'state round over'

    def __init__(self, window):
        '''
        This method is called when the scene is created
        Create and/or load any assets (images, buttons, sounds)
        that you need for this scene
        :param window:
        '''
        # Save window in instance variable
        self.window = window

        # 4 - Load assets: image(s), sounds,  etc.
        self.oGrid = Grid(window)
        self.oPlayer = Player(window)
        self.oBackground = pygwidgets.Image(window, (0, 0), 'images/background.jpg')
        self.oLevelDisplay = pygwidgets.DisplayText(window, (20, 15), '', fontSize=28)
        self.oLivesDisplay = pygwidgets.DisplayText(window, (120, 15), '', fontSize=28)
        self.oScoreDisplay = pygwidgets.DisplayText(window, (220, 15), '', fontSize=28)
        self.oBonusDisplay = pygwidgets.DisplayText(window, (350, 15), '', fontSize=28, textColor=(0, 153, 0))

        self.dingSound = pygame.mixer.Sound('sounds/ding.wav')
        self.winSound = pygame.mixer.Sound('sounds/win.wav')
        self.upSound = pygame.mixer.Sound('sounds/plus.wav')
        self.downSound = pygame.mixer.Sound('sounds/minus.wav')
        self.bonusSound = pygame.mixer.Sound('sounds/bonus.wav')
        self.splatSound = pygame.mixer.Sound('sounds/splat.wav')
        self.loseSound = pygame.mixer.Sound('sounds/lose.wav')
        self.state = ScenePlay.STATE_PLAYING
        self.oTimer = pyghelpers.Timer(.75, callBack=self.startNextRound) # wait 3/5 sec between rounds

        self.reset()


    def reset(self):
        self.nLives = 3
        self.level = 1
        self.score = 0
        self.oPlayer.newRound(self.level)


        self.bugList = []
        for i in range(0, ScenePlay.NBUGS):
            oBug = Bug(self.window, i)
            self.bugList.append(oBug)
        self.state = ScenePlay.STATE_PLAYING

    def getSceneKey(self):
        return SCENE_PLAY

    def enter(self, data):
        '''
        This method is called whenever the scene changes to this scene.
        'data' is a any information that is passed from the previous scene
        Typical use is to pass in a dictionary, from which useful data can be extracted.

        :param data:
        :return:
        '''
        pass

    def handleInputs(self, events, keyPressedList):
        '''
        This method is called on every frame when an event happens
        It is passed in a list of events and a list of keyboard keys that are down
        Typical code is to loop through the events and handle any that you want to
        :param self:
        :param events:
        :param keyPressedList:
        :return:
        '''
        if self.state == ScenePlay.STATE_PLAYING:
            for event in events:
                self.oPlayer.handleEvent(event)  # handle keyboard keys to move player

    def startNextRound(self, nickname):
        #self.level = self.level + 1
        print('In startNextRound, new level is:', self.level)

        self.oPlayer.newRound(self.level)
        self.oGrid.newRound(self.level)
        for oBug in self.bugList:
            oBug.setSpeed(self.level)
            oBug.resetLoc()
        self.state = ScenePlay.STATE_PLAYING
        self.oBonusDisplay.setValue('')

    def update(self):
        '''
        This method is called once per frame while the scene is active
        Include in here, any code you want to execute every frame
        :param self:
        :return:
        '''
        if self.nLives == 0:  # End game
            self.loseSound.play()
            answer = pyghelpers.textYesNoDialog(self.window, (100, 100, 300, 200), 'Game Over\n\nPlay Again?', \
                                            trueButtonText='Yes', falseButtonText='No')
            if answer:
                self.reset()
                return
            else:
                pygame.quit()
                sys.exit(0)

        self.oTimer.update()
        if self.state == ScenePlay.STATE_PLAYING:
            playerRow, playerCol = self.oPlayer.getRowCol()
            if playerRow == 0:  # won the round

                self.winSound.play()
                self.state = ScenePlay.STATE_ROUND_OVER
                #print('Won the round, starting timer')
                self.level = self.level + 1
                self.oTimer.start()


            else:
                item = self.oGrid.getItem(playerRow, playerCol)
                if item != NOTHING:  # found gem
                    if item == HEART:
                        self.nLives = self.nLives + 1
                        self.dingSound.play()
                    elif item == BLACK_GEM:
                        self.downSound.play()
                        self.score = self.score - 2
                    elif item in (BLUE_GEM, ORANGE_GEM, GREEN_GEM):
                        self.upSound.play()
                        if item == BLUE_GEM:
                            self.score = self.score + 2
                        elif item == ORANGE_GEM:
                            self.score = self.score + 5
                        elif item == GREEN_GEM:
                            self.score = self.score + 10


                    # clear the item, and see if all are gone.  If so, give bonus.
                    allGone = self.oGrid.clearItem(playerRow, playerCol)
                    if allGone:
                        self.bonusSound.play()
                        self.score = self.score + self.level
                        self.oBonusDisplay.setValue('Bonus: ' + str(self.level))

            playerRect = self.oPlayer.getRect()

            # 8  Do any "per frame" actions
            for oBug in self.bugList:
                oBug.update()
                bugRect = oBug.getRect()
                if playerRect.colliderect(bugRect):
                    self.nLives = self.nLives - 1
                    self.splatSound.play()
                    self.oPlayer.showDead()
                    if self.nLives > 0:
                        #self.oPlayer.newRound(self.level)
                        #self.oGrid.newRound(self.level)
                        self.state = ScenePlay.STATE_ROUND_OVER
                        #print('Lost the round, starting timer')
                        self.oTimer.start()


            self.oLivesDisplay.setValue('Lives: ' + str(self.nLives))
            self.oLevelDisplay.setValue('Level: ' + str(self.level))
            self.oScoreDisplay.setValue('Score: ' + str(self.score))

    def draw(self):
        '''
        This method is called on every frame
        Include any code that you need to draw everything in the window
        (Typical is to do a window fill or blit a background picture,
        and draw buttons, fields, characters, etc.)
        :param self:
        :return:
        '''
        self.oBackground.draw()
        self.oGrid.draw()
        self.oPlayer.draw()
        for oBug in self.bugList:
            oBug.draw()

        self.oLevelDisplay.draw()
        self.oLivesDisplay.draw()
        self.oScoreDisplay.draw()
        self.oBonusDisplay.draw()

    def leave(self):
        '''
        This method is called once when your code has asked to move on to a new scene
        It should return any data that this scene wants to pass on to the next scene
        The typical data is either None or a dictionary.
        :param self:
        :return:
        '''
        return None
