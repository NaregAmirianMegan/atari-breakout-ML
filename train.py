import random, os
import numpy as np
from PIL import Image

from keras.layers import Conv2D, Dense, Flatten
from keras.optimizers import RMSprop

import pygame, os
from pygame.locals import *

from Environment import Environment, State

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


class DeepQAgent():
    def __init__(self):
        self.EPSILON = 1.0
        self.EPSILON_DECAY = 0.99995
        self.EPSILON_BASELINE = 0.1

        self.GAMMA = 0.85

        self.LR = 0.00025

        self.experience_replay = CircularBuffer(250000)

        self.model = self.createModel()
        self.target_model = self.createModel()

    def createModel(self):
        model = Sequential()

        model.add(Conv2D(16, kernel_size=(8, 8), strides=(4, 4), activation='relu',
                            input_shape=(75, 125, 4), data_format='channels_last'))
        model.add(Conv2D(32, kernel_size=(4, 4), strides=(2, 2), activation='relu'))
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(3))

        optimizer = RMSprop(lr=self.LR, rho=0.95, epsilon=0.01)
        model.compile(optimizer, loss='mse')

        return model

    def record(self, state, action, reward, new_state, terminal):
        self.experience_replay.append((state, action, reward, new_state, terminal))

    def train(self, batch_size):
        if(self.experience_replay.currIndex <= batch_size and self.experience_replay.full == False):
            return

        batch = self.experience_replay.random_sample(batch_size)

        for game_step in batch:
            state, action, reward, new_state, terminal = game_step

            #######PLAYER
            target_q_vals = self.target_model.predict(state)

            #if game is over
            if(terminal):
                #target q val is simply the reward received for the action to get to the terminal state
                target_q_vals[0][action] = reward
            else:
                #else add future discounted reward
                Q_future = max(self.target_model.predict(new_state_input)[0])
                target_q_vals[0][action] = reward + Q_future * self.GAMMA

            self.model.fit(state, target_q_vals, epochs=1, verbose=0)

    def updateTargetModel(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_model.set_weights(target_weights)

    def act(self, state):
        #set epsilon coefficient
        self.EPSILON *= self.EPSILON_DECAY
        self.EPSILON = max(self.EPSILON_BASELINE, self.EPSILON)

        if np.random.random() < self.EPSILON:
            return np.random.random_integers(0, 2)
        else:
            return np.argmax(self.model.predict(state)[0])

    def saveModel(self):
        self.model.save('Atari-Breakout-Master.h5')

def workout(episodes, max_episode_length):
    DeepQAgent = DeepQAgent()

    print("Loading environment...")

    x = 500
    y = 100
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
    pygame.init()
    WINDOW_HEIGHT = 150
    WINDOW_WIDTH = 250

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Environment Display')

    env = Environment((4, 4), 1.75, 50, 2.5, screen)

    for episode in range(episodes):
        env.reset()

        curr_state, _, __, = env.step(1)

        print("Episode:", episode, "/", episodes)
        print("Epsilon: ", DeepQAgent.EPSILON)

        for step in range(max_episode_length):

            action = DeepQAgent.act(curr_state)
            new_state, reward, terminal = env.step(action)

            DeepQAgent.record(state, action, reward, new_state, terminal)

            DeepQAgent.train(32)
            DeepQAgent.updateTargetModel()

            if(terminal):
                break
            else:
                curr_state = new_state

        print("Score:", env.cumScore)

    DeepQAgent.saveModel()

workout(2000)
