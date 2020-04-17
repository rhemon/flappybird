"""
This file provides the GeneticBird and Genes class.

They mainly handle all data related to bird and genes
for deciding whether to jump or not.

@author Ridhwanul Haque
@version 15.04.2020
"""

import numpy as np
from pygame import Rect

from core.bird import *
from core.obstacles import *


class Genes:
    """
    This class is basically the model to deicde
    whether bird jump or not.
    In GA terms, this is probably the choromosome or one with 
    genes.
    """

    THRESHOLD = 0.6

    def __init__(self, weights=None):
        """
        If weights provided then use that
        else initialise randomly.
        """

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
            # self.bias2 = np.random.uniform()#
            self.mutate()
    
    def get_decision(self, state):
        """
        Forward calculate the output and decide whehter to jump or not.
        Uses threshold to determine it.
        """

        state = state.reshape(state.shape[0],1)
        l1 = np.dot(self.w1, state) + self.bias1
        l1 = 1 / (1 + np.exp(-l1)) 
        l2 = np.dot(self.w2, l1)
        out = 1 / (1 + np.exp(-l2))
        if out[0] > self.THRESHOLD:
            return True
        return False

    def get_w1(self):
        return self.w1
    
    def get_w2(self):
        return self.w2

    def get_bias1(self):
        return self.bias1
    
    def weight_crossover(wa, wb):
        """
        Crossover two set of weights with middle split.
        Randomly decides the split point and which to go first
        and last.
        """

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
        """
        Crossover genes. Crosses the weights of both layer
        plus the bias.
        """

        w1a = Genes.weight_crossover(gene1.get_w1(), gene2.get_w1())
        w2a = Genes.weight_crossover(gene1.get_w2(), gene2.get_w2())
        if np.random.rand() < 0.5:
            bias = gene1.get_bias1()
        else:
            bias = gene2.get_bias1()
        
        return Genes([w1a, w2a, bias, 0])
        
    def weight_mutate(w):
        """
        Adds a random value to the weight array
        """

        w += np.random.normal(scale=1)
        return w
    
    def mutate(self):
        """
        Mutates both w1 and w2 arrays.
        """

        self.w1 = Genes.weight_mutate(self.w1)
        self.w2 = Genes.weight_mutate(self.w2)
    

class GeneticBird(Bird):
    """
    This class is the bird class that is used
    during the training model with genetic algorithm
    This makes use of the gene and uses 
    that to decide whehter to jump or not
    unlike the Bird class in the core game that requires
    user to press space bar.

    The class also holds the fitness score for the bird
    and provides the method to produce new offspring bird
    consisting a touch of genes from its parents.
    """

    def __init__(self, pos, genes=None):
        """
        Initlaise bird with genes and fitness score
        """

        super().__init__(pos)
        self.fitness_score = 0
        if genes:
            self.genes = genes
        else:
            self.genes = Genes()

    def jump(self, inp):
        """
        Use the the input to decide whether to jump or not
        if so invokes jump
        """ 
        
        if self.genes.get_decision(np.asarray(inp)):
            super().jump()
    
    def set_alive(self, alive):
        """
        Set alive.
        If true, then setting it to initial pos.
        """

        super().set_alive(alive)

    def get_genes(self):
        return self.genes

    def offspring(self, b):
        """
        Make offspring with b
        by crossovering and mutating the genes.
        """
        
        gene1 = Genes.crossover(self.genes, b.get_genes())
        gene1.mutate()
        newbird = GeneticBird(self.init_pos, gene1)
        return newbird

    def update_fitness_score(self, state):
        """
        Update fitness score
        Fitness Score = Distance Travelled - Distancce from bird + 100*score
        Distance Travelled = Moves * Obstacle Speed
        Distance from bird = Vertical Distance from Y midpoints + Horizontal distance of X midpoints
        """

        distance_travelled = self.moves * Obstacle.SPEED
        bx_midpoint = (self.X + self.X + self.WIDTH) // 2
        by_midpoint = (self.Y + self.Y + self.HEIGHT) // 2
        x_dist = state[0] - bx_midpoint
        y_dist = state[1] - by_midpoint

        self.fitness_score = int(distance_travelled - x_dist - y_dist) + (100 * self.score)
    
    def get_fitness_score(self):
        return self.fitness_score

    def __lt__(self, b): 
        return self.get_fitness_score() < b.get_fitness_score()
    
    def __gt__(self, b):
        return self.get_fitness_score() > b.get_fitness_score()
