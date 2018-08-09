import pygame, os
from pygame.locals import *

from Components import Paddle, Ball, Wall

class Game:
    def __init__(self, wallDimensions, ballSpeed, paddleSpeed, paddleSize, initialScore):
        self.score = initialScore
        self.over = False
        self.wallDimensions = wallDimensions
        self.ballSpeed = ballSpeed
        self.paddleSpeed = paddleSpeed
        self.paddleSize = paddleSize
        self.font = pygame.font.SysFont('Comic Sans MS', 29)

    def run(self, screen):
        ball = Ball((50, 100), screen, self.ballSpeed)
        paddle = Paddle(screen, self.paddleSize, self.paddleSpeed)
        wall = Wall(screen, self.wallDimensions, 10, 5)

        leftPressed = False
        rightPressed = False

        screen.fill((255, 255, 255))

        i = 0

        clock = pygame.time.Clock()

        while(not self.over):

            clock.tick(60)

            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    quit()
                elif(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_RIGHT):
                        rightPressed = True
                    elif(event.key == pygame.K_LEFT):
                        leftPressed = True
                elif(event.type == pygame.KEYUP):
                    if(event.key == pygame.K_RIGHT):
                        rightPressed = False
                    elif(event.key == pygame.K_LEFT):
                        leftPressed = False

            if(rightPressed):
                paddle.moveRight()
            elif(leftPressed):
                paddle.moveLeft()

            screen.fill((255, 255, 255))

            wall.render()

            paddle.render()

            gameOver = ball.move(paddle, wall)
            if(gameOver == True):
                self.over = True
            elif(gameOver == 10):
                self.score += 10
                #print(self.score)

            ball.render()

            pygame.display.update()
            if(i%4 == 0):
                pygame.image.save(screen, "images/image"+str(i)+".jpeg")
                #print(clock.get_fps())

            i += 1
