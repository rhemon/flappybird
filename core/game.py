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

    WIDTH = 500
    HEIGHT = 400

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    BG_COLOR = WHITE 
    TEXT_COLOR = BLACK
    OBSTACLE_COLOR = (200, 200, 200)
    BIRD_COLOR = (10, 230, 40)

    INIT_BIRD_POS = (50, 195)
    
    def __init__(self):
        """
        Initialise game objects 
        """

        self.win_init()

        self.jumped = False
        self.jump_press = False
        # intialise obstacles 
        self.obstacles = [Obstacle(self.WIDTH, self.HEIGHT)]
        for i in range(1, 10):
            self.obstacles.append(Obstacle(self.WIDTH, self.HEIGHT, self.obstacles[i-1]))
        self.bird = Bird(self.INIT_BIRD_POS)

    
    def win_init(self):
        pygame.init()
        
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display.fill(self.BG_COLOR)
        
        self.font_obj = pygame.font.Font('freesansbold.ttf', 13)


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
   

    def bird_check(self):
        """
        Check if bird is alive after the move.
        If bird scores returns True,
        else returns None if alive.
        If dead returns False, also includes
        wheheter death was by upper pipe or not.
        """
        bx, by, bw, bh = self.bird.get_pos()
        if by+bh <= 0 or by >= self.HEIGHT:
            return False, False
        for each in self.obstacles:
            collide, upper = each.collison_checker(bx, by, bw, bh)
            alive = not collide # if collided, its not alive
            if not alive:
                return alive, upper
            if each.just_passed(bx):
                self.bird.inc_score()
                return True, False
        return None, False
        

    def bird_update(self):
        """
        Update bird. Move and if bird dies,
        then return False
        """
        game = True
        self.bird.move()
        
        game, _ = self.bird_check()
        
        if not game and not game == None:

            self.bird.set_alive(False)

        return game or game == None

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
            if event.key == pygame.K_SPACE and not self.jump_press:
                self.jumped = self.bird.jump()
                self.jump_press = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.jump_press = False
                self.jumped = False
    
    def end_game(self):
        """
        End and quit game.
        """

        self.exit_game()
        sys.exit()

    def status_draw(self):
        """
        Draw status. This only shows the score.
        """

        self.add_status_label("Score: " + str(self.bird.get_score()), 10)

    def extra_draw(self):
        """
        Abstract function for subclasses to implement
        if wants to add anything to the main draw method.
        Without duplicating game_draw
        """
        return
    
    def game_draw(self, wait_time=100):
        """
        Calls all the draw function for the game.
        """
        self.event_check()
        self.display.fill(self.BG_COLOR)
        self.obstacles_draw()
        self.bird_draw()
        self.status_draw()
        self.extra_draw()
        pygame.display.update()
        # print("inside game", wait_time)
        pygame.time.wait(wait_time)

        

    def play(self, wait_time=50):
        """
        Run the game.
        Calls all the update and draw method
        Used in the loop.
        """

        game = self.bird_update()
        self.obstacles_update()

        self.game_draw(wait_time)
        # self.game_draw()     
        return game
    
    def exit_game(self):
        pygame.font.quit()
        pygame.quit()

    def loop(self):
        """
        Game loop.
        """

        while 1:     
            game = self.play()
            if not game and not game == None:
                self.end_game()
    
    def reset_obstacles(self):
        """
        Reset obstacles.
        # """
        # print("RESET CALLED")
        # pygame.time.wait("")

        self.obstacles = [Obstacle(self.WIDTH, self.HEIGHT)]
        for i in range(1, 10):
            self.obstacles.append(Obstacle(self.WIDTH, self.HEIGHT, self.obstacles[i-1]))
