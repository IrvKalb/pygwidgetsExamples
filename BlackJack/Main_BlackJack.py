import pygame
from pygame.locals import *
import sys
import random
import pygwidgets

# CONSTANTS
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FRAMES_PER_SECOND = 30
FRAMES_BETWEEN_DEALING_CARD = 13

STATE_BETTING = 'stateBetting'
STATE_DEALING = 'stateDealing'
STATE_PLAYER_TURN = 'statePlayerTurn'
STATE_DEALER_TURN = 'stateDealerTurn'
STATE_DETERMINE_OUTCOME = 'stateDetermineOutcome'

#
# DECK
#
class Deck():

    SUIT_TUPLE = ('Spades', 'Hearts', 'Clubs', 'Diamonds')
    NAME_TUPLE = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')
    VALUE_TUPLE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10)

    def __init__(self):
        self.startingDeckList = []
        self.deckList = []
        for suit in Deck.SUIT_TUPLE:
            for index, name in enumerate(Deck.NAME_TUPLE):
                thisValue = Deck.VALUE_TUPLE[index]
                cardName = name + ' of ' + suit
                fileName = 'images/' + cardName +'.png'
                thisImage = pygame.image.load(fileName)
                cardDict = {'name':cardName, 'value':thisValue, 'image':thisImage}

                self.startingDeckList.append(cardDict)
        self.shuffle()

    
    def shuffle(self):
        cardShuffleSound.play()
        self.deckList = self.startingDeckList[:]  # make a copy of the starting deck
        random.shuffle(self.deckList)

         
    def getCard(self):
        if len(self.deckList) == 0:
            return 'no more cards'
        cardFlipSound.play()
        thisCard = self.deckList.pop() # pops one off of the top of the deck and returns
        return thisCard
    
#
# HAND
#
class Hand:
    CARD_OFFSET = 110
    DEALER_TOP = 78
    PLAYER_TOP = 344
    HAND_LEFT = 160

    def __init__(self, window, dealerOrPlayer):  # 'dealer' or 'player'
        self.window = window
        self.dealerOrPlayer = dealerOrPlayer
        self.handValue = 0
        self.bust = False
        self.cardList = []

        if self.dealerOrPlayer == 'dealer':
            self.dealer = True
            self.top = Hand.DEALER_TOP
            self.backOfCardImage = pygame.image.load('images/BackOfCard.png')
            self.valueText = pygwidgets.DisplayText(self.window, (174, 26), '', \
                            fontSize=40, textColor=BLACK)
        else:
            self.dealer = False
            self.top = Hand.PLAYER_TOP
            self.valueText = pygwidgets.DisplayText(self.window, (174, 290), '', \
                            fontSize=40, textColor=BLACK)
        self.reset()

    def reset(self):
        self.cardList = []
        
    def addCard(self, card):
        self.cardList.append(card)
        self.handValue = self.getTotal()
        self.bust = (self.handValue > 21)
        return self.handValue, self.bust
    
    def getTotal(self):
        total = 0 
        nAces = 0 
        for card in self.cardList:
            value = card['value']
            total = total + value
            if value == 1: 
                nAces = nAces + 1
        
        if (nAces > 0) and (total < 12):
            total = total + 10
    
        return total

    # For development testing:
    def printHand(self):
        print()
        print('Dealer:', self.dealer)
        print('Top:', self.top)
        for card in self.cardList:
            print(card['name'])

    def wasBlackJack(self):
        blackJack = (self.handValue == 21) and (len(self.cardList) == 2)
        return blackJack

    def draw(self, hideDealerInfo):
        left = Hand.HAND_LEFT
        for cardNum, card in enumerate(self.cardList):
            if self.dealer and (cardNum == 0) and hideDealerInfo:
                thisImage = self.backOfCardImage
            else:
                thisImage = card['image']
            window.blit(thisImage, (left, self.top))
            left = left + Hand.CARD_OFFSET

        if self.cardList == []:
            self.valueText.setValue('')
        else:
            if self.dealer and hideDealerInfo:
                self.valueText.setValue('??')
            else:
                self.valueText.setValue(str(self.handValue))
        self.valueText.draw()

#
# MAIN CODE
#

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

backgroundImage = pygame.image.load('images/background.png')
hitButton = pygwidgets.TextButton(window, (22, 350), 'Hit', width=108, height=44)
stayButton = pygwidgets.TextButton(window, (22, 420), 'Stay', width=108, height=44)
playGameButton = pygwidgets.TextButton(window, (20, 530), 'Play Game', width=108, height=44)
quitButton = pygwidgets.TextButton(window, (800, 530), 'Quit', width=108, height=44)
bet1Button = pygwidgets.TextButton(window, (230, 530), 'Bet 1', width=108, height=44)
up1Button = pygwidgets.CustomButton(window, (398, 510),\
                                up='images/upArrow.png', down='images/upArrowDown.png', \
                                over='images/upArrowOver.png', disabled='images/upArrowGray.png')
down1Button = pygwidgets.CustomButton(window, (398, 568),\
                                up='images/downArrow.png', down='images/downArrowDown.png',\
                                over='images/downArrowOver.png', disabled='images/downArrowGray.png')
up10Button = pygwidgets.CustomButton(window, (494, 510),\
                                up='images/upArrow.png', down='images/upArrowDown.png', \
                                over='images/upArrowOver.png', disabled='images/upArrowGray.png')
down10Button = pygwidgets.CustomButton(window, (494, 568),\
                                up='images/downArrow.png', down='images/downArrowDown.png',\
                                over='images/downArrowOver.png', disabled='images/downArrowGray.png')
betMaxButton = pygwidgets.TextButton(window, (600, 530), 'Bet Max', width=108, height=44)
winnerSound = pygame.mixer.Sound("sounds/winner.wav")
pushSound = pygame.mixer.Sound("sounds/push.wav")
loserSound = pygame.mixer.Sound("sounds/loser.wav")
dingSound = pygame.mixer.Sound("sounds/ding.wav")
cardShuffleSound = pygame.mixer.Sound("sounds/cardShuffle.wav")
cardFlipSound = pygame.mixer.Sound("sounds/cardFlip.wav")
coinDropSound = pygame.mixer.Sound("sounds/coinDrop.wav")
coinDownSound = pygame.mixer.Sound("sounds/coinDown.wav")


#messageFont = pygame.font.SysFont(None, 36)
messageText = pygwidgets.DisplayText(window, (160, 234), 'Welcome to BlackJack', \
                                fontSize=36, textColor=WHITE)

creditsText = pygwidgets.DisplayText(window,(200, 484),  '', \
                                fontSize=36, textColor=WHITE)
betText = pygwidgets.DisplayText(window, (434, 484), '', \
                                fontSize=36, textColor=WHITE)


deck = Deck()

dealer = Hand(window, 'dealer')
player = Hand(window, 'player')

state = STATE_BETTING
nCardsDealt = 0
frameNumber = FRAMES_BETWEEN_DEALING_CARD  # Force first card right away

bet = 10
nCredits = 200

while True:
    # Handle events
    for event in pygame.event.get():
        if (event.type == QUIT) or \
            ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or \
            (quitButton.handleEvent(event)):
            pygame.quit()
            sys.exit()

        if quitButton.handleEvent(event):
            pygame.quit()
            sys.exit()

        if state == STATE_PLAYER_TURN:
            if  hitButton.handleEvent(event):
                playerHandValue, playerBust = player.addCard(deck.getCard())
                if playerBust:
                    state = STATE_DETERMINE_OUTCOME

            if  stayButton.handleEvent(event):
                state = STATE_DEALER_TURN

        elif state == STATE_BETTING:
            if (playGameButton.handleEvent(event)) \
                or ((event.type == KEYDOWN) and (event.key in (K_RETURN, K_KP_ENTER))):
                deck.shuffle()
                dealer.reset()
                player.reset()
                messageText.setValue('')
                state = STATE_DEALING

            if up1Button.handleEvent(event):
                bet = bet + 1
                coinDropSound.play()

            if down1Button.handleEvent(event):
                bet = bet - 1
                coinDownSound.play()

            if up10Button.handleEvent(event):
                bet = bet + 10
                coinDropSound.play()

            if down10Button.handleEvent(event):
                bet = bet - 10
                coinDownSound.play()

            if bet1Button.handleEvent(event):
                bet = 1
                coinDropSound.play()

            if betMaxButton.handleEvent(event):
                bet = nCredits
                coinDropSound.play()

            if bet > nCredits:
                bet = nCredits

    if state == STATE_DEALING:
        if frameNumber == FRAMES_BETWEEN_DEALING_CARD:
            if (nCardsDealt == 0) or (nCardsDealt == 2):  # alternate
                playerHandValue, playerBust = player.addCard(deck.getCard())
            else:
                dealerHandValue, dealerBust = dealer.addCard(deck.getCard())
            frameNumber = 0
            nCardsDealt = nCardsDealt + 1
        else:
            frameNumber = frameNumber + 1

        if nCardsDealt == 4:
            nCardsDealt = 0
            frameNumber = FRAMES_BETWEEN_DEALING_CARD
            state = STATE_PLAYER_TURN

    elif state == STATE_DEALER_TURN:
        if frameNumber == FRAMES_BETWEEN_DEALING_CARD:
            dealerHandValue, dealerBust = dealer.addCard(deck.getCard())
            frameNumber = 0
        else:
            frameNumber = frameNumber + 1

        if (dealerHandValue >= 17) or (dealerHandValue > playerHandValue):
            nCardsDealt = 0
            frameNumber = FRAMES_BETWEEN_DEALING_CARD
            state = STATE_DETERMINE_OUTCOME

    if state == STATE_DETERMINE_OUTCOME:
        if playerBust:
            winner = 'Dealer'
            output = 'Dealer wins (player busted).'
        elif dealerBust:
            winner = 'Player'
            output = 'Player wins (dealer busted).'
        else:
            if dealerHandValue > playerHandValue:
                winner = 'Dealer'
                output = 'Dealer wins with high score.'
            elif dealerHandValue == playerHandValue:
                winner = 'Push'
                output = "It's a tie (push)."
            else:
                winner = 'Player'
                output = 'Player wins with high score.'

        messageText.setValue(output)

        if winner == 'Player':
            if player.wasBlackJack():
                winnings = bet + (bet / 2)  # integer division, rounds down
                nCredits = nCredits + winnings
                dingSound.play()
            else:
                nCredits = nCredits + bet
            winnerSound.play()
        elif winner == 'Dealer':
            nCredits = nCredits - bet
            loserSound.play()
        else:  # tie
            pushSound.play()
        state = STATE_BETTING

    creditsText.setValue('Credits: ' + str(nCredits))
    betText.setValue('Bet:  ' + str(bet))

    playGameButton.disable()
    bet1Button.disable()
    up1Button.disable()
    down1Button.disable()
    up10Button.disable()
    down10Button.disable()
    betMaxButton.disable()

    if state == STATE_BETTING:
        if nCredits > 0:
            playGameButton.enable()
            bet1Button.enable()
            betMaxButton.enable()

        if bet < nCredits:
            up1Button.enable()

        if bet > 1:
            down1Button.enable()

        if (bet + 10) <= nCredits:
            up10Button.enable()

        if bet > 10:
            down10Button.enable()

    # Draw everything
    window.blit(backgroundImage, (0, 0))

    # Tell both hands to draw themselves
    hide = state in [STATE_DEALING, STATE_PLAYER_TURN]
    dealer.draw(hide)
    player.draw(False)

    if state == STATE_PLAYER_TURN:
        hitButton.draw()
        stayButton.draw()

    playGameButton.draw()
    quitButton.draw()
    messageText.draw()
    bet1Button.draw()
    up1Button.draw()
    down1Button.draw()
    up10Button.draw()
    down10Button.draw()
    betMaxButton.draw()

    creditsText.draw()
    betText.draw()

    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)
