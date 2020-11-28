# Bug class

from Constants import *
import pygwidgets
import random

MOVE_LR = 'Left to Right'
MOVE_RL = 'Right to Left'

class Bug():

    def __init__(self, window, id):
        self.window = window
        self.id = id
        # Load pictures Left to Right and Right to Left
        self.pictureLR = pygwidgets.Image(self.window, (0, 0), 'images/bugLR.png')
        self.pictureRL = pygwidgets.Image(self.window, (0, 0), 'images/bugRL.png')
        bugRect = self.pictureLR.getRect()
        self.width = bugRect[2]  # element 2 is the width
        self.setSpeed(1)
        self.resetLoc()

    def setSpeed(self, level):
        self.speed = random.randrange(30 + (2 * level), 60 + (2 * level)) / 10.0
        print('level', level, '    speed is:', self.speed)

    def resetLoc(self):
        # randomly decide if the bug will move left to right, or right to left
        zeroOrOne = random.randrange(0, 2)
        if zeroOrOne == 0:
            self.direction = MOVE_LR
            self.picture = self.pictureLR
            self.x = float(-self.width) - random.randrange(0, 200)
        else:
            self.direction = MOVE_RL
            self.picture = self.pictureRL
            self.x = float(WINDOW_WIDTH) + random.randrange(0, 200)

        row = random.randrange(1, 4)  # choose a random row
        self.y = ROW_OFFSET + (row * ROW_HEIGHT)
        self.picture.setLoc((int(self.x), self.y))

    def update(self):
        if self.direction == MOVE_LR:
            self.x = self.x + self.speed
            if self.x > WINDOW_WIDTH:
                self.resetLoc()
        else:  # moving right to left
            self.x = self.x - self.speed
            if self.x < - self.width:
                self.resetLoc()
        self.picture.setLoc((int(self.x), self.y))

    def getRect(self):
        return self.picture.getRect()

    def draw(self):
        self.picture.draw()
        
