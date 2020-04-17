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

### 3. Starting Training with Supervised Neural Network
- This part will require keras along with numpy and pygame, so make sure you had all requiremens installed.
- Run:
```
$ python start.py supervised
```
This will first prompt the user to play a round first so that it can gather some initial data
for training the neural network model.
It then uses that to play a round, and after everyround with new collected data retrains the model.

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

### `supervised/`

*This folder contains extended classes for making the flappy bird AI learn to play
the game using the concept of supervised machine learning. It uses the same
neural network model as the genetic algorithm one, but here it tries to collect the
interaction and train the model to learn to play the game.

It first prompts the user to play the game, where it takes the input set and user's 
action to label X and Y. In a case if user's decision led ot the bird crashing,
it switches the label in that case.*

`supervised/bird.py`

This file contains the `Model` and `SupervisedBird` class. The `Model` class basically
provides the methods to maintain the neural network model. `SupervisedBird` uses `Model`
to decide whehter to jump or not, unlike `Bird` in the core game that uses user interaction.

`supervised/trainer.py`

This contains the `GameDataGen` and `SupervisedTrainer` class. `GameDataGen` extends game
and adjusts to collect user data, and allows uer to play once only. `SupervisedTrainer`
extends `GameDataGen` as it also collects data from the play, so to avoid duplication I did
this inheritance. It modifies `loop`, `event_check` and `bird_update` method to make the 
bird jump using AI instead of user invoked events.

------------------------------------------------------------------------------------

Model Descriptions
---

*TO BE CONTINUED*