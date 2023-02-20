# this is a dungeon map generator trained using a Q-learning algorithm

import numpy as np
import random
import dungeon as dg
import utils
import training


"""
First train the AI agent
"""

# initialize training dungeon
training_dungeon = dg.Dungeon(4,4)
# actions are changing a dungeon cell to one of the 16 wall configurations
# as in the conversion dictionary from the Dungeon class
actions = np.arange(training_dungeon.ncells)
# 3D array for the Q function, storing a value for each (x,y,action) triplet, initialized at zero everywhere
q_values = np.zeros((training_dungeon.width, training_dungeon.height, len(actions)))
# initialize rewards based on desired dungeon shape
rewards = utils.initialize_rewards(training_dungeon)

# training parameters
epsilon = 0.1 # used in the epsilon greedy function to determine whether to explore or exploit; small epsilon favors exploration
discount_factor = 0.8 # weight for future rewards
learning_rate = 0.8 # weight for rate of q_value changes
episodes = 2000 # training iterations

# call the training function!
training.train_agent(training_dungeon,epsilon,discount_factor,learning_rate,actions,q_values,rewards,episodes)


"""
Then generate dungeons as you please
Now that the algorithm is trained, we use it to alter a newly generated random dungeon
by letting the IA do a full sweep of modifications, optimally picked from trained q_values, to the dungeon
"""

"""
The function goes over every cell of a dungeon to make at most one change to each
The change to each cell is picked at random between best choices to ensure every dungeon is different
The resulting dungeon should have closed exterior walls and a big enough path (controlled by path_size_threshold)
The has_keypoints boolean is for opting in or out of keypoints. If True, the dungeon will have an entrance, 
a treasure, and an exit along the longest path
"""
def make_suitable_dungeon(path_size_threshold,has_keypoints):
    print("Generating a dungeon...\n")
    # initialize a random dungeon
    dung = dg.Dungeon(4,4)
    path_length = 0 # the largest path of connected cells in the dungeon
    connected_cells = []
    while path_length < path_size_threshold: # keep only dungeons with at least path_size_threshold connected cells
        for i in range(dung.height):
            for j in range(dung.width):
                action_id = utils.pick_next_action_localized(i,j,q_values,1)
                dung.cells[i][j].wall_type = action_id
        connected_cells = dung.find_longest_path()
        path_length = len(connected_cells)  
    # add key points randomly along longest path if keypoints opted in
    if has_keypoints:
       dung.add_key_points(connected_cells)
    return dung        



# change these two values to alter dungeon generation
minimum_longest_path_length = 12
keypoints = True

user_input = ""
while user_input.upper() != "Q":
    # let the AI agent craft a dungeon and print it afterwards
    # walls are black, :: are open walls, entrance is green, treasure is yellow, exit is red
    new_dungeon = make_suitable_dungeon(minimum_longest_path_length,keypoints)
    print(new_dungeon)
    print("\nDungeon generated! Generate another one? (Enter for yes, Q to quit)")
    user_input = input()
