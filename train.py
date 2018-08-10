import random, os
import numpy as np
from PIL import Image

from keras.layers import Conv2D, Dense, Flatten
from keras.optimizers import RMSprop

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


class DeepQNetwork():
    def __init__(self):
        self.EPSILON = 1.0
        self.EPSILON_DECAY = 0.99995
        self.EPSILON_BASELINE = 0.1

        self.GAMMA = 0.85

        self.LR = 0.00025

        self.experience_replay = CircularBuffer(1000000)

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
        if(len(self.experience_replay) < batch_size):
            return

        batch = random.sample(self.experience_replay, batch_size)

        for game_step in batch:
            state, player, action, reward, new_state, terminal = game_step

            #######PLAYER
            target_q_vals = self.target_model.predict(state_input)

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

    def act(self, state, player):
        #set epsilon coefficient
        self.EPSILON *= self.EPSILON_DECAY
        self.EPSILON = max(self.EPSILON_BASELINE, self.EPSILON)

        if np.random.random() < self.EPSILON:
            #print("RANDOM")
            #select random action
            return np.random.random_integers(0, 8)
        else:
            #print("MODEL CHOSEN")
            #select action based on the model
            input = self.formatInput(state, player)
            return np.argmax(self.model.predict(input)[0])

    def saveModel(self):
        self.model.save('3TGod.h5')

def getAction(ID):
    if(ID < 3):
        x = 0
        y = ID
    elif(ID < 6):
        x = 1
        y = ID - 3
    else:
        x = 2
        y = ID - 6

    return Action(x, y)

def workout(episodes):

    max_episode_length = 100

    DeepQAgent = DeepQNetwork()

    switch_player = True

    curr_state = State()
    curr_player = 2

    step_count_list = []

    for episode in range(episodes):
        curr_state.reset()

        print("Episode: ", episode)
        print("Epsilon: ", DeepQAgent.EPSILON)
        if(len(step_count_list) > 0):
            step_avg = sum(step_count_list)/len(step_count_list)
        else:
            step_avg = 0
        #print("Game length avg: ", step_avg)

        step_count = 0

        for step in range(max_episode_length):
            step_count += 1

            action = getAction(DeepQAgent.act(curr_state, curr_player))
            new_state = curr_state.update(curr_player, action)

            #Illegal move
            if(new_state == False):
                switch_player = False
                reward = -1
                new_state = curr_state
                terminal = False
            #Legal move
            else:
                switch_player = True
                reward, terminal = new_state.reward(curr_player)

            # curr_qvals = DeepQAgent.model.predict(DeepQAgent.formatInput(curr_state, curr_player))
            # q_max = max(curr_qvals[0])
            # max_move = getAction(np.argmax(curr_qvals))

            # print("Reward: ", reward, " For ", curr_player)
            #print("MaxQval: ", q_max, " For (", max_move.x, ", ", max_move.y, ")")

            #new_state.show()

            DeepQAgent.record(curr_state, curr_player, action, reward, new_state, terminal)

            DeepQAgent.train(20)
            DeepQAgent.updateTargetModel()

            if(terminal):
                step_count_list.append(step_count)
                # if(reward == 1):
                #     print("WINNER: ", curr_player)
                # else:
                #     print("TIE")
                break
            else:
                curr_state = new_state
                if(switch_player):
                    curr_player *= -1

    DeepQAgent.saveModel()

workout(2000)
