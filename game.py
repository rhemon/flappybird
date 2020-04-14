"""
The main game file. That contains the Game class
for starting the game window and looping over it.

Maintains the object of the whole game.

"""

import pygame
import sys
from pygame.locals import *
from obstacles import Obstacle
from bird import Bird

class Game:
    
    WIDTH = 800
    HEIGHT = 400

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display.fill((0,255,0))
        self.jumped = False
        # intialise obstacles 
        self.obstacles = [Obstacle(self.WIDTH, self.HEIGHT, 400)]
        for i in range(1, 10):
            self.obstacles.append(Obstacle(self.WIDTH, self.HEIGHT, self.obstacles[i-1].get_X()))
        
        self.bird = Bird((50, 195))


    def obstacles_update(self):
        for each in self.obstacles:
            each.dec_X()
        for i in range(len(self.obstacles)):
            if (i >= len(self.obstacles)):
                break
            each = self.obstacles[i]
            if (each.get_X()+Obstacle.WIDTH < 0):
                each = self.obstacles.pop(i)
            
                # print("an obstacle removed")
            i -= 1
            
        for i in range(len(self.obstacles), 10):
            self.obstacles.append(Obstacle(self.WIDTH, self.HEIGHT, self.obstacles[i-1].get_X()))

    def get_state(self):
        state = []
        for each in self.obstacles[:1]:
            state.append(each.get_X())
            state.append(each.get_Y1())
            state.append(each.get_Y2())
        return state

    def bird_draw(self):
        pygame.draw.rect(self.display, self.BLUE, self.bird.get_rect())

    def bird_update(self):
        # print("called")
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
        for each in self.obstacles:
            r1, r2 = each.get_rects()
            pygame.draw.rect(self.display, self.RED, r1)
            pygame.draw.rect(self.display, self.RED, r2)
            
    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.check_jump(event)
    
    def check_jump(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.jumped:
                self.bird.jump()
                self.jumped = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.jumped = False
    
    def end_game(self):
        pygame.quit()
        sys.exit()

    def status_draw(self):
        return

    def play(self):
        self.event_check()

        self.display.fill((0,255,0))
        

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
        while 1:     
            self.play()

            

if __name__ == "__main__":
    g = Game()
    g.loop()