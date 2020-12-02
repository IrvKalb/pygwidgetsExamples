# Square

from Constants import *

class Square(object):


    def __init__(self, window, boundingLinesList, x, y, emptyImage, humanImage, computerImage):
        self.window = window
        self.boundingLinesList = boundingLinesList
        self.loc = (x, y)
        self.owned = False
        self.emptyImage = emptyImage
        self.humanImage = humanImage
        self.computerImage = computerImage
        self.mReset()


    def mReset(self):
        self.image = self.emptyImage
        self.owned = False


    def draw(self):
        self.window.blit(self.image, self.loc)

    def mSetOwner(self, owner):
        self.owner = owner
        self.owned = True
        if owner == HUMAN:
            self.image = self.humanImage
        else:
            self.image = self.computerImage



    def mGetOwner(self):
        return self.owner

    def mGetOwned(self):
        return self.owned

    def mGetLines(self):
        return self.boundingLinesList

    # def mSetMarker(self, iMarker):
    #     self.marker = iMarker
    #     if self.owned:
    #         if (self.owner == Square.HUMAN):
    #             self.image = self.humanImage



