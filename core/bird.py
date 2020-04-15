from pygame import Rect
import numpy as np
from core.obstacles import *

class Bird:

    WIDTH=10
    HEIGHT=10
    JUMP_LIMIT = 60

    def __init__(self, pos):
        self.X = pos[0]
        self.Y = pos[1]
        self.rect = Rect(self.X, self.Y, self.WIDTH, self.HEIGHT)
        self.up_X = 0
        self.moveBy = 7
        self.alive = True
        self.score = 0
        self.moves = 0
        self.fitness_score = 0

    def jump(self):
        if (self.up_X > 0 and self.up_X < self.JUMP_LIMIT):
            return
        self.up_X = 0
        self.moveBy = -abs(self.moveBy)
    
    def move(self):

        self.moves += 1
        if (self.moveBy < 0 and self.up_X >= self.JUMP_LIMIT):
            self.moveBy = abs(self.moveBy)
            self.up_X = 0
        elif (self.moveBy < 0):
            self.up_X += abs(self.moveBy)
        
        # self.X += abs(self.moveBy)
        self.Y += self.moveBy

        self.rect = Rect(self.X, self.Y, self.WIDTH, self.HEIGHT)
    
    def get_rect(self):
        return self.rect
    
    def get_pos(self):
        return (self.X, self.Y, self.WIDTH, self.HEIGHT)

    def inc_score(self):
        self.score += 1
    
    def get_score(self):
        return self.score

    def update_fitness_score(self, state):
        # print("moves", self.moves)
        # print("ospeed", Obstacle.SPEED)
        # print("fitness score", (self.moves*Obstacle.SPEED)*(self.score+1))
        distance_travelled = self.moves * Obstacle.SPEED
        oy_midpoint = (state[1]+state[2]) // 2
        ox_midpoint = (state[0] + state[0]+Obstacle.WIDTH) // 2
        bx_midpoint = (self.X + self.X + self.WIDTH) // 2
        by_midpoint = (self.Y + self.Y + self.HEIGHT) // 2
        x_dist = ox_midpoint - bx_midpoint
        y_dist = oy_midpoint - by_midpoint
        dist = np.sqrt((x_dist ** 2) + (y_dist ** 2))

        self.fitness_score = int(distance_travelled - dist)
        # return (self.moves*Obstacle.SPEED)*(self.score+1)
    
    def get_fitness_score(self):
        return self.fitness_score

    def __lt__(self, b):
        return self.get_fitness_score() < b.get_fitness_score()
    
    def __gt__(self, b):
        return self.get_fitness_score() > b.get_fitness_score()
    
    def set_alive(self, alive):
        self.alive = alive
        if alive:
            self.moves = 0
            self.score = 0
            self.up_X = 0

    def is_alive(self):
        return self.alive