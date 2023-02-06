import sys, pygame
from Constants import *
from Game import *

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake game')
GAME_FONT = 'freesansbold.ttf'

oGame = Game(window, GAME_FONT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        oGame.handleEvent(event)

    oGame.update()

    oGame.draw()

    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)