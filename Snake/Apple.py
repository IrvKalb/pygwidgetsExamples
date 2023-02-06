import pygame
import random
from Constants import *


class Apple():

  def __init__(self, window):
    self.window = window
    self.setNewLocation()

  def setNewLocation(self):
    self.x = random.randint(0, N_CELLS_WIDE - 1)
    self.y = random.randint(0, N_CELLS_HIGH - 1)

  def getLocation(self):
    return (self.x, self.y)

  def draw(self):
    appleRect = pygame.Rect(self.x * CELLSIZE, self.y * CELLSIZE, CELLSIZE, CELLSIZE)
    pygame.draw.rect(self.window, RED, appleRect)