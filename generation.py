
import pygame
from game import *
from bird import *
from obstacles import *

class Generation(Game):

    def __init__(self, population_size=100):
        super().__init__()
        self.birds = [BirdWithGenes((50, 195)) for i in range(population_size)]
        self.bird = None
        self.generation = 1

    def bird_draw(self):
        for each in self.birds:
            if not each.is_alive():
                continue
            self.bird = each
            # print(each.Y)
            super().bird_draw()
    
    def bird_update(self):
        game = False
        i = 0
        # self.bird = None
        for each in self.birds:

            if not each.is_alive():
                continue
            # self.prevbird = self.bird
            self.bird = each
            self.bird.jump(self.get_state())
            # assert self.prevbird != self.bird
            # print("bird move called", i)
            i += 1
            game = super().bird_update() or game
        return game
    
    def check_jump(self, event):
        return

    def play(self):
        game = super().play()
        if not game:
            self.birds = sorted(self.birds)
            self.birds[0], self.birds[1], self.birds[-1], self.birds[-2] = self.birds[0].offspring(self.birds[1])
            for each in self.birds:
                each.set_alive(True)
                each.set_init_pos()
                each.get_genes().mutate()
            self.reset_obstacles()
            

    def reset_obstacles(self):
        # intialise obstacles 
        self.obstacles = [Obstacle(self.WIDTH, self.HEIGHT, 400)]
        for i in range(1, 10):
            self.obstacles.append(Obstacle(self.WIDTH, self.HEIGHT, self.obstacles[i-1].get_X()))
        

    def end_game(self):
        self.generation += 1
        print("Generation:", self.generation)
    
if __name__ == "__main__":
    gen = Generation()
    gen.loop()
    
