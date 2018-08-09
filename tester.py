import numpy as np
from PIL import Image
import os
from collections import deque
import random

#
# def preprocess(img):
#     #greyscale
#     img = np.asarray(Image.open(img))
#     img = np.mean(img, axis=2).astype(np.uint8)
#
#     #resize
#     img = img[::2, ::2]
#
#     return img
#
# def saveImgToView(img):
#     im = Image.fromarray(np.uint8(img))
#     im.save('images/out.jpeg')
#
#
# saveImgToView(preprocess('images/image0.jpeg'))


class CircularBuffer:
    def __init__(self, size):
        self.data = [None] * size
        self.size = size
        self.currIndex = 0
        self.full = False

    def append(self, element):
        if(self.currIndex == self.size):
            self.full = True
            self.currIndex = 0
        self.data[self.currIndex] = element
        self.currIndex += 1

    def random_sample(self, batch_size):
        sample = [None] * batch_size
        for x in range(batch_size):
            if(self.full):
                sample[x] = self.data[random.randint(0, self.size-1)]
            else:
                sample[x] = self.data[random.randint(0, self.currIndex)]

buffer = CircularBuffer(5)

for x in range(10):
    buffer.append(x)
    print(buffer.data)

print("------------------------")

de = deque(maxlen=5)

for y in range(10):
    de.append(y)
    print(de)
