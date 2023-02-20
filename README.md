# QLDG
 Q-learning dungeon generator

Prerequisites: Python 3.x, numpy, random

How to use: run main.py from a folder containing every file in this repository

The code first trains an AI agent how to generate dungeons using Q-learning. The resulting dungeons have a size of 4x4 and closed exterior walls, as well as a long path on which lie an entrance, treasure and exit. 

Here is an example of a generated dungeon:

████████████████████████
██  ██::  ::::  ::::  ██
██::████████████████::██
████████::████::████::██
██  ::::  ::::  ::::  ██
██::████::████::████████
██::████::████::████::██
██  ██::  ██::  ████  ██
████████::████::████████
████████::██████████::██
██  ::::  ██::  ::::  ██
████████████████████████

Each of the cells is represented with 8 walls around it. The diagonal walls are always closed. The four other ones have all possible combinations. :: represent open walls. 

The agent has free control over the dungeon during training. A state is the global view of the dungeon and its cells at a training episode. The actions are changing a single cell's wall configuration (16 possibilities). At each episode, an action is picked and the agent gets a reward or punishment, which is used to update the Q-function. The rewards are tied to each action and cell, and initialized in such a way that the dungeon will comply to the requirements. 

Once training is complete, the agent can generate a vast range of different dungeons, with or without keypoints, and with a specified minimum path length. Keypoints are not part of the Q-learning process and are added after dungeon generation on the longest existing path. 

Evaluation metric: a possible metric that could be used to evaluate the difficulty of the dungeon would be the number of moves one has to make to go from entrance to treasure and from treasure to exit. 




