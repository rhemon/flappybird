from pygame import Rect
import numpy as np
from core.obstacles import *
from core.bird import *


class Genes:
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
        state = state.reshape(state.shape[0],1)
        l1 = np.dot(self.w1, state) + self.bias1
        l1 = 1 / (1 + np.exp(-l1)) 
        l2 = np.dot(self.w2, l1)
        out = 1 / (1 + np.exp(-l2))
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
        w1a = Genes.weight_crossover(gene1.get_w1(), gene2.get_w1())
        w2a = Genes.weight_crossover(gene1.get_w2(), gene2.get_w2())
        if np.random.rand() < 0.5:
            bias = gene1.get_bias1()
        else:
            bias = gene2.get_bias1()
        
        return Genes([w1a, w2a, bias, 0])
        
    def weight_mutate(w):
        # mutator = np.random.rand(w.shape[0], w.shape[1])
        # prob = lambda: (np.random.rand(w.shape[0], w.shape[1]) < 0.5).astype('int')
        # w *= mutator * prob() + mutator*prob()*-1
        w += np.random.normal(scale=1)
        return w
    
    def mutate(self):
        self.w1 = Genes.weight_mutate(self.w1)
        self.w2 = Genes.weight_mutate(self.w2)
    
class GeneticBird(Bird):
    
    def __init__(self, pos, genes=None):
        super().__init__(pos)
        self.init_pos = pos
        if genes:
            self.genes = genes
        else:
            self.genes = Genes()

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
        gene1 = Genes.crossover(self.genes, b.get_genes())
        gene1.mutate()
        newbird = GeneticBird(self.init_pos, gene1)
        return newbird