# Demo of Scenes with Scene manager
# Connect 4
# Original code from Making Games with Python & Pygame by my friend, Al Sweigart

# 1 - Import packages

import pygame
import pyghelpers
import sys
from Constants import *
from SceneChoose import *
from ScenePlay import *


# 2 - Define constants
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Load assets: image(s), sounds,  etc.

# 5 - Initialize variables
# Instantiate all scenes and store them into a dictionary
scenesDict = {SCENE_CHOOSE: SceneChoose(window), SCENE_PLAY: ScenePlay(window)}

# Create the Scene Manager, passing in the scenes dict, and FPS
oSceneMgr = pyghelpers.SceneMgr(scenesDict, FRAMES_PER_SECOND)

# Tell the scene manager to start running
oSceneMgr.run()