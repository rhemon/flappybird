"""
File used to run the flappy bird game from the command line.

Requires python3 with pygame and numpy installed.

To run the game on normal play mode:
You need to run
$ pythoon start.py play

To run the game on genetic algorithm to make the ai learn to play on its own run:
$ python start.py genetic
If you have previously run it or wanna continue on the given weights just use
$ python start.py genetic -r
If you wish to provide your own size 
$ python start.py genetic -r -s 200

To run the game on supervised mode
$ python start.py supervised

To run the game learning with qlearning
$ python start.py qlearn

@author Ridhwanul Haque
@version 15.04.2020
"""

import getopt
import sys

from core.game import Game
from genetic.trainer import *
from supervised.trainer import *
from qlearning.trainer import *


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Arugment must be in form `python start.py <runtype> ...`")
    runtype = sys.argv[1]
    if runtype == "play":
        g = Game()
        g.loop()
    elif runtype == "genetic":
        try:
            opts, args = getopt.getopt(sys.argv[2:], "hrs:")
        except getopt.GetoptError:
            print('Invalid options. Valid are -h (for help), -r (for resuming training), -s <size> (population size)')
            sys.exit()
        trained = False
        size = 100
        resume = False
        sizespecified = False
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('-h for help, -r for continuing the training from best point, -s <size> for the population')
            elif opt in ('-s', '--size'):
                size = arg
                sizespecified = True
            elif opt in ('-r', '--resume'):
                resume = True
        size = int(size)
        if resume:
            g = GeneticTrainer(size, True)
        else:
            g = GeneticTrainer(size)
        g.loop()
    elif runtype == "qlearn":
        g = ReinforcedTrainer()      
        g.loop()
    elif runtype == "supervised":
        gdg = GameDataGen()
        gdg.loop()
        X, Y = gdg.get_XY()
        sg = SupervisedTrainer(X=X, Y=Y)
        sg.loop()
    else:
        raise  Exception("Unrecognised runtype. Valid optionos: play, genetic, supervised, qlearn")
