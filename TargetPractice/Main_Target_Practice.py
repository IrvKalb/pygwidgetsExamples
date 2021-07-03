#  Target Practice Main program
#
# Instantiates 3 scenes, creates and starts the Scene Manager


# 1 - Import packages
import os
# The next line is here just in case you are running from the command line
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pygame
import pyghelpers
from pygame.locals import *
from Constants import *
from SceneSplash import *
from ScenePlay import *
from SceneScore import *

# 2 - Define constants
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 4 - Load assets: image(s), sounds,  etc.
# Create instances of all scenes.  Specify the window for each scene
oSplashScene = SceneSplash(window)
oPlayScene = ScenePlay(window)
oScoreScene = SceneScore(window)

# 5 - Initialize variables
# Build a list of all scenes
scenesList = [oSplashScene, oPlayScene, oScoreScene]

# Create the Scene Manager, passing in the scenes list, the starting scene, and the FPS
oSceneMgr = pyghelpers.SceneMgr(scenesList, FRAMES_PER_SECOND)  #

# Tell the scene manager to start running
print('Start')
oSceneMgr.run()
