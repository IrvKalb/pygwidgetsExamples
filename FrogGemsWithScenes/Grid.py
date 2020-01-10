from Constants import *
import pygwidgets
import random

class Grid():
    def __init__(self, window):
        self.window = window
        self.oBlueGem = pygwidgets.Image(self.window, (0, 0), 'images/gem-blue.png')
        self.oOrangeGem = pygwidgets.Image(self.window, (0, 0), 'images/gem-green.png')
        self.oGreenGem = pygwidgets.Image(self.window, (0, 0), 'images/gem-orange.png')
        self.oStar = pygwidgets.Image(self.window, (0, 0), 'images/gem-black.png')
        self.oHeart = pygwidgets.Image(self.window, (0, 0), 'images/Heart.png')


        self.grid = [[NOTHING, NOTHING, NOTHING, NOTHING, NOTHING],\
                     [NOTHING, NOTHING, NOTHING, NOTHING, NOTHING], \
                     [NOTHING, NOTHING, NOTHING, NOTHING, NOTHING], \
                     [NOTHING, NOTHING, NOTHING, NOTHING, NOTHING], \
                     [NOTHING, NOTHING, NOTHING, NOTHING, NOTHING], \
                     [NOTHING, NOTHING, NOTHING, NOTHING, NOTHING]]
        self.newRound(1)


    def newRound(self, theLevel):
        for row in range(START_PLACING_ROW, END_PLACING_ROW):
            for col in range(0, NCOLS_IN_GRID):
                randomValue = random.randrange(0, 101)
                if randomValue < 50:
                    self.grid[row][col] = NOTHING
                elif randomValue < 75:
                    self.grid[row][col] = BLUE_GEM
                elif randomValue < 90:
                    self.grid[row][col] = GREEN_GEM
                elif randomValue < 95:
                    self.grid[row][col] = ORANGE_GEM
                elif randomValue < 98:
                    self.grid[row][col] = BLACK_GEM
                else:
                    self.grid[row][col] = HEART


    def getItem(self, row, col):
        return self.grid[row][col]

    def clearItem(self, row, col):
        self.grid[row][col] = NOTHING
        for row in range(START_PLACING_ROW, END_PLACING_ROW):
            for col in range(0, NCOLS_IN_GRID):
                if self.grid[row][col] != NOTHING:
                    return False

        return True


    def draw(self):
        for row in range(START_PLACING_ROW, END_PLACING_ROW):
            for col in range(0, NCOLS_IN_GRID):

                thisLoc = ((col * COL_WIDTH), (ROW_OFFSET + (row * ROW_HEIGHT)))

                item = self.grid[row][col]
                # ignore NOTHINGs
                if item == BLUE_GEM:
                    self.oBlueGem.setLoc(thisLoc)
                    self.oBlueGem.draw()
                elif item == ORANGE_GEM:
                    self.oOrangeGem.setLoc(thisLoc)
                    self.oOrangeGem.draw()
                elif item == GREEN_GEM:
                    self.oGreenGem.setLoc(thisLoc)
                    self.oGreenGem.draw()
                elif item == BLACK_GEM:
                    self.oStar.setLoc(thisLoc)
                    self.oStar.draw()
                elif item == HEART:  # Heart
                    self.oHeart.setLoc(thisLoc)
                    self.oHeart.draw()

