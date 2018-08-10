import numpy as np
from PIL import Image
import os, sys, random
from collections import deque

import pygame, os
from pygame.locals import *

from Environment import Environment

# print("Loading environment...")
#
# #set window position
# x = 500
# y = 100
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
#
# #setup pygame
# pygame.init()
#
# #set game constants
# #set window size
# WINDOW_HEIGHT = 150
# WINDOW_WIDTH = 250
#
# #create pygame display and frame clock
# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption('Environment Display')
#
# env = Environment((4, 4), 1.75, 50, 2.5, screen)
#
# for x in range(40):
#     env.step(0)


def preprocess(img):
    #greyscale
    img = np.asarray(Image.open(img))
    img = np.mean(img, axis=2).astype(np.uint8)

    #resize
    img = img[::2, ::2]

    return img

class State():
    def __init__(self, de):
        #numpy array with shape (75, 125, 4) created from input deque
        self.data = np.dstack((de[0], de[1], de[2], de[3]))

    def normalize(self):
        #cast as float and divide each element in the array by 255 for input to the network
        return np.true_divide(self.data, 255)

appendArr = preprocess('images/image0.jpeg')

de = deque(maxlen=4)
for x in range(4):
    de.append(appendArr)

state = State(de)
print(state.data.nbytes)

#
# def saveImgToView(img):
#     im = Image.fromarray(np.uint8(img))
#     im.save('images/out.jpeg')
#
# example = preprocess('images/image0.jpeg')
# print(example.shape)
#
#
# # saveImgToView(preprocess('images/image0.jpeg'))
#
#
# class CircularBuffer:
#     def __init__(self, size):
#         self.data = [None] * size
#         self.size = size
#         self.currIndex = 0
#         self.full = False
#
#     def append(self, element):
#         if(self.currIndex == self.size):
#             self.full = True
#             self.currIndex = 0
#         self.data[self.currIndex] = element
#         self.currIndex += 1
#
#     def random_sample(self, batch_size):
#         sample = [None] * batch_size
#         for x in range(batch_size):
#             if(self.full):
#                 sample[x] = self.data[random.randint(0, self.size-1)]
#             else:
#                 sample[x] = self.data[random.randint(0, self.currIndex)]
#
# buffer = CircularBuffer(5)
#
# for x in range(10):
#     buffer.append(x)
#     print(buffer.data)
#
# print("------------------------")
#
# de = deque(maxlen=5)
#
# for y in range(10):
#     de.append(y)
#     print(de)
