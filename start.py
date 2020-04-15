import getopt
import sys
from core.game import Game
from genetic.trainer import *

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
        
    else:
        raise  Exception("Unrecognised runtype. Valid optionos: play, genetic")