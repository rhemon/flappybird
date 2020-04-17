"""
This file provides the classes for the neural network
mdoel and the Bird class that uses the model to decide
whether to jump or not.

@author Ridhwanul Haque
@version 17.04.2020
"""

import numpy as np
import keras
import pygame

from core.bird import Bird


class Model:
    """
    Neural network model.
    Uses keras mainly to for the neural network model.
    """

    def __init__(self, load_prev=False):
        self.model = keras.Sequential([
            keras.layers.Dense(8, input_shape=(4,), activation="sigmoid"),
            keras.layers.Dense(1, activation="sigmoid")
        ])

        self.model.compile(optimizer='adam', loss=keras.losses.binary_crossentropy, metrics=['accuracy'])

    def train(self, X, y):
        self.model.fit(X, y, epochs=100)
    
    def decide(self, state):
        """
        Decide whehter to jump or not in given state.
        """

        return self.model.predict(state).item() > 0.5


class SupervisedBird(Bird):
    """
    Extends core's Bird class where uses the model
    to determine whether to jump or not.
    """

    def __init__(self, pos, model=None):
        super().__init__(pos)
        if model:
            self.model = model
        else:
            self.model = Model()
    
    def jump(self, inp):
        if self.model.decide([[inp]]):
            return super().jump()
        return False

    def train(self, X, Y):
        self.model.train(X, Y)
    