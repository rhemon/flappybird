import numpy as np
from core.game import Game
from .bird import ReinforcedBird
from core.obstacles import *

class QTable:


    VERSION_NAME = "v1"
    FILE_PATH="weights/qlearn-"+VERSION_NAME+".npz"
    LEARNING_RATE = 0.9
    DISCOUNT = 0.99

    EPSILON_DECAY = 0.01

    

    def __init__(self, dimensions):
        print(dimensions)
        try:
            datas = np.load(self.FILE_PATH)
            self.qtable = datas['qtable']
            self.epsilon = datas['epsilon']
        except:
            self.qtable = np.random.uniform(size=(dimensions))
            self.epsilon = 0.99
            
    
    def get_action(self, state):
        if np.random.random() > self.epsilon:
            return np.argmax(self.qtable[state])
        else:
            return np.random.randint(0, 2)

    def update_action(self, next_state, state, action, reward):
        # print(len(state))
        # print(self.qtable.shape)
        # print(state + (action,))
        current_q = self.qtable[(state + (action,))]
        max_future_q = np.max(self.qtable[next_state])
        new_q = (1 - self.LEARNING_RATE) * current_q + self.LEARNING_RATE * (reward + self.DISCOUNT * max_future_q)

        self.qtable[(state + (action,))] = new_q
    
    def decay_epsilon(self):
        self.epsilon -= self.EPSILON_DECAY

    def save_qtable(self, rewards, episode):
        try:
            os.remove(self.FILE_PATH)
        except:
            np.savez(self.FILE_PATH, qtable=self.qtable, epsilon=self.epsilon, rewards=rewards, episode=episode)
    
class ReinforcedTrainer(Game):

    ACITONS = 2 # (Not Jump, Jump)

    def __init__(self):
        super().__init__()

        self.bird = ReinforcedBird(self.INIT_BIRD_POS)

        ## MAKINGS EACH BIN SIZE BY VALUES BIRD AND OBSTACLE MOVE BY
        ## SO BASICALLY HERE AS BOTH MOVE BY are 7
        ## EACH BIN SIZE is 7. so there 0 - HIGHT or WIDTH, 
        ## X_DELTA_BINS is 115
        ## Y_DELTA_BINS is 57
        ## SO HERE Y_DELTA_BINS and Y_BINS
        
        self.BINS_SCALE = ((0, ReinforcedBird.INIT_MOVE_BY), (0, Obstacle.SPEED), (self.HEIGHT, ReinforcedBird.INIT_MOVE_BY))
        Y_DELTA_BINS = ((self.HEIGHT // self.BINS_SCALE[0][1])+1)*2
        X_DELTA_BINS = ((self.WIDTH // self.BINS_SCALE[1][1] ) + 1)
        Y_BINS = ((self.HEIGHT // self.BINS_SCALE[2][1] ) + 1)
        self.BINS = (Y_BINS, X_DELTA_BINS, Y_DELTA_BINS, self.ACITONS)
        self.qtable = QTable(self.BINS)

        datas = np.load(QTable.FILE_PATH)
        self.rewards, self.cur_episode = datas['rewards'], datas['episode']

        self.round = 1
        self.ep_dec_every = 1_000
        self.prev_score = 0
        self.show_every = 5

    def get_distinct_bin(self, index, value):
        value += self.BINS_SCALE[index][0]
        b = value // self.BINS_SCALE[index][1]

        return b
    
    def get_state_bins(self):
        state = self.bird.get_input(self.get_state())[1:]
        bins = ()
        for i in range(len(state)):
            bins += (self.get_distinct_bin(i, state[i]),)
        return bins


    def bird_update(self):
        self.cur_state = self.get_state_bins()
        if not self.bird.in_jump():
            self.action = self.qtable.get_action((self.cur_state[0], self.cur_state[1], self.cur_state[2]))
            self.acted = True
            self.bird.jump(self.action)
        else:
            self.acted = False
        return super().bird_update()

    def reward_action(self):
        if self.bird.get_score() > self.prev_score:
            self.prev_score = self.bird.get_score()
            return 20
        if self.bird.is_alive:
            return -1
        return -20

    # def bird_draw(self):
    #     if (not self.round % self.show_every):
    #         super().bird_draw()

    # def obstacles_draw(self):
    #     if (not self.round % self.show_every):
    #         super().obstacles_draw()
    #     self.add_status_label("Learning...", self.HEIGHT-10)
    
    def play(self):
        super().play()
        if self.acted:

            reward = self.reward_action()

            self.next_state = self.get_state_bins()

            self.qtable.update_action((self.next_state[0], self.next_state[1], self.next_state[2]),
                                    (self.cur_state[0], self.cur_state[1], self.cur_state[2]),
                                    self.action, reward)

            self.cur_episode += 1

            if not self.cur_episode % self.ep_dec_every:
                self.qtable.decay_epsilon()
            self.qtable.save_qtable(self.rewards, self.cur_episode)
    
    def check_jump(self, event):
        return

    def end_game(self):
        self.round += 1
        self.bird.set_alive(True)
        self.reset_obstacles()