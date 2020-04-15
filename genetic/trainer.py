import os
import pygame
from core.game import *
from genetic.bird import *
from core.obstacles import *

class GeneticTrainer(Game):

    OPT_FILE_PATH = "genetic/weights/opt.npz"

    def __init__(self, population_size=100, load_opt=False):
        if population_size <= 0:
            raise Exception("Trainer population size must be a positive value.")
        super().__init__()
        self.font_obj = pygame.font.Font('freesansbold.ttf', 13)
        
        if load_opt:
            self.load_opt_weights(population_size)
        else:
            self.birds = [GeneticBird((50, 195)) for i in range(population_size)]
            self.best_score = None
            self.best_bird = None
            
        
        self.raw_score = 0
        self.generation = 1
        self.bird = None
        self.alive = population_size

    def load_opt_weights(self, population_size):
        weights = np.load(self.OPT_FILE_PATH)
        w1 = weights['w1']
        print(w1)
        w2 = weights['w2']
        bias1 = weights['bias1'].item()
        genes = Genes([w1, w2, bias1])
        self.birds = [GeneticBird((50, 195), genes)]
        if population_size > 1:
            genes = Genes([w1, w2, bias1])
            genes.mutate()
            self.birds.append(GeneticBird((50, 195), genes))
            for i in range(2, population_size):
                self.birds.append(self.birds[0].offspring(self.birds[i-1]))
        
        self.best_score = weights['best_score'].item()
        self.best_bird = self.birds[0]
        
    def bird_draw(self):
        for each in self.birds:
            if not each.is_alive():
                continue
            self.bird = each
            # print(each.Y)
            super().bird_draw()
    
    def status_draw(self):
        gen_numb = self.font_obj.render('Generation: ' + str(self.generation), True, self.WHITE)
        best_score = self.font_obj.render('Best Fitness: ' + str(self.best_score), True, self.WHITE)
        cur_score = self.font_obj.render('Current Fitness: ' + str((self.birds)[-1].get_fitness_score()), True, self.WHITE)
        alive_score = self.font_obj.render('Alive: ' + str(self.alive), True, self.WHITE)
        raw_score = self.font_obj.render('Best Score: ' + str(self.raw_score), True, self.WHITE)

        gen_numb_rect = gen_numb.get_rect()
        gen_numb_rect.center = (self.WIDTH-80, 20)
        best_score_rect = best_score.get_rect()
        best_score_rect.center = (self.WIDTH-80, 10)
        cur_score_rect = cur_score.get_rect()
        cur_score_rect.center = (self.WIDTH-80, 30)
        alive_score_rect = alive_score.get_rect()
        alive_score_rect.center = (self.WIDTH-80, 40)
        raw_score_rect = raw_score.get_rect()
        raw_score_rect.center = (self.WIDTH-80, 50)

        self.display.blit(gen_numb, gen_numb_rect)
        self.display.blit(best_score, best_score_rect)
        self.display.blit(cur_score, cur_score_rect)
        self.display.blit(alive_score, alive_score_rect)
        self.display.blit(raw_score, raw_score_rect)

        
    def bird_update(self):
        game = False
        i = 0
        count = 0
        for each in self.birds:
            if not each.is_alive():
                continue
            count += 1
            self.bird = each
            self.bird.jump(self.get_state())
            i += 1
            game = super().bird_update() or game
            self.bird.update_fitness_score(self.get_state())
        self.alive = count
        self.birds = sorted(self.birds)
        return game
    
    def check_jump(self, event):
        return

    def update_opt_wieghts(self):
        if (np.load(self.OPT_FILE_PATH)['best_score'].item() > self.best_score):
            return 
        os.remove(self.OPT_FILE_PATH)
        np.savez(self.OPT_FILE_PATH, w1=self.best_bird.get_genes().get_w1(), 
                w2=self.best_bird.get_genes().get_w2(), bias1=self.best_bird.get_genes().get_bias1(),
                best_score=self.best_score)
        print(np.load(self.OPT_FILE_PATH)['w1'])
        print(self.best_bird.get_genes().get_w1())

    def do_selection(self, game):
        if not game:
            self.birds = sorted(self.birds)

            if self.best_score == None:
                self.best_score = self.birds[-1].get_fitness_score()
                self.best_bird = self.birds[-1]
            
            if self.birds[-1].get_fitness_score() > self.best_score:
                self.best_score = self.birds[-1].get_fitness_score()
                self.best_bird = self.birds[-1]
                self.update_opt_wieghts()

            if self.birds[-1].get_score() > self.raw_score:
                self.raw_score = self.birds[-1].get_score()

            for i in range(1,11):
                self.alive += 1
                self.birds[len(self.birds)-i].set_alive(True)

            for i in range(len(self.birds)-10):
                self.alive += 1
                ind = -int(np.random.rand()*3)-2
                self.birds[i] = self.birds[-1].offspring(self.birds[ind])

            self.reset_obstacles()
            print("best score", self.best_score)
        
    def play(self):
        game = super().play()
        self.do_selection(game)
        
    def reset_obstacles(self):
        self.obstacles = [Obstacle(self.WIDTH, self.HEIGHT, 400)]
        for i in range(1, 10):
            self.obstacles.append(Obstacle(self.WIDTH, self.HEIGHT, self.obstacles[i-1].get_X()))

    def end_game(self):
        self.generation += 1
        print("Generation:", self.generation)