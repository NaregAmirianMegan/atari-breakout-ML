import pygame, os
from pygame.locals import *
import numpy as np
from PIL import Image

from Components import Paddle, Ball, Wall

class Environment:
    def __init__(self, wallDimensions, ballSpeed, paddleSize, paddleSpeed, screen):
        self.score = 0
        self.over = False
        self.wallDimensions = wallDimensions
        self.ballSpeed = ballSpeed
        self.paddleSize = paddleSize
        self.screen = screen

        self.ball = Ball((screen.get_size()[0]-50, screen.get_size()[1]-50), screen, self.ballSpeed)
        self.paddle = Paddle(screen, self.paddleSize, paddleSpeed)
        self.wall = Wall(screen, self.wallDimensions, 10, 10)

        #holding four frames at a time
        self.frameRecord = deque(maxlen=4)
        self.currFrame = 0
        self.kVal = 4

    #return numpy array of uint8 numbers representing a downscaled, grayscaled, cropped game image
    def preprocess(img):
        img = Image.open(img, 'r')
        img = img.convert('L')
        img.save('images/out.jpeg')


    def render(self):
        self.screen.fill((255, 255, 255))
        self.wall.render()
        self.paddle.render()
        self.ball.render()

        pygame.display.update()

    #move game 4 frames forward preprocess and save frame in frame record
    def step(self, moveKey):
        for x in range(self.kVal):
            if(moveKey == 1):
                self.paddle.moveRight()
            elif(moveKey == -1):
                self.paddle.moveLeft()

            gameOver = self.ball.move(self.paddle, self.wall)
            if(gameOver == True):
                self.over = True
                break
            elif(gameOver == 10):
                self.score += 10

            self.currFrame += 1

        self.render()

        imgString = ("images/image"+str(self.currFrame)+".jpeg")
        pygame.image.save(screen, imgString)
        stateFrame = self.preprocess(imgString)
        self.frameRecord.append(stateFrame)
