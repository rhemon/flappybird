# Flappy Bird

Start How-To(s)
---

### 1. Playing game

- Set up all necessary requiremnts. You will need python 3 installed before these.
- I also recommend using a virutal environment before installing requirements.
```
$ python3 -m venv venv // python if you only have python3 installed
$ source venv/bin/activate // venv\Scripts\activate if windows
// You can directly run the below code if you don't want to use virtual environment.
(venv) $ pip install -r requirements.txt 
```
- Once all required packages get installed, to play game run:
```
$ python start.py play
```

### 2. Starting Training with Genetic Algorithm
- With all packages installed, just run
```
$ python start.py genetic
```
- You can also make it continue from last best weights saved or specify population size from command line.
```
$ python start.py genetic -r -s 100
```

File Descriptions
---

### `start.py`

This file is used to invoke the different ways to launch the game. It makes use
of command line arguments to determine how to laod the game.

On above how-to's the avialable commands are shared.

-----------------------------------------------------------------------------------

### `core/`

*This folder mainly consist of all the models providing essential feature for the game.*

`core/bird.py`

Contains `Bird` class. It contains the position and score information of the bird. Provides
methods to let bird move and jump in the game.

`core/obstacles.py`

Contains `Obstacle` class. Prepares and handles the obstacles of the game.
Here each obstacle are simply the boxes that leave a small gap inbetween.

`core/game.py`

Contains the `Game` class that handles the game loop and states.

------------------------------------------------------------------------------------

### `genetic/`

*The folder containig extended classes of Game and Bird for making it suitable
for genetic algorithm and letting bird learn to play the game.*

`genetic/bird.py`

Provides `Genes` and `GeneticBird` class. `Genes` provide the basic functionality for
the model that handles the weight and uses to get decision for the bird to jump
or not.

The `GeneticBird` class uses a `Genes` object to determine jump and also
uses a fitness score to compare between different birds.

`genetic/trainer.py`

The `GeneticTrainer` class is used to loop over the game with the genetic birds
and uses the concept of genetic algorithm to evolve the birds to learn to
play the game.

------------------------------------------------------------------------------------

Model Descriptions
---

*TO BE CONTINUED*