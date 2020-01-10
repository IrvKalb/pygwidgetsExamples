#
# Import packages
#
import pygame
from pygame.locals import *
import pygwidgets
import random
import sys

# Define constants
BARRIER_COLOR = (207, 204, 118)
BACKGROUND_COLOR = (233, 232, 214)
PLAYER_COLOR = (207, 114, 118)
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 840
FPS = 30

TILE_SIZE = 20
NROWS = 42
NCOLS = 24
MIDCOL = NCOLS // 2
PLAYER_START_ROW = NROWS // 2

STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game over'
STATE_PRE_ROUND = 'pre round'

#
# Initialize pygame
#
pygame.init()
window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
clock = pygame.time.Clock()

#
# Load assets
#
tileImage = pygame.image.load("images/tile.png")
playerImage = pygame.image.load("images/player.png")

#
# Initialize Variables
#
frameCounter = 0
state = STATE_PRE_ROUND

levelInfoDict = { \
    1: {'corridorWidth': 6, 'nFramesBetweenUpdates': 5, 'timeToComplete': 10, 'pctShift': 50}, \
    2: {'corridorWidth': 6, 'nFramesBetweenUpdates': 4, 'timeToComplete': 30, 'pctShift': 65}, \
    3: {'corridorWidth': 6, 'nFramesBetweenUpdates': 4, 'timeToComplete': 40, 'pctShift': 75}, \
    4: {'corridorWidth': 6, 'nFramesBetweenUpdates': 4, 'timeToComplete': 40, 'pctShift': 80}, \
    5: {'corridorWidth': 5, 'nFramesBetweenUpdates': 4, 'timeToComplete': 40, 'pctShift': 85}, \
    6: {'corridorWidth': 5, 'nFramesBetweenUpdates': 3, 'timeToComplete': 40, 'pctShift': 90} \
    }

nLevels = len(levelInfoDict)

level = 0  # increments before level starts
nextLevel = True  # So we build level 1 first time through
playerCol = NCOLS // 2

messageLine1 = pygwidgets.DisplayText(window, (0, 315), '', \
                                    fontSize=40, textColor=BACKGROUND_COLOR, width=480, justified='center')
timeMessage = pygwidgets.DisplayText(window, (0, 360), '', \
                                    fontSize=80, textColor=PLAYER_COLOR, width=480, justified='center')
messageLine2 = pygwidgets.DisplayText(window, (0, 435), '', \
                                    fontSize=40, textColor=BACKGROUND_COLOR, width=480, justified='center')

startButton = pygwidgets.TextButton(window, (195, 500), 'Start', enterToActivate=True)
startOverButton = pygwidgets.TextButton(window, (200, 500), 'Start Over')
restartLevelButton = pygwidgets.TextButton(window, (200, 560), 'Restart Current Level')
quitButton = pygwidgets.TextButton(window, (200, 620), 'Quit')


#
# Loop Forever
#
while True:

    # Loop through events
    for event in pygame.event.get():

        # check if quitting
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if state == STATE_PLAYING:

            # Check for keypress
            if event.type == pygame.KEYDOWN:

                # Arrow key left
                if event.key == pygame.K_LEFT:
                    if playerCol > 0:
                        playerCol = playerCol - 1

                # Arrow key right
                elif event.key == pygame.K_RIGHT:
                    if playerCol < NCOLS:
                        playerCol = playerCol + 1

                # Arrow key up
                elif event.key == pygame.K_UP:
                    if playerRow > 0:
                        playerRow = playerRow - 1

                # Arrow key down
                elif event.key == pygame.K_DOWN:
                    if playerRow < NROWS - 1:
                        playerRow = playerRow + 1

        elif state == STATE_PRE_ROUND:

            # Wait for start button
            if startButton.handleEvent(event):
                state = STATE_PLAYING
                startTicks = pygame.time.get_ticks()

        elif state == STATE_GAME_OVER:
            if startOverButton.handleEvent(event):
                level = 0
                nextLevel = True
                state = STATE_PRE_ROUND

            elif restartLevelButton.handleEvent(event):
                level = level - 1
                nextLevel = True
                state = STATE_PRE_ROUND

            elif quitButton.handleEvent(event):
                pygame.quit()
                sys.exit(0)

    # Do any per frame actions
    if state == STATE_PRE_ROUND:
        if nextLevel:  # Time to build the next level
            nextLevel = False
            level = level + 1
            if nextLevel == nLevels:   # Finished!
                messageLine1.setValue('YOU WIN!!!')
                timeMessage.setValue(str(''))
                messageLine2.setValue('CONGRATULATIONS')

            else:  # go to next level

                playerRow = PLAYER_START_ROW
                playerCol = NCOLS // 2
                levelDict = levelInfoDict[level]  # get the dictionary representing the next level of the game

                corridorWidth = levelDict['corridorWidth']
                nFramesBetweenUpdates = levelDict['nFramesBetweenUpdates']
                pctShift = levelDict['pctShift']
                timeToComplete = levelDict['timeToComplete']
                halfCorridorWidth = corridorWidth // 2
                startCol = MIDCOL - halfCorridorWidth
                maxCorridorStartIndex = NCOLS - corridorWidth

                messageLine1.setValue('LEVEL: ' + str(level))
                timeMessage.setValue(str(timeToComplete) + ' seconds')
                messageLine2.setValue('')

                # Build a single row with the corridor in the middle
                oneRow = []
                for colNum in range(0, NCOLS):
                    if (colNum >= startCol) and (colNum < (startCol + corridorWidth)):
                        oneRow.append(False)
                    else:
                        oneRow.append(True)

                # Build the whole starting screen as copies of that row
                screenData = []
                for rowNum in range(0, NROWS):
                    screenData.append(oneRow)

    elif state == STATE_PLAYING:

        # Generate a new row every 'tick'
        frameCounter = frameCounter + 1
        if frameCounter == nFramesBetweenUpdates:
            frameCounter = 0
            screenData.pop(NROWS - 1)  # remove bottom row of screen data
            rowZero = screenData[0][:]  # make a copy of screen data row 0

            # Figure out if we should shift left or right
            randomValue = random.randrange(1, 101)
            if randomValue <= pctShift:  # Do a shift
                # Find beginning of corridor, first False is where it starts
                corridorStart = 0
                for tileValue in rowZero:
                    if tileValue is False:
                        break
                    corridorStart = corridorStart + 1

                direction = random.randrange(0, 2)  # 0 means shift left, 1 means shift right
                if direction == 0:  # shift left
                    if corridorStart > 0:
                        rowZero[corridorStart - 1] = False
                        rowZero[corridorStart + corridorWidth - 1] = True

                else:  # shift right
                    if corridorStart < maxCorridorStartIndex:
                        rowZero[corridorStart] = True
                        rowZero[corridorStart + corridorWidth] = False

            # Paste new row into top of screen data
            screenData.insert(0, rowZero)

#
# Draw all elements
#
    if state == STATE_PRE_ROUND:
        # fill background
        window.fill(BARRIER_COLOR)

        messageLine1.draw()
        timeMessage.draw()
        messageLine2.draw()
        startButton.draw()
        
    elif state == STATE_PLAYING:
        
        # fill background
        window.fill(BACKGROUND_COLOR)

        # Draw tiles
        for row in range(0, NROWS):
            for col in range(0, NCOLS):

                if screenData[row][col]:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    window.blit(tileImage, (x, y))

        # Draw player
        x = playerCol * TILE_SIZE
        window.blit(playerImage, (x, playerRow * TILE_SIZE))

        endTicks = pygame.time.get_ticks()
        aliveTicks = endTicks - startTicks
        aliveSeconds = aliveTicks // 1000

        if aliveSeconds >= timeToComplete:
            # Time is up, moving to next level
            nextLevel = True
            state = STATE_PRE_ROUND

        # Check for collision with corridor - if True, game is over
        elif screenData[playerRow][playerCol]:
            messageLine1.setValue('YOU SURVIVED')
            # Be anal about grammar
            if aliveSeconds == 1:
                timeMessage.setValue(str(aliveSeconds) + ' SECOND')
            else:
                timeMessage.setValue(str(aliveSeconds) + ' SECONDS')
            messageLine2.setValue('IN LEVEL ' + str(level))
            state = STATE_GAME_OVER

    elif state == STATE_GAME_OVER:
        # fill background
        window.fill(BARRIER_COLOR)

        messageLine1.draw()
        timeMessage.draw()
        messageLine2.draw()
        startOverButton.draw()
        restartLevelButton.draw()
        quitButton.draw()

    # update window
    pygame.display.update()

    # match ticks to framerate
    clock.tick(FPS)
