"""
Plots the progress with reinforcemnet learning.
Updates the graph every 5seconds to reread the saved
progress into file.

@author Ridhwanul Haque
@version 22.04.2020
"""

import numpy as np
from matplotlib import style
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from qlearning.trainer import ReinforcedTrainer

fig, axs = plt.subplots(2)
ax1, ax2 = axs
fig.suptitle(ReinforcedTrainer.REWARDS_HISTORY_FILE)

def plotter(i):
    try:
        rewards_history = list(np.load(ReinforcedTrainer.REWARDS_HISTORY_FILE)['rewards'])
    except:
        return

    ax1.clear()
    ax2.clear()
    ax1.plot(rewards_history[0], rewards_history[1], label="Min Reward") # min
    ax1.plot(rewards_history[0], rewards_history[2], label="Max Reward") # max
    ax1.plot(rewards_history[0], rewards_history[3], label="Avg Reward") # avg
    ax2.plot(rewards_history[0], rewards_history[4], label="Min Score") # min
    ax2.plot(rewards_history[0], rewards_history[5], label="Max Score") # max
    ax2.plot(rewards_history[0], rewards_history[6], label="Avg Score") # avg
    ax1.legend()
    ax2.legend()
    
ani = animation.FuncAnimation(fig, plotter, interval=5000)

plt.show()
