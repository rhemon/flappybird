"""
Provides classes to run the game and train the bird to play the game
using concepts of reinforced learning

@author Ridhwanul Haque
@version 21.04.2020
"""

import os
import sys


import numpy as np
import pygame

from core.bird import Bird
from core.game import Game
from core.obstacles import *


class QTable:
    """
    Maintains the qtable,
    updates the qtable,
    contains basic hyperparamters of the learning iteraiton.
    """

    VERSION_NAME = "xy-v6"
    FILE_PATH="weights/qlearn-"+VERSION_NAME+".npz"
    LEARNING_RATE = 0.1
    DISCOUNT = 1

    EPSILON_DECAY = 0.1 ## why need it when we are randomly generating the pipes 

    
    def __init__(self, dimensions):
        try:
            datas = np.load(self.FILE_PATH)
            self.qtable = datas['qtable']
            # #print("this? ")
        except FileNotFoundError:
            self.qtable = np.zeros((dimensions)) 
            # #print(self.qtable)
        self.epsilon = 0
    
    def get_action(self, state):
        """
        Pick best action or a random action.
        Probability depends on epsilon
        """
        # #printself.epsilon)
        if np.random.random() > self.epsilon:
            return np.argmax(self.qtable[state])
        else:
            return np.random.randint(0, 2)
    
    def decay_epsilon(self):
        if self.epsilon > 0.09:
            self.epsilon -= self.EPSILON_DECAY

    def save_qtable(self):
        try:
            os.remove(self.FILE_PATH)
        except FileNotFoundError:
            pass
        np.savez(self.FILE_PATH, qtable=self.qtable)

    def update_state(self, state, action, reward, new_state):
        future_q = np.max(self.qtable[new_state])
        old_q = self.qtable[(state + (action,))]
        new_q = (1.0-self.LEARNING_RATE) * old_q + self.LEARNING_RATE * ((reward + (self.DISCOUNT * future_q)))
        self.qtable[state+(action,)] = new_q

    def reset_epsilon(self):
        if self.epsilon == 0:
            self.epsilon = 0.0
        else:
            self.epsilon = 0
    
    def decay_lr(self):
        return
        # self.LEARNING_RATE -= 0.01

    def set_state(self, state, value):
        self.qtable[state] = value
                
class ReinforcedTrainer(Game):
    """
    Game that uses the QTable to determine whether to jump or not.
    Doesn't render instead trains in the back.
    Uses a different extension to make it render once in between the
    learning iterations.
    """

    ACITONS = 2 # (Not Jump, Jump)

    DEATH_PENALTY = -100
    ALIVE_REWARD = 0
    SCORE_REWARD = 1

    REWARDS_HISTORY_FILE = "weights/qlearn-"+QTable.VERSION_NAME+"-rewards.npz"
    
    def __init__(self, ep = -1):
        super().__init__()
        self.bird = Bird(self.INIT_BIRD_POS)
        
        # After tinkering around the bin size for states
        # seemed best to break y values into bird's height value
        # and break the x values by obstacle's width value
        self.BINS_SCALE = ((0,Bird.HEIGHT), (0, Obstacle.WIDTH), (0, Bird.HEIGHT), (0, Bird.HEIGHT))
        Y_BIN_SIZE = ((self.HEIGHT // self.BINS_SCALE[0][1]))+2 ## taking of the border case to avoid -1
        X_OBS_BIN_SIZE = ((self.WIDTH // self.BINS_SCALE[1][1]))+2
        self.BINS = (Y_BIN_SIZE, X_OBS_BIN_SIZE, Y_BIN_SIZE, Y_BIN_SIZE, self.ACITONS)
        
        self.qtable = QTable(self.BINS)
        self.render = True
        
        self.cur_episode = 1
        try:
            data = np.load(self.REWARDS_HISTORY_FILE)['rewards']
            self.rewards_history = list(map(list, list(data)))
            self.cur_episode = data[0][-1]+1
        except:
            self.rewards_history = [[], [], [], [], [], [], []]
        
        if ep != -1:
            self.cur_episode = ep
        
        # use to determine whether last action was complete or not
        self.state_update = False

        self.eps_dec_every = 100
        self.show_every = 1000
        self.reset_eps_every = 500
        self.lr_decay_every = 2000
        self.reset_eprew_every = 50

        self.reward = 0
        self.wait_speed = 1
        
        self.scores = []
        self.episode_rewards = []
        self.ep_reward = 0
        self.cur_round_states = [] # (state, action, reward, new_state)

        self.debug_count = 0

        pygame.display.set_caption("QLearning LR:"+str(QTable.LEARNING_RATE)+", DISCOUNT:" + str(QTable.DISCOUNT) + ", eps swap, lr decay")

    def check_jump(self, event):
        """
        Overwriting to avoid jump caused by space press
        """
        return

    def get_distinct_bin(self, index, value):
        """
        Using value to get the distin bin it should be in
        """

        value += self.BINS_SCALE[index][0]
        b = value // self.BINS_SCALE[index][1]
        return b+1 # adding one to avoid -1

    def get_state(self):
        """
        Overwriting pervious to give x, y1, y2
        of the upcoming obstacle.
        Just to make the states more specific, which
        isn't very clear with the distance as state
        values.
        If none, returns None
        """

        for i in range(len(self.obstacles)):
            each = self.obstacles[i]
            if not each.did_pass():
                x = each.get_X()
                y1 = each.get_Y1()
                y2 = each.get_Y2()
                return [x, y1, y2]

    def get_state_bins(self):
        """
        Returns the bin found from 
        (BirdX, ObsX, ObsY1, ObsY2)
        """
        
        states = self.get_state()
        states.insert(0, self.bird.get_pos()[1])
        
        bins = ()
        for i in range(len(states)):
            bins += (self.get_distinct_bin(i, states[i]),)
        
        return bins

    def bird_check(self):
        """
        Check if bird alive, dead or scored
        Set reward accordingly
        If scored, returns True
        If dead returns False
        If just alive returns None
        Along with that returns true if death was caused by
        upper pipe.
        """

        alive, self.death_by_upper = super().bird_check()
        #print"alive", alive)
        if not alive and not alive == None:
            self.state_update = True
            self.reward = self.DEATH_PENALTY
        elif alive:
            self.reward = self.SCORE_REWARD
        else:
            self.reward = self.ALIVE_REWARD
        
        #print"reward set to ", self.reward)
        return alive, None

    def bird_update(self):
        """
        If bird is in jump, then state shouldnt updated as it
        was effect of last one.
        Otherwise check current state and take action.
        """

        if not self.bird.in_jump():
            # #print("TOok action")
            # self.state_update = True 
            self.cur_state = self.get_state_bins()
            # #print(self.cur_state)
            self.action = self.qtable.get_action((self.cur_state))
            if self.action == 1:
                self.bird.jump()
        else:
            self.state_update = False
        game = super().bird_update()
        if not self.bird.in_jump():
            self.state_update = True
        return game
    
    def extra_draw(self):
        self.draw_grid()

    def draw_grid(self):
        """
        Drawing a grid to display the different 
        states.
        """

        x_scale = self.BINS_SCALE[1][1]
        y_scale = self.BINS_SCALE[0][1]
        x_now = x_scale
        while x_now < self.WIDTH+x_scale:
            r = pygame.Rect(x_now, 0, 1, self.HEIGHT)
            pygame.draw.rect(self.display, self.BLACK, r)
            x_now += x_scale
        y_now = y_scale
        while y_now < self.WIDTH+y_scale:
            r = pygame.Rect(0, y_now, self.WIDTH, 1)
            pygame.draw.rect(self.display, self.BLACK, r)
            y_now += y_scale
    
    def play(self, wait_speed=1):
        """
        Play turn. If state should update
        add to states list to later
        use to learn qtable valeus
        """

        game = super().play(self.wait_speed)
        if self.state_update:
            self.ep_reward += self.reward
            self.new_state = self.get_state_bins()
            self.cur_round_states.append((self.cur_state, self.action, self.reward, self.new_state))
            self.state_update = False 
        
        return game

    def end_game(self):
        """
        Update the table and reset episode values
        as per iteration values set initially.
        """

        ### IF DEATH BY UPPER PIPE SEt LAST JUMP REWARD TO DEATH PENALTY AS WELL
        if self.death_by_upper:
            for i in range(len(self.cur_round_states)-1, -1, -1):
                if self.cur_round_states[i][1] == 1:
                    self.cur_round_states[i] = (self.cur_round_states[i][0], 1, self.DEATH_PENALTY, self.cur_round_states[i][3])
                    break

        self.qtable.set_state(self.cur_round_states[-1][0]+(self.cur_round_states[-1][1],), self.DEATH_PENALTY)
        for i in range(len(self.cur_round_states)-2, -1, -1):
            self.qtable.update_state(*self.cur_round_states[i])

        self.qtable.save_qtable()

        # Later use to track the learning progress
        self.scores.append(self.bird.get_score())
        self.episode_rewards.append(self.ep_reward)

        if not (self.cur_episode) % self.reset_eprew_every:
            min_re = min(self.episode_rewards)
            max_re = max(self.episode_rewards)
            avg_re = np.mean(self.episode_rewards)
            min_s = min(self.scores)
            max_s = max(self.scores)
            avg_s = np.mean(self.scores)
            self.rewards_history[0].append(self.cur_episode-1)
            self.rewards_history[1].append(min_re)
            self.rewards_history[2].append(max_re)
            self.rewards_history[3].append(avg_re)
            self.rewards_history[4].append(min_s)
            self.rewards_history[5].append(max_s)
            self.rewards_history[6].append(avg_s)

            self.episode_rewards = []
            self.scores = []
            print(f"Episode: {self.cur_episode}, avg re: {avg_re}, epsilon: {self.qtable.epsilon}, ......")
            
            self.update_plot()

        # Decay or reset epsilon or learning rate to improve learning
        if not (self.cur_episode) % self.eps_dec_every:
            self.qtable.decay_epsilon()
        if not self.cur_episode % self.reset_eps_every:
            self.qtable.reset_epsilon()
        if not self.cur_episode % self.lr_decay_every:
            self.qtable.decay_lr()
        
        self.cur_episode += 1
        self.bird.set_alive(True)
        self.reset_obstacles()
        self.ep_reward = 0     

    def update_plot(self):
        """
        Save rewards and score values for using later
        to analyse the progress.
        """

        retry = True
        while retry:
            try:
                os.remove(self.REWARDS_HISTORY_FILE)
                retry = False
            except FileNotFoundError:
                retry = False
                pass
            except PermissionError:
                pass
            
        np.savez(self.REWARDS_HISTORY_FILE, rewards=self.rewards_history)
