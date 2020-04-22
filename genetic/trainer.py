"""
This file provides the trainer class
to run the game with population size
that evolves and tries to learn to play the game
using concepts of genetic algorithm.

@author Ridhwanul Haque
@version 15.04.2020
"""

import os
import pygame

from core.game import *
from core.obstacles import *
from genetic.bird import *

class GeneticTrainer(Game):
    """
        Handles population and makes it loop over.
        Does selection and invokes crossover and mutation for
        new generations.
        Saves optimum weights.
        Allows to resume from best wieghts saved.
    """
    
    OPT_FILE_PATH = "weights/genetic-opt.npz"

    def __init__(self, population_size=100, load_opt=False):
        """
            Initialise population related variables.
            If load from the last optimum model, then load's
            last weights from saved file.
        """

        if population_size <= 0:
            raise Exception("Trainer population size must be a positive value.")
        super().__init__()
        
        if load_opt:
            self.load_opt_weights(population_size)
        else:
            self.birds = [GeneticBird((50, 195)) for i in range(population_size)]
            self.best_score = None
            self.best_bird = None
            
        self.raw_score = 0
        self.generation = 1
        self.bird = None
        self.score = 0
        self.alive = population_size

    def load_opt_weights(self, population_size):
        """
        Load weight of the best bird and then mutate the bird for the
        remaining population size.
        """

        weights = np.load(self.OPT_FILE_PATH)
        w1 = weights['w1']
        # print(w1)
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
        """
        Loop over all birds and draw each using superclass's draw
        method.
        """

        for each in self.birds:
            if not each.is_alive():
                continue
            self.bird = each
            # print(each.Y)
            super().bird_draw()
    
    def status_draw(self):
        """
        Display status information
        """

        self.add_status_label('Best Fitness: ' + str(self.best_score), 10)
        self.add_status_label('Generation: ' + str(self.generation), 20)
        self.add_status_label('Fitness: ' + str((self.birds)[-1].get_fitness_score()), 30)
        self.add_status_label('Alive: ' + str(self.alive), 40)
        self.add_status_label('Best Score: ' + str(self.raw_score), 50)
        self.add_status_label('Score: ' + str(self.score), 60)
        
    def bird_update(self):
        """
        For each bird in birds set them as self.bird
        and use super class's bird udpate method to make it move.
        """

        game = False
        i = 0
        count = 0
        for each in self.birds:
            if not each.is_alive():
                continue
            count += 1
            self.bird = each
            self.bird.jump(self.bird.get_input(self.get_state()))
            i += 1
            game = super().bird_update() or game
            self.bird.update_fitness_score(self.get_state())
        self.alive = count
        self.birds = sorted(self.birds)
        return game
    
    def check_jump(self, event):
        """
        Overwrite superclass's check_jump method to avoid calling
        jump on space bar press.
        """

        return

    def update_opt_wieghts(self):
        """
        Update local file with new optimum
        weights.
        """

        try:
            if (np.load(self.OPT_FILE_PATH)['best_score'].item() > self.best_score):
                return
            os.remove(self.OPT_FILE_PATH)
        except FileNotFoundError:
            pass
        np.savez(self.OPT_FILE_PATH, w1=self.best_bird.get_genes().get_w1(), 
                w2=self.best_bird.get_genes().get_w2(), bias1=self.best_bird.get_genes().get_bias1(),
                best_score=self.best_score)

    def do_selection(self):
        """
        End of the generation keep top 10 birds and 
        replace remaining with offsprings of best bird
        with 2nd to 4th best bird. 
        """

        self.birds = sorted(self.birds)

        if self.best_score == None:
            self.best_score = self.birds[-1].get_fitness_score()
            self.best_bird = self.birds[-1]
        
        if self.birds[-1].get_fitness_score() > self.best_score:
            self.best_score = self.birds[-1].get_fitness_score()
            self.best_bird = self.birds[-1]
            self.update_opt_wieghts()

        # if self.birds[-1].get_score() > self.raw_score:
        #     self.raw_score = self.birds[-1].get_score()

        for i in range(1,11):
            self.alive += 1
            self.birds[len(self.birds)-i].set_alive(True)

        for i in range(len(self.birds)-10):
            self.alive += 1
            ind = -int(np.random.rand()*3)-2
            self.birds[i] = self.birds[-1].offspring(self.birds[ind])

        self.reset_obstacles()
        # print("best scor///e", self.best_score)
        
    def play(self, wait_time=50):
        """
        Play a round.
        If all birds die then do selection for new generaiton.
        """

        game = super().play(wait_time)
        # print(game)
        self.score = sorted(self.birds)[-1].get_score()
        if game == False:
            self.do_selection()
        
    def end_game(self):
        """
        Increment the generation count.
        Doesn't actually end the game. 
        Used to mainly overwrite Game's end_game method.
        """

        self.generation += 1
        self.raw_score = self.score if self.score > self.raw_score else self.raw_score
        print("Generation:", self.generation)