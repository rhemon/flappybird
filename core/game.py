"""
This provides the core game class
that combines all necessary objects
and allows to play the basic flappy bird game.

@author Ridhwanul Haque
@version 15.04.2020
"""

import sys

import pygame
from pygame.locals import *

from core.bird import *
from core.obstacles import *


class Game:
    """
    Handles the obstacles and bird in game.
    Draws and updates the status of the game.
    Allows user to play a single round and on end
    game quits.
    """

    WIDTH = 800
    HEIGHT = 400

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    BG_COLOR = GREEN 
    TEXT_COLOR = WHITE
    OBSTACLE_COLOR = RED
    BIRD_COLOR = BLUE
    
    def __init__(self):
        """
        Initialise game objects 
        """

        pygame.init()
        
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display.fill(self.BG_COLOR)
        
        self.font_obj = pygame.font.Font('freesansbold.ttf', 13)

        self.jumped = False
        # intialise obstacles 
        self.obstacles = [Obstacle(self.WIDTH, self.HEIGHT)]
        for i in range(1, 10):
            self.obstacles.append(Obstacle(self.WIDTH, self.HEIGHT, self.obstacles[i-1]))
        
        self.bird = Bird((50, 195))

    def add_status_label(self, text, y_center):
        """
        Add status text at y_center
        """

        text_obj = self.font_obj.render(text, True, self.TEXT_COLOR)
        text_rect = text_obj.get_rect()
        text_rect.center = (self.WIDTH-90, y_center)

        self.display.blit(text_obj, text_rect)
    

    def obstacles_update(self):
        """
        Update obstacle. Make them move.
        If any goes out of screen remove it from the list.
        Add new. Always keeps 10 in the list.
        """

        for each in self.obstacles:
            each.dec_X()
        for i in range(len(self.obstacles)):
            if (i >= len(self.obstacles)):
                break
            each = self.obstacles[i]
            if (each.get_X()+Obstacle.WIDTH < 0):
                each = self.obstacles.pop(i)
                i -= 1
            
        for i in range(len(self.obstacles), 10):
            self.obstacles.append(Obstacle(self.WIDTH, self.HEIGHT, self.obstacles[i-1]))

    def get_state(self):
        """
        Get state. Mainly provides the list for the input
        in training models.
        """
        state = []
        for i in range(len(self.obstacles)):
            each = self.obstacles[i]
            if not each.did_pass():
                x_end = each.get_X()+Obstacle.WIDTH
                y_mid = each.get_Y_Midpoint()
                x_start_2 = self.obstacles[i+1].get_X()
                y_mid_2 = self.obstacles[i+1].get_Y_Midpoint()
                dist = np.sqrt((x_end-x_start_2)**2 + (y_mid-y_mid_2)**2)
                state.append(x_end)
                state.append(y_mid)
                # state.append(dist)
                break
        return state

    def bird_draw(self):
        """
        Draw bird rectangle
        """

        pygame.draw.rect(self.display, self.BIRD_COLOR, self.bird.get_rect())

    def bird_update(self):
        """
        Update bird. Move and if bird dies,
        then return False
        """

        game = True
        self.bird.move()
        bx, by, bw, bh = self.bird.get_pos()
        if by+bh <= 0 or by >= self.HEIGHT:
            game = False

        for each in self.obstacles:
            if each.collison_checker(bx, by, bw, bh):
                game = False
            if each.just_passed(bx):
                self.bird.inc_score()
        
        if not game:
            self.bird.set_alive(False)
        return game

    def obstacles_draw(self):
        """
        Draw all the obstacle rectangles
        """

        for each in self.obstacles:
            r1, r2 = each.get_rects()
            pygame.draw.rect(self.display, self.OBSTACLE_COLOR, r1)
            pygame.draw.rect(self.display, self.OBSTACLE_COLOR, r2)
            
    def event_check(self):
        """
        Check for events during thegame
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.check_jump(event)
    
    def check_jump(self, event):
        """
        Check for spacebar press to whether jump or not.
        """

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.jumped:
                self.bird.jump()
                self.jumped = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.jumped = False
    
    def end_game(self):
        """
        End and quit game.
        """

        pygame.quit()
        sys.exit()

    def status_draw(self):
        """
        Draw status. This only shows the score.
        """

        self.add_status_label("Score: " + str(self.bird.get_score()), 10)

    def play(self):
        """
        Run the game.
        Calls all the update and draw method
        Used in the loop.
        """

        self.event_check()

        self.display.fill(self.BG_COLOR)
        

        self.obstacles_update()
        self.obstacles_draw()

        game = self.bird_update()
        self.bird_draw()

        self.status_draw()
            
        pygame.display.update()
        # pygame.display.flip()

        if not game:
            self.end_game()
            
        pygame.time.wait(50)

        return game
    
    def loop(self):
        """
        Game loop.
        """

        while 1:     
            self.play()
