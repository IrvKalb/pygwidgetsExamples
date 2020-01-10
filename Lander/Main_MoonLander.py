#Moon Lander, where we try to land in 1 of the 3 landing pads, and keep speed under 2 m/s

import pygame
from pygame.locals import *
import sys
import random
import math
import pygwidgets
import pyghelpers


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN =  (0, 255, 0)
ORANGE = (255, 100, 0)
GREENISH_YELLOW = (150, 255, 0)
GREENISH = (10,200,125)

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
MAX_WIDTH = WINDOW_WIDTH - 100
MAX_HEIGHT = WINDOW_HEIGHT - 100
FRAMES_PER_SECOND = 30
MOON_START = WINDOW_HEIGHT - 50
LANDED_SAFE = 'landedSafe'
LANDED_WITH_INJURIES = 'landedWithInjuries'
LANDED_CRASHED = 'landedCrashed'
LANDED_NOT = 'landedNot'
GAME_FLYING = 'gameFlying'
GAME_JUST_LANDED = 'gameJustLanded'
GAME_SHOWING_DIALOG = 'gameShowingDialog'



# CONSTANTS
LANDER_MASS = 1
LANDER_FUEL = 100
SPEED_LIMIT = 2.00
PLANET_MASS = 7.347 * (10 ** 8)
PLANET_RADIUS = 1.079
GRAVITY_CONSTANT = 6.673 * (10 ** -11)
GRAVITY = (GRAVITY_CONSTANT * LANDER_MASS * PLANET_MASS)/ (PLANET_RADIUS ** 2)

class FuelGauge(object):
    def __init__(self, window):
        self.window = window
        self.outerRect = pygame.Rect(725, WINDOW_HEIGHT - 30, 150, 40)
        self.thermometerRange = pygame.Rect(750 - 1, WINDOW_HEIGHT - 15, 102, 12)
        self.thermometer = pygame.Rect(750, WINDOW_HEIGHT - 14, 100, 10)


        self.fuelDisplay = pygwidgets.DisplayText(window, (750, WINDOW_HEIGHT - 28), '', \
                                    fontSize=20, textColor=BLACK)

    def mDraw(self, fuelAmount):
        if fuelAmount < 0:
            fuelAmount = 0
        self.thermometer.width = int(fuelAmount)
        self.fuelDisplay.setValue('Fuel: ' + str(fuelAmount))

        if landerFuel >= 90:
            color = GREEN
        elif landerFuel > 65:
            color = GREENISH_YELLOW
        elif landerFuel > 45:
            color = YELLOW
        elif landerFuel > 10:
            color = ORANGE
        else:
            color = RED

        pygame.draw.rect(self.window, color, self.outerRect, 0)
        self.fuelDisplay.draw()
        
        pygame.draw.rect(self.window, BLACK, self.thermometerRange, 0)
        if fuelAmount > 0:
            pygame.draw.rect(self.window, WHITE, self.thermometer, 0)
        


class LandingPad(object):
    HEIGHT = 10

    def __init__(self, window, landingBonus, color, minX, maxX, maxWidth, minWidth):
        self.window = window
        self.color = color
        self.landingBonus = landingBonus

        self.minX = minX
        self.maxX = maxX
        self.maxWidth = maxWidth
        self.minWidth = minWidth

        self.mReset()

    def mReset(self):
        # Create new size and positions for all landing pads
        x = random.randrange(self.minX, self.maxX)
        width = random.randrange(self.minWidth, self.maxWidth)
        self.rect = pygame.Rect(x, MOON_START - 5, width, LandingPad.HEIGHT)
        

    def mIntersects(self, landerRect):
        intersects = landerRect.colliderect(self.rect)
        if intersects:     # check if landed completely inside the landing pad
            inside = (landerRect.left >= self.rect.left) and ((landerRect.left + landerRect.width) <= self.rect.left + self.rect.width)
            return True, inside
        else: 
            return False, False   # does not intersect, and did therefore did not land safely

    def mGetBonus(self):
        return self.landingBonus

    def mDraw(self):
        pygame.draw.ellipse(self.window, self.color, self.rect, 0)


class LandingPadMgr(object):

    def __init__(self, window, minWidth):

        oLandingPad1 = LandingPad(window, 75, YELLOW, 1, 300, 85, minWidth)
        oLandingPad2 = LandingPad(window, 50, GREEN, 400, 1150, 160, minWidth + 15)  # make larger for easy landing
        oLandingPad3 = LandingPad(window, 75, YELLOW, 1300, 1525, 85, minWidth)
        self.landingPadList = [oLandingPad1, oLandingPad2, oLandingPad3]

        self.mReset()

    def mReset(self):
        for oLandingPad in self.landingPadList:
            oLandingPad.mReset()
        
    def mCheckForLanding(self, landerRect):
        for oLandingPad in self.landingPadList:
            landed, insidePad = oLandingPad.mIntersects(landerRect)
            if landed:
                bonus = oLandingPad.mGetBonus()
                return bonus, insidePad

        return 0, False   #  signal that it did not land


    def mGetBonus(self, whichLandingPad):
        oLandingPad = self.landingPadList[whichLandingPad]
        bonus = oLandingPad.mGetBonus()
        return self.bonus

    def mDraw(self):
        for landingPad in self.landingPadList:
            landingPad.mDraw()



class StarField(object):
    def __init__(self, window):
        self.window = window
        self.mReset()
        self.earth = pygame.image.load("images/earth.jpg")

    def mReset(self):
        self.starInfo = []
        nStars = random.randrange(25, 50)
        for i in range(nStars):
            x = random.randrange(0, WINDOW_WIDTH)
            y = random.randrange(0, MOON_START)
            radius = random.randrange(1, 4)
            self.starInfo.append(((x, y), radius))
        self.earthLeft = random.randrange(0, WINDOW_WIDTH)
        self.earthTop = random.randrange(0, MOON_START)

    def mDraw(self):
        for thisStarTuple in self.starInfo:
            pygame.draw.circle(window, WHITE, (thisStarTuple[0]), thisStarTuple[1])
        self.window.blit(self.earth, (self.earthLeft, self.earthTop))

                
        


class Lander(object):
    STARTING_FUEL = 100
    MIN_X = 100
    MAX_X = WINDOW_WIDTH - 100
    START_Y = 2.0
    
    def __init__(self, window):
        self.window = window
        self.imageOK = pygame.image.load("images/lander.png")
        self.imageCrashed = pygame.image.load("images/landerCrashed.png")
        self.imageInjuries = pygame.image.load("images/landerInjuries.png")
        self.rect =  self.imageOK.get_rect()
        self.leftJet = pygame.image.load("images/jetLeft.png")
        self.rightJet = pygame.image.load("images/jetRight.png")
        self.mainJet = pygame.image.load("images/jetMain.png")
        self.leftArrow = pygame.image.load("images/arrowLeft.png")
        self.leftArrowLeft = 2
        self.leftArrowTop = WINDOW_HEIGHT / 2
        self.rightArrow = pygame.image.load("images/arrowRight.png")
        self.rightArrowLeft = WINDOW_WIDTH - 47  # so it shows on window
        self.rightArrowTop = WINDOW_HEIGHT / 2
        self.upArrow = pygame.image.load("images/arrowUp.png")
        self.upArrowLeft = WINDOW_WIDTH / 2
        self.upArrowTop = 2

        self.mReset()


    def mReset(self):
        self.image = self.imageOK
        self.fuel = Lander.STARTING_FUEL
        #  Need these as floating point, because speed increments are decimal values
        self.xSpeed = float(random.randrange(-5, 6))
        self.ySpeed = 0.0
        self.landerX = float(random.randrange(Lander.MIN_X, Lander.MAX_X))
        self.landerY = 2.0
        self.rect.left = int(self.landerX)
        self.rect.top = self.landerY
        self.landed = False
        self.leftEngineOn = False
        self.rightEngineOn = False
        self.mainEngineOn = False
        self.jetSoundPlaying = False
        self.engineSoundPlaying = True

       

    def mUpdate(self, moveLeftEngineOn, moveRightEngineOn, mainEngineOn):
        self.leftEngineOn = moveLeftEngineOn
        self.rightEngineOn = moveRightEngineOn
        self.mainEngineOn = mainEngineOn
        if self.jetSoundPlaying and (not moveRightEngineOn) and (not moveLeftEngineOn):
            jetSound.stop()
            self.jetSoundPlaying = False
        if self.engineSoundPlaying and (not mainEngineOn):
            engineSound.stop()
            self.engineSoundPlaying = False
        
        if self.fuel > 0:
            if self.leftEngineOn:
                self.xSpeed = self.xSpeed - .1
                self.fuel = self.fuel - .25
                if not self.jetSoundPlaying:
                    jetSound.play(-1)  #continuous
                    self.jetSoundPlaying = True

            if self.rightEngineOn:
                self.xSpeed = self.xSpeed + .1
                self.fuel = self.fuel - .25
                if not self.jetSoundPlaying:
                    jetSound.play(-1)
                    self.jetSoundPlaying = True

            if self.mainEngineOn:
                self.ySpeed = self.ySpeed - .25
                self.fuel = self.fuel - 1
                if not self.engineSoundPlaying:                   
                    engineSound.play(-1)  #continuous
                    self.engineSoundPlaying = True

        else:
            self.leftEngineOn = False
            self.rightEngineOn = False
            self.mainEngineOn = False

        self.landerX = self.landerX + self.xSpeed
        self.ySpeed = self.ySpeed + GRAVITY
        self.landerY = self.landerY + self.ySpeed
        
        self.rect.left = int(self.landerX)
        self.rect.top = int(self.landerY)

        return self.rect, self.xSpeed, self.ySpeed

    def mDown(self, landedState): # Lander has landed, may have crashed
        if landedState == LANDED_CRASHED:
            self.image = self.imageCrashed
        elif landedState == LANDED_WITH_INJURIES:
            self.image = self.imageInjuries
        self.ySpeed = 0
        self.leftEngineOn = False
        self.rightEngineOn = False
        self.mainEngineOn = False
        self.ySpeed = 0
        if self.jetSoundPlaying:
            jetSound.stop()
            self.jetSoundPlaying = False
        if self.engineSoundPlaying:
            engineSound.stop()
            self.engineSoundPlaying = False

    def mGetWidth(self):
        return self.rect.width



    def mDraw(self):
        # Show arrows if off window
        if self.rect.left < 0:
            self.window.blit(self.leftArrow, (self.leftArrowLeft, self.leftArrowTop))

        if self.rect.left > WINDOW_WIDTH:
            self.window.blit(self.rightArrow, (self.rightArrowLeft, self.rightArrowTop))

        if self.rect.top < 0:
            self.window.blit(self.upArrow, (self.upArrowLeft, self.upArrowTop))

        
        # Draw the lander, and any jets that are on
        self.window.blit(self.image, self.rect)
                                   
        if self.leftEngineOn:
            self.window.blit(self.rightJet, (self.rect.left, self.rect.top))
            
        if self.rightEngineOn:
            self.window.blit(self.leftJet, (self.rect.left, self.rect.top))

        if self.mainEngineOn:
            self.window.blit(self.mainJet, (self.rect.left, self.rect.top))


    def mGetFuel(self):
        return self.fuel

    def mGetYSpeed(self):
        return self.ySpeed
        


    
#Initialize pygame
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
window= pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

gameFont = pygame.font.SysFont("monospaces", 30)
endFont = pygame.font.SysFont("monospaces", 60)
fuelFont = pygame.font.SysFont("monospaces", 20)

oLander = Lander(window)

minLandingPadSize = oLander.mGetWidth() + 5
oLandingPadMgr = LandingPadMgr(window, minLandingPadSize)

oStarField = StarField(window)

oFuelGauge = FuelGauge(window)

gameState = GAME_FLYING
landedState = LANDED_NOT


# Score
score = 0


#The ground 
moon = pygame.image.load("images/moon.png")
austronaut = pygame.image.load("images/astronaut.png")



liveSpeedX = pygwidgets.DisplayText(window, (500, MOON_START + 20), '', \
                                    fontSize=30, textColor=GREEN)
liveSpeedY = pygwidgets.DisplayText(window, (900, MOON_START + 20), '', \
                                    fontSize=30, textColor=GREEN)
scoreText = pygwidgets.DisplayText(window, (10, MOON_START + 20), '', \
                                    fontSize=30, textColor=GREEN)
countUpTimerField = pygwidgets.DisplayText(window, (WINDOW_WIDTH - 150, MOON_START + 20, ), '0', \
                                    fontSize=30, textColor=GREEN)


# Stuff dealing with dialog box when one round of the game is done
messageDisplay = pygwidgets.DisplayText(window, (565, 290), '', \
                                    fontSize=48, textColor=BLACK)
speedDisplay = pygwidgets.DisplayText(window, (565, 340), '', \
                                    fontSize=48, textColor=BLACK)
newSoftestField = pygwidgets.DisplayText(window, (565, 390), '', \
                                    fontSize=48, textColor=BLACK)
newFastestField = pygwidgets.DisplayText(window, (565, 440), '', \
                                    fontSize=48, textColor=BLACK)
playAgainDisplay = pygwidgets.DisplayText(window, (690, 550), 'Play again?', \
                                    fontSize=48, textColor=BLACK)

startButton = pygwidgets.TextButton(window, (750, 610), 'Start', width=60, height=30)
yesButton = pygwidgets.TextButton(window, (720, 610), 'Yes', width=60, height=30)
noButton = pygwidgets.TextButton(window, (820, 610), 'No', width=60, height=30)

DATA_FILE_PATH = 'LanderData.txt'

# Data file will be made of two entries - separated by a comma:
#  <softestSoFar>,<fastestSoFar>
if pyghelpers.fileExists(DATA_FILE_PATH):
    savedDataString = pyghelpers.readFile(DATA_FILE_PATH)
    savedDataList = savedDataString.split(',') 
    softestSoFar = float(savedDataList[0])
    fastestSoFar = float(savedDataList[1])
else:  #first time, set some outrageous values
    softestSoFar = 10000.
    fastestSoFar = 10000.


oCountUpTimer = pyghelpers.CountUpTimer()
clock = pygame.time.Clock()  # set the speed (frames per second)

introwindow = pygame.image.load("images/introscreen.png")
jetSound = pygame.mixer.Sound('sounds/jet.wav')
engineSound = pygame.mixer.Sound('sounds/engine.wav')
landedSafelySound = pygame.mixer.Sound('sounds/landedSafely.wav')
crashMinorSound = pygame.mixer.Sound('sounds/crashMinor.wav')
crashMajorSound = pygame.mixer.Sound('sounds/crashMajor.wav')

## Intro window:
waitingToPressStart = True
while waitingToPressStart:

    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            sys.exit()

        if startButton.handleEvent(event):
            oLander.mReset()
            oLandingPadMgr.mReset()
            oStarField.mReset()
            gameState = GAME_FLYING
            landedState = LANDED_NOT
            oCountUpTimer.start()
            waitingToPressStart = False   # start up
    
    # Draw star field, moon, control text, landing pads, lander, and control text
    oStarField.mDraw()    
    window.blit(moon, (0, MOON_START))
    landerFuel = oLander.mGetFuel()
    oFuelGauge.mDraw(landerFuel)

    scoreText.draw()

    oLandingPadMgr.mDraw()
    oLander.mDraw()

    window.blit(introwindow, (400, 200))
    startButton.draw()    
       
    # update the window
    pygame.display.update()

    # slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make PyGame wait the correct amount




##  MAIN PLAYING LOOP


# 4 - Loop forever
while True:
    
        
    # 5 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            sys.exit()

    if gameState == GAME_SHOWING_DIALOG:
        if yesButton.handleEvent(event):
            oLander.mReset()
            oLandingPadMgr.mReset()
            oStarField.mReset()
            gameState = GAME_FLYING
            landedState = LANDED_NOT
            oCountUpTimer.start()
            
        if noButton.handleEvent(event):
            pygame.quit()
            sys.exit()
            
    else:   # not landed
        #Moving the lander
        keyPressedList = pygame.key.get_pressed()

        landerRect, landerXSpeed, landerYSpeed = oLander.mUpdate(keyPressedList[pygame.K_LEFT], keyPressedList[K_RIGHT], keyPressedList[K_UP])
        landerXSpeed = round(landerXSpeed, 4)
        landerYSpeed = round(landerYSpeed, 4)
        
        bonusForLandingOnPad, landedInsidePad = oLandingPadMgr.mCheckForLanding(landerRect)  # 0 if not landed, otherwise bonus
        if bonusForLandingOnPad > 0:
            gameState = GAME_JUST_LANDED
            if landerYSpeed < SPEED_LIMIT:
                if landedInsidePad :
                    landedState = LANDED_SAFE
                    score = score + bonusForLandingOnPad
                else:
                    landedState = LANDED_WITH_INJURIES

            else:
                landedState = LANDED_CRASHED
                score = score - 10
                
            oLander.mDown(landedState)
            oCountUpTimer.stop()

        if gameState == GAME_FLYING:    #check for collision on moon
            if (landerRect.top + landerRect.height) > MOON_START:
                gameState = GAME_JUST_LANDED
                score = score - 10
                landedState = LANDED_CRASHED
                oLander.mDown(landedState)
                oCountUpTimer.stop()


    if gameState == GAME_FLYING:
        liveSpeedX.setValue('Hor. Speed: ' + str(landerXSpeed) + ' m/s')
        liveSpeedY.setValue('Vert. Speed: ' + str(landerYSpeed) +  'm/s')

    if gameState == GAME_JUST_LANDED:  # only runs once
        liveSpeedX.setValue('')
        liveSpeedY.setValue('')
        if landedState == LANDED_SAFE:
            messageDisplay.setValue('Safe landing!')
            landedSafelySound.play()
        elif landedState == LANDED_WITH_INJURIES:
            messageDisplay.setValue('Landed, but there are injuries')
            crashMinorSound.play()
            
        else: # LANDED_CRASHED
            messageDisplay.setValue('Crashed!  No survivors')
            crashMajorSound.play()
            
        speedDisplay.setValue('Landing speed: ' + str(landerYSpeed))
        
        writeDataFile = False
        newSoftestField.setValue('')
        newFastestField.setValue('')
        if (bonusForLandingOnPad > 0) and (landedState != LANDED_CRASHED):
            if landerYSpeed < softestSoFar:
                softestSoFar = landerYSpeed
                newSoftestField.setValue('New softest landing:  ' + str(softestSoFar))
                writeDataFile = True

            seconds = oCountUpTimer.getTime()
            if seconds < fastestSoFar:
                fastestSoFar = seconds
                newFastestField.setValue('New fastest landing:  ' + str(fastestSoFar))
                writeDataFile = True

            if writeDataFile:
                dataList = [str(softestSoFar), str(fastestSoFar)]
                dataString = ','.join(dataList)
                print('Writing file')
                pyghelpers.writeFile(DATA_FILE_PATH, dataString)
        gameState = GAME_SHOWING_DIALOG


    scoreText.setValue("Score: " + str(score))
    sec = oCountUpTimer.getTime()  # ask the clock object for the elapsed time
    countUpTimerField.setValue('Time: ' + str(sec))  # put that into a text field

    
    # 6 - clear the window before drawing it again
    window.fill(BLACK)

    # Draw star field, moon, control text, landing pads, lander, and control text
    oStarField.mDraw()    
    window.blit(moon, (0, MOON_START))
    landerFuel = oLander.mGetFuel()
    oFuelGauge.mDraw(landerFuel)
    liveSpeedX.draw()
    liveSpeedY.draw()
    scoreText.draw()
    countUpTimerField.draw()

    oLandingPadMgr.mDraw()
    oLander.mDraw()

    
    if gameState == GAME_SHOWING_DIALOG:
        pygame.draw.rect(window, WHITE, (400, 200, 800, 500))

        if landedState == LANDED_SAFE:
            window.blit(austronaut, (oLander.rect.left + 50, MOON_START - 18))
            newSoftestField.draw()
            newFastestField.draw()
        elif landedState == LANDED_WITH_INJURIES:
            newSoftestField.draw()
            newFastestField.draw()
        else: # LANDED_CRASHED
            pass  # nothing

        messageDisplay.draw()
        speedDisplay.draw()
        playAgainDisplay.draw()

        yesButton.draw()
        noButton.draw()    
       
    # 8 - update the window
    pygame.display.update()

    # 9 slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make PyGame wait the correct amount
    
