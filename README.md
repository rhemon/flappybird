# Flappy Bird

## Start How-To(s)

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
$ python game.py
```

### 2. Starting Training with Genetic Algorith
- With all packages installed, just run
```
$ python generation.py
```

## File Descritions

#### bird.py

Contains Bird, Chromosome and BirdWithGenes class.
Bird class is used for the simple game. Where BirdWithGenes used in the genetic algorithm version where it uses Chromosome which basically holds the neural network
weights and functions to calculate the decision.

------------------------------------------------------------------------------------

#### obstacles.py

Contains Obstacle class. Prepares and handles the obstacles of the game.
Here each obstacle are simply the boxes that leave a small gap inbetween.

------------------------------------------------------------------------------------

#### game.py

Contains the game class that handles the game loop and states.

------------------------------------------------------------------------------------

#### generation.py

Handles the loop to train the bird ai through genetic algorithm.

------------------------------------------------------------------------------------
