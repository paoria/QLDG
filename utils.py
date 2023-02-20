import numpy as np
import random

"""
This function creates and returns the rewards array for the training process
Rewards are based on the conditions for a suitable dungeon (e.g. exterior walls closed, long path)
"""
def initialize_rewards(dungeon):
    # initialize every reward at -20
    rewards = np.full((dungeon.width, dungeon.height, dungeon.ncells), -20.)
    # reward for closing top left corner
    rewards[0][0][8], rewards [0][0][13], rewards[0][0][14] = 20,20,20 
    # rewards for closing bottom right corner
    rewards[-1][-1][6], rewards[-1][-1][11], rewards[-1][-1][12] = 20,20,20 
    # rewards for closing top right corner
    rewards[0][-1][5], rewards[0][-1][11], rewards[0][-1][14] = 20,20,20 
    # rewards for closing bottom left corner
    rewards[-1][0][7], rewards[-1][0][12], rewards[-1][0][13] = 20,20,20 
    # rewards for closing north walls
    for i in range(1,dungeon.width-1): 
        for j in dungeon.cells[0][0].north_walls:
            rewards[0][i][j] = 20
    # rewards for closing east walls
    for i in range(1,dungeon.height-1): 
        for j in dungeon.cells[0][0].east_walls:
            rewards[i][-1][j] = 20
    # rewards for closing south walls
    for i in range(1,dungeon.width-1): 
        for j in dungeon.cells[0][0].south_walls:
            rewards[-1][i][j] = 20
    # rewards for closing west walls
    for i in range(1,dungeon.height-1):
        for j in dungeon.cells[0][0].west_walls:
            rewards[i][0][j] = 20
    # rewards for leaving center rooms more open (to get long paths more often)
    # by giving them at most one wall
    for i in range (1,dungeon.height-1):
        for j in range(1,dungeon.width-1):
            rewards[i][j][0:5] = 10
    return rewards


"""
Get a random argmax from an array in case of tie
"""
def randargmax(arr,**kw):
    return np.argmax(np.random.random(arr.shape) * (arr==arr.max()), **kw)  


"""
Returns the indices corresponding to the n maximum values from a numpy array
"""
def largest_indices(arr, n):
    flat = arr.flatten()
    indices = np.argpartition(flat, -n)[-n:]
    indices = indices[np.argsort(-flat[indices])]
    unraveled = np.unravel_index(indices, arr.shape)
    return [[unraveled[j][i] for j in range(len(arr.shape))] for i in range(n)]


# during training, the next action is chosen using an epsilon greedy algorithm
# this determines the percentage of actions that will be "greedy", i.e. of random exploration, 
# rather than the optimal one from current q_values
"""
The function returns a tuple (cell_x,cell_y,action_id) corresponding to the action the AI will do
"""
def pick_next_action(dungeon,actions,q_values,epsilon):
    if np.random.random() < epsilon:
        # epsilon test passed; pick most efficient action
        #return np.unravel_index(randargmax(q_values,axis=None),q_values.shape)
        return random.choice(largest_indices(q_values,5))
    else:
        # pick random integers for the tile to modify, and one for the action to perform
        return (np.random.randint(dungeon.width), np.random.randint(dungeon.height), np.random.randint(len(actions)))

    
"""
Like pick_next_action, but for a specific cell with (x,y) coordinates
Only returns the action id
"""
def pick_next_action_localized(x,y,q_values,epsilon):
    if np.random.random() < epsilon:
        return random.choice(largest_indices(q_values[x][y],3))[0]
    else:
        return random.choice(q_values[x][y])     

