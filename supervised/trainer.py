import pandas as pd
import pygame
import sys

from .bird import *
from core.game import Game

class GameDataGen(Game):
    """
    Using this class we let a player play a single round
    in the game to allow to set an example for the AI.

    This mainly prepares some starting dataset for the model
    to train on.
    """

    def __init__(self):
        super().__init__()
        self.X = []
        self.Y = []
        self.run = True
        self.jump_added = False
        self.user_started = False

    def play(self):
        """
        If bird is not in jump that means player decided not
        to jump, so add that to status. If bird is in jump
        and its not already added then add that to the dataset.
        """
        game = super().play()
        # so only
        if not self.bird.in_jump() or not self.jump_added:
            self.set_XY()
            jump_added = self.bird.in_jump()
        return game

    def set_XY(self):
        """
        If jumped and bird is alive, for input set label Y as 1
        If jumped and bird died then label as 0
        If not jumped and bird died then set label as 1
        If not jumped and bird alive then set label as 0
        """

        y = 0
        if (self.jumped and self.bird.is_alive()) or (not self.jumped and not self.bird.is_alive()):
            y = 1
        self.X += [self.bird.get_input(self.get_state())]
        self.Y += [[y]]

    def get_XY(self):
        return self.X, self.Y

    def end_game(self):
        pygame.quit()
        # print(self.X)
        # print(self.Y)
        self.run = False

    def temp_screen(self):
        """
        Temp screen when waiting for player to start.
        """

        self.display.fill(self.BG_COLOR)
        self.obstacles_draw()
        self.bird_draw()

        self.add_status_label("Press Enter to Start", 10)
        pygame.display.update()
        
    def loop(self):
        """
        Overwritten loop to wait for invoke player to start.
        """

        # Wait for player to invoke a start
        while not self.user_started:
            self.temp_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.user_started = True
            
        while self.run:
            game = self.play()
            if game == False:
                self.end_game()
    

class SupervisedTrainer(GameDataGen):
    """
    Extending GameDataGen as it also will collect dataset
    as it plays the game. Altho it will no longer interact
    with player so check jump and bird update is modified
    to adjust the needs.
    """

    DATA_PATH = "data/supervised_data.csv"
    OPT_PATH = "weights/supervised-opt.***"

    def __init__(self, X=[], Y=[], reload=False):
        super().__init__()
        self.bird = SupervisedBird((50, 195))
        self.best_score = 0
        self.round = 1
        self.X = X
        self.Y = Y
        if not reload and len(X) != len(Y) and len(X) == 0:
            raise Exception("X and Y has to be more than zero and equal")
        elif reload:
            pass
        self.retrain_model()
        
    def status_draw(self):
        self.add_status_label("Best Score: " + str(self.best_score), 10)
        self.add_status_label("Score: " + str(self.bird.get_score()), 20)
        self.add_status_label("Round: " + str(self.round), 30)
    
    def check_jump(self, event):
        return
    
    def bird_update(self):
        """
        Update bird actions
        """

        decide = 0
        jumped = False

        if (not self.bird.in_jump()):
            self.jumped = self.bird.jump(self.bird.get_input(self.get_state()))
        
        game = super().bird_update()
        return game

    def temp_screen(self):
        """
        Temp screen to show its being trained.
        """

        self.display.fill(self.BG_COLOR)
        self.add_status_label("Training model...", self.HEIGHT-10)
        pygame.display.update()

    def retrain_model(self):
        """
        Call to train model with the update dataset.
        """

        self.temp_screen()
        self.bird.train(np.asarray(self.X), np.asarray(self.Y))

    def end_game(self):
        """
        Retrian model instead of quitting.
        And continue further.
        """

        self.round += 1
        self.retrain_model()
        self.bird.set_alive(True)
        self.reset_obstacles()

    def loop(self):
        """
        Overwritting again to original loop in Game class, as this does
        not require interaction with player.
        """

        while self.run:
            game = self.play()
            if game == False:
                self.end_game()