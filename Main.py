import pygame, os
from pygame.locals import *

from Game import Game

print("Game loading...")

#set window position
x = 500
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#setup pygame
pygame.init()
#setup text font
pygame.font.init()

#set game constants
#set window size
WINDOW_HEIGHT = 150
WINDOW_WIDTH = 250

#create pygame display and frame clock
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game Window')

game1 = Game((4, 4), 1.75, 2.5, 50, 0)
game1.run(screen)
