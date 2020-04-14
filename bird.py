
from pygame import Rect
import numpy as np
from obstacles import *

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

class Chromosome:

    def __init__(self, weights=None):
        self.bias2 = 0
        if weights:
            self.w1 = weights[0]
            self.w2 = weights[1]
            self.bias1 = weights[2]
            # self.bias2 = weights[3]
        else:    
            self.w1 = np.random.random((8, 4))
            self.w2 = np.random.random((1, 8))
            self.bias1 = np.random.uniform()
            # self.bias2 = np.random.uniform()
    
    def get_decision(self, state):
        # print("w1", self.w1)
        # print("w2", self.w2)
        # print("bias", self.bias1)
        # print(state)
        state = state.reshape(state.shape[0],1)
        l1 = np.dot(self.w1, state) + self.bias1
        l1 = 1 / (1 + np.exp(-l1)) 
        # print(l1)
        l2 = np.dot(self.w2, l1) # + self.bias2
        out = 1 / (1 + np.exp(-l2))
        # out = 
        if out[0] > 0.9:
            return True
        return False

    def get_w1(self):
        return self.w1
    
    def get_w2(self):
        return self.w2

    def get_bias1(self):
        return self.bias1
    
    def get_bias2(self):
        return self.bias2
    
    def weight_crossover(wa, wb):
        if wa.shape != wb.shape:
            raise Exception("Weight dimensions must be equal for a crossover")
        
        x = round(np.random.rand() * wa.shape[0])
        wa_ = np.zeros(wa.shape)
        
        prob = np.random.rand()
        if (prob < 0.5):
            wa_[:x][:] = wa[:x][:]
            wa_[x:][:] = wb[x:][:]
        else:
            wa_[:x][:] = wb[:x][:]
            wa_[x:][:] = wa[x:][:]    
        
        return wa_

    def crossover(gene1, gene2):
        w1a = Chromosome.weight_crossover(gene1.get_w1(), gene2.get_w1())
        w2a = Chromosome.weight_crossover(gene1.get_w2(), gene2.get_w2())
        if np.random.rand() < 0.5:
            bias = gene1.get_bias1()
        else:
            bias = gene2.get_bias1()
        
        return Chromosome([w1a, w2a, bias, 0])
        
    def weight_mutate(w):
        # mutator = np.random.rand(w.shape[0], w.shape[1])
        # prob = lambda: (np.random.rand(w.shape[0], w.shape[1]) < 0.5).astype('int')
        # w *= mutator * prob() + mutator*prob()*-1
        w += np.random.normal(scale=1)
        return w
    
    def mutate(self):
        self.w1 = Chromosome.weight_mutate(self.w1)
        self.w2 = Chromosome.weight_mutate(self.w2)
    
class BirdWithGenes(Bird):
    
    def __init__(self, pos, genes=None):
        super().__init__(pos)
        self.init_pos = pos
        if genes:
            self.genes = genes
        else:
            self.genes = Chromosome()

    def jump(self, state):
        state.insert(0, self.Y)
        if self.genes.get_decision(np.asarray(state)):
            super().jump()
    
    def set_init_pos(self):
        self.X = self.init_pos[0]
        self.Y = self.init_pos[1]

    def set_alive(self, alive):
        super().set_alive(alive)
        if alive:
            self.set_init_pos()

    def get_genes(self):
        return self.genes

    def offspring(self, b):
        gene1 = Chromosome.crossover(self.genes, b.get_genes())
        gene1.mutate()
        newbird = BirdWithGenes(self.init_pos, gene1)
        return newbird