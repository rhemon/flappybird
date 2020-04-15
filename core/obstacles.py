"""
This file provides all objects to prepare the obstacle
for the game.

The obstacle here are the plain rectangle blocks. In
between which the bird must pass through.

@author Ridhwanul Haque
@version 12.04.2020
"""

from random import random as rand

from pygame import Rect


class Obstacle:
    """
    Obstacle class for the game.

    Each obstacle wall will be of 50px wide.
    For height it can be of any. But between the obstacles
    it has to have a min gap of 40px and a max gap of 90px.

    It may be so the obstacle is made of one box only, 
    leaving a space between the pane border and the obstacle
    for the bird to pass thorugh.
    """

    # WIDTH OF BOXES OF OBSTACLE
    WIDTH = 40

    # VERITCAL GAP BETWEEN TWO BOXES OF AN OBSTACLE
    MIN_GAP = 100
    MAX_GAP = 120

    # HORIZONTAL SPACE BETWEEN TWO OBSTACLES
    MIN_SPACE = 230
    MAX_SPACE = 230

    SPEED = 7

    def __init__(self, WIN_WIDTH, WIN_HEIGHT, prev_X):
        """
        Initialise x,y co-ordinates for the obstacle boxes.
        
        :param WIN_HEIGHT:      Height of game window
        :param prev_X:          Previous obstacle's X-coordinate
        """
        
        self.WIN_WIDTH = WIN_WIDTH
        self.WIN_HEIGHT = WIN_HEIGHT

        # Random height between 0 to WINDOWWIN_HEIGHT_HEIGHT - MIN_GAP
        self.height1 = round(rand() * (WIN_HEIGHT - self.MIN_GAP))
        
        # If height1 is big enough then second box not needed.
        # otherwise create a second box height that will at least
        # leave a gap no more than MAX_GAP
        if (self.height1 > WIN_HEIGHT - self.MAX_GAP):
            self.height2 = 0
        else:
            self.height2 = round(rand() * (WIN_HEIGHT - self.MIN_GAP - self.height1))
            if (WIN_HEIGHT - self.height1 - self.height2 > self.MAX_GAP):
                self.height2 += WIN_HEIGHT - self.height1 - self.height2 - self.MAX_GAP
        
        # Based on previous prev_X, select a X point at a random distance between MIN to MAX SPACE
        self.X = round(rand() * (self.MAX_SPACE - self.MIN_SPACE)) + self.MIN_SPACE + prev_X

        self.init_X = self.X
        
        # Initial rectangles for obstacle
        self.r1 = Rect(self.X, 0, self.WIDTH, self.height1)
        self.r2 = Rect(self.X, self.WIN_HEIGHT-self.height2, self.WIDTH, self.height2)

        self.passed = False

    def reset_X(self):
        """
        Reset X to initial position.
        """

        self.X = self.init_X
        self.update_rects()

    def get_rects(self):
        return (self.r1, self.r2)

    def get_X(self):
        return self.X
    
    def dec_X(self):
        """
        Decrement X.
        Making it move left.
        """
        
        self.X -= self.SPEED
        self.update_rects()

    def update_rects(self):
        """
        Reset rect with updated X and Y cords.
        """

        self.r1 = Rect(self.X, 0, self.WIDTH, self.height1)
        self.r2 = Rect(self.X, self.WIN_HEIGHT-self.height2, self.WIDTH, self.height2)

    def collison_checker(self, x, y, width, height):
        """
        Check if given position with width and height
        collide with the obstacle anywhere.
        If so returns True, otherwise False.
        """

        if x >= self.X and x <= self.X+self.WIDTH or (x+width) >= self.X and (x+width) <= self.X+self.WIDTH:
            if (self.height1 >= y or self.WIN_HEIGHT-self.height2 <= y+height):
                return True
        return False
    
    def just_passed(self, x):
        """
        Check's if obstacle gets passed by the x cordinate.
        If so, returns True else returns False.
        If position already passed then returns false.
        """
        
        if self.passed:
            return False
        elif self.X+self.WIDTH < x:
            self.passed = True
            return True
        return False

    def did_pass(self):
        return self.passed

    def get_Y1(self):
        return self.height1
    
    def get_Y2(self):
        return self.WIN_HEIGHT-self.height2

    def get_Y_Midpoint(self):
        return (self.get_Y1() + self.get_Y2()) // 2

    def get_X_Midpoint(self):
        return (self.get_X() + self.WIDTH + self.get_X()) // 2
