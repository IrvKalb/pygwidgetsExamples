import pygame
import pygwidgets
import random
import sys



pygame.init()


# Set window width/height and caption
WINDOW_WIDTH = 1152
WINDOW_HEIGHT = 1000
STATE_BETTING = 'stateBetting'
STATE_SPINNING = 'stateSpinning'
STATE_PAYING_OUT = 'statePayingOut'

BLACKISH = (10, 10, 10)
YELLOW = (255, 255, 0)
FRAMES_PER_SECOND = 30

COIN_DROP_SOUND = pygame.mixer.Sound('sounds/coinDrop.wav')
COIN_DOWN_SOUND = pygame.mixer.Sound('sounds/coinDown.wav')


class Reel(object):

    def __init__(self, window, locX, locY, minMaxTuple):
        self.window = window
        self.locX = locX
        self.locY = locY
        self.spinning = False
        self.minTime = minMaxTuple[0]
        self.maxTime = minMaxTuple[1]
        self.dialClick = pygame.mixer.Sound("sounds/dialClick.wav")
        pictureOffset = 190
        self.prevY = self.locY - pictureOffset
        self.nextY = self.locY + pictureOffset

        self.reelTuple = ('orange', 'lemon', 'plum', 'cherries', 'banana', 'bar', \
                        'orange', 'lemon', 'plum', 'cherries', 'banana', 'lucky7', \
                        'orange', 'lemon', 'plum', 'cherries', 'banana', 'bar')  # never changes
        self.nItems = len(self.reelTuple)
        self.nItemsMinusOne = self.nItems - 1
        self.index = random.randrange(0, self.nItems)


        self.uniqueList = list(set(self.reelTuple))   # create a list of unique symbols

        self.imageDict = {}
        for symbol in self.uniqueList:
            thisImage = pygame.image.load('images/' + symbol + '.png')
            self.imageDict[symbol] = thisImage

        self.blurredDict = {}
        for symbol in self.uniqueList:
            thisImage = pygame.image.load('images/' + symbol + 'Blurred.png')
            self.blurredDict[symbol] = thisImage

    def mStartSpin(self):

        self.spinning = True
        self.endSpinCount = random.randrange(self.minTime, self.maxTime)
        endingIndex = (self.index + self.endSpinCount) % self.nItems
        self.endingSymbol = self.reelTuple[endingIndex]
        self.nSpins = 0
        #print 'in startSpin, endSpinCount is:', self.endSpinCount
        return self.endingSymbol

    def mSpin(self):
        if self.spinning:
            self.nSpins = self.nSpins + 1
            self.index = self.index + 1
            if self.index >= self.nItems:
                self.index = 0

            if self.nSpins == self.endSpinCount:
                self.spinning = False
                self.dialClick.play()


        return self.spinning


    def mDraw(self):

        prevIndex = self.index - 1
        if prevIndex == -1:
            prevIndex = self.nItems - 1

        nextIndex = self.index + 1
        if nextIndex == self.nItems:
            nextIndex = 0

        #print 'self.index is:', self.index
        symbolPrev = self.reelTuple[prevIndex]
        symbol = self.reelTuple[self.index]
        symbolNext = self.reelTuple[nextIndex]
        if self.spinning:
            # drawing blurred pic
            imagePrev = self.blurredDict[symbolPrev]
            image = self.blurredDict[symbol]
            imageNext = self.blurredDict[symbolNext]
        else:
            #draw reg pic
            imagePrev = self.imageDict[symbolPrev]
            image = self.imageDict[symbol]
            imageNext = self.imageDict[symbolNext]

        self.window.blit(imagePrev, [self.locX, self.prevY])
        self.window.blit(image, [self.locX, self.locY])
        self.window.blit(imageNext, [self.locX, self.nextY])

class ReelMgr(object):
    def __init__(self, window):
        locXList = (308, 499, 690)
        locY = 371
        timeRanges = ((12, 18), (24, 30), (36, 42))

        oReel0 = Reel(window, locXList[0], locY, timeRanges[0])
        oReel1 = Reel(window, locXList[1], locY, timeRanges[1])
        oReel2 = Reel(window, locXList[2], locY, timeRanges[2])

        self.reelTuple = [oReel0, oReel1, oReel2]


    def mStartSpin(self):
        symbolsList = []
        for oReel in self.reelTuple:
            thisEndingSymbol = oReel.mStartSpin()
            symbolsList.append(thisEndingSymbol)
        return symbolsList

    def mSpin(self):
        for oReel in self.reelTuple:
            done = oReel.mSpin()

        # Only need to return the result of if the last reel is done spinning
        return done

    def mDraw(self):
        for oReel in self.reelTuple:
            oReel.mDraw()


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Slot Machine')

pygame.font.init()
#moneyFont = pygame.font.SysFont(fontName='Haettenschweiler', fontSize=30)
#jackpotFont = pygame.font.SysFont(fontName='Broadway', fontSize=50)
#messageFont = pygame.font.SysFont(fontName='Haettenschweiler', fontSize=35)


slotMachine_image = pygame.image.load("images/slotMachine.png")
slotMachineCoverTop = pygame.image.load("images/slotMachineCoverTop.png")
slotMachineCoverBottom = pygame.image.load("images/slotMachineCoverBottom.png")
payLine = pygame.image.load('images/payline.png')

jackpotDisplay = pygwidgets.DisplayText(window,(530, 212), '', \
                                    fontName='Broadway', fontSize=50, textColor=BLACKISH)
betDisplay = pygwidgets.DisplayText(window, (376,710), '', \
                                    fontName='Haettenschweiler', fontSize=30, textColor=YELLOW)
coinsDisplay = pygwidgets.DisplayText(window,(610, 710), '', \
                                    fontName='Haettenschweiler', fontSize=30, textColor=YELLOW)
winningsDisplay = pygwidgets.DisplayText(window, (800, 710), '', \
                                    fontName='Haettenschweiler', fontSize=30, textColor=YELLOW)
messageDisplay = pygwidgets.DisplayText(window, (181, 870), '', \
                                    fontName='Haettenschweiler', fontSize=35, textColor=BLACKISH)

spinButton = pygwidgets.CustomButton(window,(755, 772, 108, 44), \
                                 up='images/spinButton.png', down='images/spinButtonDown.png', \
                                over='images/spinButtonOver.png', disabled='images/spinButtonGray.png')
bet1Button = pygwidgets.TextButton(window, (230, 785), 'Bet 1', width=108, height=44,\
                                soundOnClick=COIN_DROP_SOUND)
up1Button = pygwidgets.CustomButton(window, (395, 766),\
                                up='images/upArrow.png', down='images/upArrowDown.png', \
                                over='images/upArrowOver.png', disabled='images/upArrowGray.png',
                                soundOnClick=COIN_DROP_SOUND)
down1Button = pygwidgets.CustomButton(window, (395, 818),\
                                up='images/downArrow.png', down='images/downArrowDown.png',\
                                over='images/downArrowOver.png', disabled='images/downArrowGray.png',
                                soundOnClick=COIN_DOWN_SOUND)
up10Button = pygwidgets.CustomButton(window, (490, 766),\
                                up='images/upArrow.png', down='images/upArrowDown.png', \
                                over='images/upArrowOver.png', disabled='images/upArrowGray.png',
                                soundOnClick=COIN_DROP_SOUND)
down10Button = pygwidgets.CustomButton(window, (490, 818),\
                                up='images/downArrow.png', down='images/downArrowDown.png',\
                                over='images/downArrowOver.png', disabled='images/downArrowGray.png',
                                soundOnClick=COIN_DOWN_SOUND)
betMaxButton = pygwidgets.TextButton(window, (580, 785), 'Bet Max', width=108, height=44,\
                                soundOnClick=COIN_DROP_SOUND)



#Functions
def payTable(myList, currentJackpot):
    picture1 = myList[0]
    picture2 = myList[1]
    picture3 = myList[2]
    if myList.count(picture1) == 3:
        if picture1== 'Lucky 7':
            nCoinsWon = currentJackpot
        elif picture1== 'bar':
            nCoinsWon = 100
        else:
            nCoinsWon = 10

    else:
        if (picture1 == picture2) or (picture2 == picture3) or (picture1 == picture3):
            nCoinsWon = 2
        else:
            nCoinsWon = 0

    return nCoinsWon


#SoundVariables
doneSound = pygame.mixer.Sound('sounds/done.wav')

#Variables
clock = pygame.time.Clock()
nCoins = 100
bet = 10
winnings = 0
jackpot = random.randrange(1000, 10000)
message = "Place your bet, click or press space to spin."

oReelMgr = ReelMgr(window)

state = STATE_BETTING

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if state == STATE_BETTING:
            if (spinButton.handleEvent(event)) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE)):
                endingSymbolsList = oReelMgr.mStartSpin()
                jackpot = jackpot + 1
                nCoins = nCoins - bet  # subtract the bet
                winnings = 0  # clear the winnings
                state = STATE_SPINNING

            if  up1Button.handleEvent(event):
                bet = bet + 1
                #coinDropSound.play()

            if  down1Button.handleEvent(event):
                bet = bet - 1
                #coinDownSound.play()

            if  up10Button.handleEvent(event):
                bet = bet + 10
                #coinDropSound.play()

            if  down10Button.handleEvent(event):
                bet = bet - 10
                #coinDownSound.play()

            if  bet1Button.handleEvent(event):
                bet = 1
                #coinDropSound.play()

            if  betMaxButton.handleEvent(event):
                bet = nCoins
                #coinDropSound.play()



    if state == STATE_SPINNING:
        isSpinning = oReelMgr.mSpin()
        if not isSpinning:  # When the spin finishes
            nCoinsWon = payTable(endingSymbolsList, jackpot)
            winnings = bet * nCoinsWon
            nCoins = nCoins + winnings  # add in any winnings
            state = STATE_BETTING
            if winnings > 200:
                message = 'Way to go!!'
            elif winnings > 50:
                message = 'WOO-HOO'
            elif winnings > 0:
                message = 'CHA-CHING'
            else:
                 message = 'Sorry about that.'

            if nCoins == 0:
                message = 'Come back when you have more money'
                bet = 0
                doneSound.play()

    # Enable/disable appropriate betting buttons
    if (state == STATE_BETTING) or (state == STATE_PAYING_OUT):
        if bet > nCoins:
            bet = nCoins

        if nCoins > 0:
            spinButton.enable()
            bet1Button.enable()
            betMaxButton.enable()
        else:
            spinButton.disable()
            bet1Button.disable()
            betMaxButton.disable()

        if bet < nCoins:
            up1Button.enable()
        else:
            up1Button.disable()
        if bet > 1:
            down1Button.enable()
        else:
            down1Button.disable()

        if (bet + 10) <= nCoins:
            up10Button.enable()
        else:
            up10Button.disable()
        if bet > 10:
            down10Button.enable()
        else:
            down10Button.disable()

    coinsDisplay.setValue(str(nCoins))
    jackpotDisplay.setValue(str(jackpot))
    betDisplay.setValue(str(bet))
    winningsDisplay.setValue(str(winnings))
    messageDisplay.setValue(message)

    # Display everything
    window.fill((255, 255, 255))
    window.blit(slotMachine_image,(0, 0))

    oReelMgr.mDraw()
    window.blit(payLine, (270, 492))

    window.blit(slotMachineCoverTop,(0, 0))
    window.blit(slotMachineCoverBottom,(0, 0))

    coinsDisplay.draw()
    jackpotDisplay.draw()
    betDisplay.draw()
    winningsDisplay.draw()
    messageDisplay.draw()

    bet1Button.draw()
    up1Button.draw()
    down1Button.draw()
    up10Button.draw()
    down10Button.draw()
    betMaxButton.draw()
    spinButton.draw()

    #bet1Button.debug()  ### TEMPORARY

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

