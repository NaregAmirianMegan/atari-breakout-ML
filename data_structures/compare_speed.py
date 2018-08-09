"""
Compare the speed of python's deque data structure versus other data structures.

Compare:
- append speed
- remove speed
- random selection speed
"""

import time, random
import numpy as np
from PIL import Image
from collections import deque

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

        return sample

def preprocess(img):
    #greyscale
    img = np.asarray(Image.open(img))
    img = np.mean(img, axis=2).astype(np.uint8)

    #resize
    img = img[::2, ::2]

    return img

def test_append_speed_deque(appendNumber, size):
    de = deque(maxlen=size)

    s = preprocess('../images/image0.jpeg')
    a = 0
    r = 0
    sp = s
    t = False

    start = time.time()

    for x in range(appendNumber):
        de.append((s, a, r, sp, t))

    end = time.time()
    return (end - start), de

def test_append_speed_buffer(appendNumber, size):
    buffer = CircularBuffer(size)

    s = preprocess('../images/image0.jpeg')
    a = 0
    r = 0
    sp = s
    t = False

    start = time.time()

    for x in range(appendNumber):
        buffer.append((s, a, r, sp, t))

    end = time.time()
    return (end - start), buffer


def test_random_selection_speed_deque(deque, samples, sampleSize):
    start = time.time()

    for x in range(samples):
        samp = random.sample(deque, sampleSize)

    end = time.time()
    return end - start

def test_random_selection_speed_buffer(buffer, samples, sampleSize):
    start = time.time()

    for x in range(samples):
        samp = buffer.random_sample(sampleSize)

    end = time.time()
    return end - start



appends = 1500000
structureSize = 1000000
SAMPLES = 500000
SAMPLESIZE = 32

print("---------------DEQUE TEST--------------")

time1, deque = test_append_speed_deque(appends, structureSize)
print("Append", appends, "items to", structureSize, "size deque:", time1, "seconds")

time2 = test_random_selection_speed_deque(deque, SAMPLES, SAMPLESIZE)
print(SAMPLES, "random samples of", SAMPLESIZE, "each:", time2, "seconds")

print("TOTAL TIME: ", str(time1+time2), "seconds")

print("--------------BUFFER TEST--------------")

time3, buffer = test_append_speed_buffer(appends, structureSize)
print("Append", appends, "items to", structureSize, "size deque:", time3, "seconds")

time4 = test_random_selection_speed_buffer(buffer, SAMPLES, SAMPLESIZE)
print(SAMPLES, "random samples of", SAMPLESIZE, "each:", time4, "seconds")

print("TOTAL TIME: ", str(time3+time4), "seconds")
