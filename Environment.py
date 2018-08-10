import pygame, os, random
import numpy as np
from collections import deque
from pygame.locals import *
from PIL import Image

from Components import Paddle, Ball, Wall

class State():
    def __init__(self, de):
        #numpy array with shape (75, 125, 4) created from input deque
        self.data = np.concatenate((de[0], de[1], de[2], de[3]), axis=2)

    def normalize(self):
        #cast as float and divide each element in the array by 255 for input to the network
        return np.true_divide(self.data, 255)

class Environment:
    def __init__(self, wallDimensions, ballSpeed, paddleSize, paddleSpeed, screen):
        self.cumScore = 0
        self.wallDimensions = wallDimensions
        self.ballSpeed = ballSpeed
        self.paddleSize = paddleSize
        self.paddleSpeed = paddleSpeed
        self.screen = screen

        randomSpawnLoc = self.genRandomSpawnLoc()
        self.ball = Ball(randomSpawnLoc, screen, self.ballSpeed)
        self.paddle = Paddle(screen, self.paddleSize, paddleSpeed)
        self.wall = Wall(screen, self.wallDimensions, 10, 10)

        #holding four frames at a time
        self.frameRecord = deque(maxlen=4)
        self.currFrame = 0
        self.kVal = 4

    def genRandomSpawnLoc(self):
        x = random.randint(10, self.screen.get_size()[0]-10)
        y = random.randint(self.screen.get_size()[1]/2 + 10, self.screen.get_size()[1]-30)

        return (x, y)

    #return numpy array of uint8 numbers representing a downscaled, grayscaled, cropped game image
    def preprocess(self, img):
        #greyscale
        img = np.asarray(Image.open(img))
        img = np.mean(img, axis=2).astype(np.uint8)

        #resize
        img = img[::2, ::2]

        return img

    def render(self):
        self.screen.fill((255, 255, 255))
        self.wall.render()
        self.paddle.render()
        self.ball.render()

        pygame.display.update()

    #move game forward a total of 16 frames saving and preprocessing every 4th frame
    #and return a state object along with its associated reward and whether or not
    #the state is terminal
    def step(self, moveKey):
        reward = None
        terminal = False
        for x in range(self.kVal):
            for x in range(4):
                if(moveKey == 2):
                    self.paddle.moveRight()
                elif(moveKey == 0):
                    self.paddle.moveLeft()

                result = self.ball.move(self.paddle, self.wall)
                gameWon = (self.wall.bricksLeft == 0)

                if(result == True): #game lost
                    reward = -1
                    terminal = True
                    break
                if(gameWon): #all bricks eliminated
                    reward = 1
                    terminal = True
                    break
                elif(result == 10): #hit a brick but game is not over
                    reward = 1
                    terminal = False
                    self.cumScore += 1

                self.currFrame += 1

            self.render()

            imgString = ("images/image"+str(self.currFrame)+".jpeg")
            pygame.image.save(self.screen, imgString)
            stateFrame = self.preprocess(imgString)
            self.frameRecord.append(stateFrame)
            os.remove(imgString)

            if(terminal):
                break

        return State(self.frameRecord), reward, terminal

    def reset(self):
        self.__init__(self.wallDimensions, self.ballSpeed, self.paddleSize, self.paddleSpeed, self.screen)
