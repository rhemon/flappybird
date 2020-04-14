
import pygame
from game import *
from bird import *
from obstacles import *

class Generation(Game):

    def __init__(self, population_size=100):
        super().__init__()
        self.font_obj = pygame.font.Font('freesansbold.ttf', 13)
        
        self.birds = [BirdWithGenes((50, 195)) for i in range(population_size)]
        self.bird = None
        self.generation = 1
        self.best_score = None
        self.alive = population_size
        

    def bird_draw(self):
        for each in self.birds:
            if not each.is_alive():
                continue
            self.bird = each
            # print(each.Y)
            super().bird_draw()
    
    def status_draw(self):
        gen_numb = self.font_obj.render('Generation: ' + str(self.generation), True, self.WHITE)
        best_score = self.font_obj.render('Best Score: ' + str(self.best_score), True, self.WHITE)
        cur_score = self.font_obj.render('Current Best Score: ' + str((self.birds)[-1].get_fitness_score()), True, self.WHITE)
        alive_score = self.font_obj.render('Alive: ' + str(self.alive), True, self.WHITE)

        gen_numb_rect = gen_numb.get_rect()
        gen_numb_rect.center = (self.WIDTH-80, 20)
        best_score_rect = best_score.get_rect()
        best_score_rect.center = (self.WIDTH-80, 10)
        cur_score_rect = cur_score.get_rect()
        cur_score_rect.center = (self.WIDTH-80, 30)
        alive_score_rect = alive_score.get_rect()
        alive_score_rect.center = (self.WIDTH-80, 40)

        self.display.blit(gen_numb, gen_numb_rect)
        self.display.blit(best_score, best_score_rect)
        self.display.blit(cur_score, cur_score_rect)
        self.display.blit(alive_score, alive_score_rect)

        
    def bird_update(self):
        game = False
        i = 0
        # self.bird = None
        count = 0
        for each in self.birds:

            if not each.is_alive():
                continue
            count += 1
            # self.prevbird = self.bird
            self.bird = each
            self.bird.jump(self.get_state())
            # assert self.prevbird != self.bird
            # print("bird move called", i)
            i += 1
            game = super().bird_update() or game
            self.bird.update_fitness_score(self.get_state())
        self.alive = count
        self.birds = sorted(self.birds)
        return game
    
    def check_jump(self, event):
        return

    def play(self):
        game = super().play()
        # self.status_draw()
        if not game:
            self.birds = sorted(self.birds)
            if self.best_score == None:
                self.best_score = self.birds[-1].get_fitness_score()
            self.best_score = self.birds[-1].get_fitness_score() if self.birds[-1].get_fitness_score() > self.best_score else self.best_score

            for i in range(1,11):
                self.alive += 1
                self.birds[len(self.birds)-i].set_alive(True)

            for i in range(len(self.birds)-10):
                self.alive += 1
                ind = -int(np.random.rand()*3)-2
                self.birds[i] = self.birds[-1].offspring(self.birds[ind])

            self.reset_obstacles()
            print("best score", self.best_score)
        
        
    def reset_obstacles(self):
        # intialise obstacles 
        self.obstacles = [Obstacle(self.WIDTH, self.HEIGHT, 400)]
        for i in range(1, 10):
            self.obstacles.append(Obstacle(self.WIDTH, self.HEIGHT, self.obstacles[i-1].get_X()))
        # for each in self.obstacles:
        #     each.reset_X()        

    def end_game(self):
        self.generation += 1
        print("Generation:", self.generation)
    
if __name__ == "__main__":
    gen = Generation()
    gen.loop()
    
