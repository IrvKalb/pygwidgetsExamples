#  FrogGems Main program
#
# Instantiates 3 scenes, creates and starts the Scene Manager


# 1 - Import packages
import pygame
import pyghelpers

from pygame.locals import *
from Constants import *
from SceneSplash import *
from ScenePlay import *
from SceneHighScores import *

# 2 - Define constants
FRAMES_PER_SECOND = 40

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 4 - Load assets: image(s), sounds,  etc.
# Create instances of all scenes.  Specify the window and
# a unique scene key (string) for each scene (stored in Constants.py)
oSplashScene = SceneSplash(window)
oHighScoresScene = SceneHighScores(window)
oPlayScene = ScenePlay(window)



# 5 - Initialize variables
# Build a dictionary of all scenes
scenesList = [oSplashScene, oPlayScene, oHighScoresScene]

# Create the Scene Manager, passing in the scenes list and the FPS
oSceneMgr = pyghelpers.SceneMgr(scenesList, FRAMES_PER_SECOND)  #

# Tell the scene manager to start running
oSceneMgr.run()
