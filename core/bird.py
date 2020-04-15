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

    def __init__(self, pos):
        self.X = pos[0]
        self.Y = pos[1]
        self.rect = Rect(self.X, self.Y, self.WIDTH, self.HEIGHT)
        self.up_X = 0
        self.moveBy = 7
        self.alive = True
        self.score = 0
        self.moves = 0
        self.init_pos = pos

    def jump(self):
        """
        Sets moveBy negative so that next time on move
        it moves upward.
        """

        if (self.up_X > 0 and self.up_X < self.JUMP_LIMIT):
            return
        self.up_X = 0
        self.moveBy = -abs(self.moveBy)
    
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
        if (self.moveBy < 0 and self.up_X >= self.JUMP_LIMIT):
            self.moveBy = abs(self.moveBy)
            self.up_X = 0
        elif (self.moveBy < 0):
            self.up_X += abs(self.moveBy)
        
        # self.X += abs(self.moveBy)
        self.Y += self.moveBy
        self.rect = Rect(self.X, self.Y, self.WIDTH, self.HEIGHT)
    
    def get_rect(self):
        """
        Return rect object
        """

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

    def is_alive(self):
        return self.alive
