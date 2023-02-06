import pygame
import random
from Constants import *
import pygwidgets
import time


class Snake():

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    HEAD = 0

    def __init__(self, window, oApple):
        self.window = window
        self.oApple = oApple
        self.reset()
        self.biteSound = pygame.mixer.Sound('sounds/bite.wav')

    def reset(self):
        self.x = random.randint(5, N_CELLS_WIDE - 6)
        self.y = random.randint(5, N_CELLS_HIGH - 6)
        self.direction = Snake.RIGHT
        self.snakeCoordinates = [{'x': self.x, 'y': self.y},{'x': self.x - 1, 'y': self.y}, {'x': self.x - 2, 'y': self.y}]
 
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.direction != Snake.RIGHT:
                self.direction = Snake.LEFT
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.direction != Snake.LEFT:
                self.direction = Snake.RIGHT
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.direction != Snake.DOWN:
                self.direction = Snake.UP
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.direction != Snake.UP:
                self.direction = Snake.DOWN
       
    def update(self):
        appleX, appleY = self.oApple.getLocation()
        snakeHeadX = self.snakeCoordinates[Snake.HEAD]['x']
        snakeHeadY = self.snakeCoordinates[Snake.HEAD]['y']

        if snakeHeadX == appleX and snakeHeadY == appleY:  # Ate the apple!
            self.oApple.setNewLocation()
            self.biteSound.play()
        else:
            del self.snakeCoordinates[-1]    # Remove the last segment

        # Determine the new placement for the head based on the direction
        if self.direction == Snake.UP:
            newHead = {'x': snakeHeadX,'y': snakeHeadY - 1}
        elif self.direction == Snake.DOWN:
            newHead = {'x': snakeHeadX, 'y': snakeHeadY + 1}
        elif self.direction == Snake.LEFT:
            newHead = {'x': snakeHeadX - 1, 'y': snakeHeadY}
        elif self.direction == Snake.RIGHT:
            newHead = {'x': snakeHeadX + 1, 'y': snakeHeadY}
        # Assign the new head position
        self.snakeCoordinates.insert(0, newHead)

    def getScore(self):
        score = len(self.snakeCoordinates) - 3
        return score

    def checkGameOver(self):
        headX = self.snakeCoordinates[Snake.HEAD]['x']
        headY = self.snakeCoordinates[Snake.HEAD]['y']
        if (headX == -1 or headX == N_CELLS_WIDE or
            headY == -1 or headY == N_CELLS_HIGH):
            return GAME_OVER

        # Iterate through all segments to see if head collides with any segment
        for snakeBody in self.snakeCoordinates[1:]:
            if snakeBody['x'] == headX and snakeBody['y'] == headY:
                return GAME_OVER

        return KEEP_GOING

    def draw(self):
        for index, coord in enumerate(self.snakeCoordinates):
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE

            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(self.window, DARKGREEN, wormSegmentRect)
            
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            if index == Snake.HEAD:
                pygame.draw.rect(self.window, TEAL, wormInnerSegmentRect)
            else:
                pygame.draw.rect(self.window, GREEN, wormInnerSegmentRect)