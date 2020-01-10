# Target

import random
import pygwidgets

HIDDEN = 'hidden'
SHOWING = 'showing'
DONE = 'done'

NOT_SHOWN = 'none'
GROWING = 'growing'
FULL = 'full'
SHRINKING = 'shrinking'

TARGET_WIDTH_HEIGHT = 100
SIZE_INCR_DECR = 5  # increment by 5 units (percent) to grow from 0 to 100
SHOW_FULL_TIME = 2
TOTAL_SHOW_TIME = 3 # roughly three seconds, grow + show + shrink


class Target():
    def __init__(self, window, maxWidth, maxHeight, beginTime, maxSeconds):
        myX = random.randrange(0, maxWidth - TARGET_WIDTH_HEIGHT)
        myY = random.randrange(0, maxHeight - TARGET_WIDTH_HEIGHT)

        self.image = pygwidgets.Image(window, (myX, myY), "images/target.png")

        self.startTime = beginTime + random.randrange(maxSeconds - TOTAL_SHOW_TIME) + \
                         (random.randrange(0, 100) / 100.)  # add some fractional time
        self.endTime = self.startTime + TOTAL_SHOW_TIME # Add 3 seconds
        self.state = HIDDEN
        self.showingState = NOT_SHOWN
        self.image.hide()
        self.percent = 0
        self.image.scale(self.percent)

    def update(self, theTime):
        if self.state == HIDDEN:
            if theTime > self.startTime:
                self.state = SHOWING
                self.image.show()
                self.showingState = GROWING

        elif self.state == SHOWING:
            if self.showingState == GROWING:
                self.percent = self.percent + SIZE_INCR_DECR
                self.image.scale(self.percent)
                if self.percent == 100:
                    self.showingState = FULL
                    self.endTime = self.startTime + SHOW_FULL_TIME #  seconds from now

            elif self.showingState == FULL:
                if theTime > self.endTime:
                    self.showingState = SHRINKING

            elif self.showingState == SHRINKING:
                self.percent = self.percent - SIZE_INCR_DECR
                self.image.scale(self.percent)
                if self.percent == 0:
                    self.image.hide()
                    self.state = DONE
                    return True  # returns True to say that this target ran out of time

        elif self.state == DONE:  # state is DONE
            pass  # do nothing

        return False


    def handleClick(self, mouseLoc):
        if self.state == SHOWING:
            myRect = self.image.getRect()
            if myRect.collidepoint(mouseLoc):
                self.state = DONE
                self.image.hide()
                return True  # hit this target

        return False  # did not hit this target

    def draw(self):
        if self.state == SHOWING:
            self.image.draw()
        

        

        
        
