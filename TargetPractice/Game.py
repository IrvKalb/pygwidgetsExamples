# Game Manager

import pygame
from Target import *
import time

N_TARGETS = 30
PLAYING = 'playing'
DONE = 'done'
N_SECONDS = 30


class Game():
    def __init__(self, window, windowWidth, windowHeight):
        self.window = window
        self.targetList = [ ]
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.nMissedTargets = 0
        self.nTargetsHit = 0
        self.nClicks = 0
        self.nMissedClicks = 0
        self.state = PLAYING
        self.shotSound = pygame.mixer.Sound('sounds/shot.wav')
        self.missSound = pygame.mixer.Sound('sounds/miss.wav')


    def reset(self):  # called when ready to play a round of the game
        self.nClicks = 0
        self.nTargetsHit = 0
        self.nMissedTargets = 0
        self.nMissedClicks = 0
        self.targetList = [ ]
        timeNow = time.perf_counter()
        for i in range(0, N_TARGETS):
            oTarget = Target(self.window, self.windowWidth, self.windowHeight, timeNow, N_SECONDS)
            self.targetList.insert(0, oTarget)  # add at the beginning of the list

        self.state = PLAYING

        #self.targetList.reverse()  # reverse list so newer targets appear on top

    def update(self):
        if self.state == DONE:
            return False, []  # ignore clicks after round is done
        theTime = time.perf_counter()
        for oTarget in self.targetList:
            missedTarget = oTarget.update(theTime)
            if missedTarget:  # time ran out without a click on this target
                self.nMissedTargets = self.nMissedTargets + 1

        if (self.nTargetsHit + self.nMissedTargets) == N_TARGETS:
            #print("Game over")
            #print('total clicks', self.nClicks)
            #print('hits', self.nTargetsHit)
            #print('misses', self.nMissedClicks)
            #print('missed targets', self.nMissedTargets)
            #print()

            xFactor = N_TARGETS - self.nClicks
            if xFactor < 0:
                xFactor = 0
            score = int(self.nTargetsHit / (xFactor + self.nClicks) * 100.)
            #print('Score is:', score)

            self.state = DONE

            # Build a list to send to the Score scene
            # [clicks, hits, misses, missedTargets, score]
            dataList = [self.nClicks, self.nTargetsHit, self.nMissedTargets, self.nMissedClicks, score]
            return True, dataList # meaning game play is over

        else:
            return False, []  # game is not over

    def handleClick(self, mouseLoc):
        if self.state == DONE:
            return  # ignore clicks after round is done
        self.nClicks = self.nClicks + 1
        for oTarget in self.targetList:
            hit = oTarget.handleClick(mouseLoc)
            if hit:
                self.nTargetsHit = self.nTargetsHit + 1
                self.shotSound.play()
                return  # only count the front-most target

        # Did not hit any target

        self.nMissedClicks = self.nMissedClicks + 1
        print('clicked, but did not hit a target, count is', self.nMissedClicks)
        self.missSound.play()


    def draw(self):
        for oTarget in self.targetList:
            oTarget.draw()
