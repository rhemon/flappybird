"""
This file provides the Bird class for the game.

@author Ridhwanul Haque
@version 15.04.2020
"""

import numpy as np
from pygame import Rect

from core.obstacles import *


class Bird:
    """
    Hanldes all bird related information.
    Includings it co-ordinates, score,
    rectangle and movement speed.
    """

    WIDTH=10
    HEIGHT=10
    JUMP_LIMIT = 60
    INIT_MOVE_BY = 7

    def __init__(self, pos):
        self.X = pos[0]
        self.Y = pos[1]
        self.up_X = 0
        self.moveBy = self.INIT_MOVE_BY
        self.alive = True
        self.score = 0
        self.moves = 0
        self.init_pos = pos

    def jump(self):
        """
        Sets moveBy negative so that next time on move
        it moves upward.
        """
        if (self.in_jump()):
            return False
        self.up_X = 0
        self.moveBy = -abs(self.moveBy)
        return True
    
    def in_jump(self):
        return self.moveBy < 0

    def set_init_pos(self):
        """
        Set to initial position
        """
        self.X = self.init_pos[0]
        self.Y = self.init_pos[1]

    def move(self):
        """
        Move the bird. 
        X cordinate doesn't
        change as obstacles X move.
        Only Y moves.
        """
        self.moves += 1
        self.Y += self.moveBy

        if (self.in_jump()):
            self.up_X += abs(self.moveBy)
            if self.up_X >= self.JUMP_LIMIT:
                self.moveBy = abs(self.moveBy)
                self.up_X = 0
    
    def get_rect(self):
        """
        Return rect object
        """
        
        self.rect = Rect(self.X, self.Y, self.WIDTH, self.HEIGHT)
        return self.rect
    
    def get_pos(self):
        """
        Position detail of the bird
        """

        return (self.X, self.Y, self.WIDTH, self.HEIGHT)

    def inc_score(self):
        self.score += 1
    
    def get_score(self):
        return self.score
    
    def set_alive(self, alive):
        """
        Set alive. If its being set to true
        it means its respawning so resetting
        details
        """

        self.alive = alive
        if alive:
            self.moves = 0
            self.score = 0
            self.up_X = 0
            self.set_init_pos()

    def is_alive(self):
        return self.alive

    def __lt__(self, b): 
        return self.get_score() < b.get_score()
    
    def __gt__(self, b):
        return self.get_score() > b.get_score()
    
    def get_input(self, state):
        """
        Returns the data for model's input.
        """

        inp = [self.X, self.Y, (state[0] - ((self.X+self.X+self.WIDTH) // 2)), (state[1] - ((self.Y+self.Y+self.HEIGHT) // 2))]
        return inp

    def get_UpX(self):
        return self.up_X

