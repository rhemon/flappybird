
from pygame import Rect
import numpy as np

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
        return self.moves*(self.score+1)
    
    def __lt__(self, b):
        return self.get_score() < b.get_score()
    
    def __gt__(self, b):
        return self.get_score() > b.get_score()
    
    def set_alive(self, alive):
        self.alive = alive

    def is_alive(self):
        return self.alive

class Chromosome:

    def __init__(self, weights=None):
        if weights:
            self.w1 = weights[0]
            self.w2 = weights[1]
        else:    
            self.w1 = np.random.uniform(-5,5,(8, 4))
            self.w2 = np.random.uniform(-5,5,(1, 8))
    
    def get_decision(self, state):
        l1 = np.dot(self.w1, state)
        # l1 = 1 / (1 + np.exp(-l1))
        l2 = np.dot(self.w2, l1)
        out = 1 / (1 + np.exp(-l2))
        # out = 
        if out[0] <= 0.5:
            return True
        return False

    def get_w1(self):
        return self.w1
    
    def get_w2(self):
        return self.w2
    
    def weight_crossover(wa, wb):
        if wa.shape != wb.shape:
            raise Exception("Weight dimensions must be equal for a crossover")
        
        x = round(np.random.rand() * wa.shape[0])
        y = round(np.random.rand() * wa.shape[1])
        

        wa_, wb_ = np.zeros(wa.shape), np.zeros(wa.shape)

        wa_[:x][:y] = wa[:x][:y]
        wa_[:x][y:] = wb[:x][y:]
        wa_[x:][:y] = wb[x:][:y]
        wa_[x:][y:] = wa[x:][y:]

        wb_[:x][:y] = wb[:x][:y]
        wb_[:x][y:] = wa[:x][y:]
        wb_[x:][:y] = wa[x:][:y]
        wb_[x:][y:] = wb[x:][y:]

        return wa_, wb_

    def crossover(gene1, gene2):
        w1a, w1b = Chromosome.weight_crossover(gene1.get_w1(), gene2.get_w1())
        w2a, w2b = Chromosome.weight_crossover(gene1.get_w2(), gene2.get_w2())
        
        return Chromosome([w1a, w2a]), Chromosome([w1b, w2b])
        
    def weight_mutate(w):
        mutator = np.random.rand(w.shape[0], w.shape[1])
        prob = (np.random.rand(w.shape[0], w.shape[1]) < 0.5).astype('int')
        w *= mutator * prob
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
        state.insert(0, self.X)
        if self.genes.get_decision(np.asarray(state)):
            super().jump()
    
    def set_init_pos(self):
        self.X = self.init_pos[0]
        self.Y = self.init_pos[1]

    def get_genes(self):
        return self.genes

    def offspring(self, b):
        gene1, gene2 = Chromosome.crossover(self.genes, b.get_genes())
        gene1.mutate()
        gene2.mutate()
        bird1 = BirdWithGenes(self.init_pos, gene1)
        bird2 = BirdWithGenes(self.init_pos, gene2)
        gene1.mutate()
        gene2.mutate()
        bird3 = BirdWithGenes(self.init_pos, gene1)
        bird4 = BirdWithGenes(self.init_pos, gene2)
        return bird1, bird2, bird3, bird4