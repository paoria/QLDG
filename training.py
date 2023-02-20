"""
Here we train the AI
A state is simply the state of the dungeon at a given iteration
The AI is free to modify any cell of the dungeon using the actions; it is not located in space
"""
import numpy as np
import dungeon
import utils
    
"""
This functions trains the AI agent using the Q-learning algorithm
by picking an action at each episode (chosen by epsilon greedy algorithm)
then getting the reward, computing the temporal difference and updating the Q-values
"""
def train_agent(dungeon,epsilon,discount_factor,learning_rate,actions,q_values,rewards,episodes):
    print("Training the agent...\n")
    for episode in range(episodes):
        # pick next action and cell to do said action
        result_tuple = utils.pick_next_action(dungeon,actions,q_values,epsilon)
        cell_x, cell_y, action_id = result_tuple[0], result_tuple[1], result_tuple[2]
    
        # do the action on the chosen cell
        dungeon.cells[cell_x][cell_y].wall_type = action_id    
        
        # pick reward for the action and compute temporal difference
        reward = rewards[cell_x, cell_y, action_id]
        old_q_value = q_values[cell_x, cell_y, action_id]
        temporal_difference = reward + (discount_factor * np.max(q_values[cell_x, cell_y])) - old_q_value
    
        # Bellman equation to update q_values
        new_q_value = old_q_value + (learning_rate * temporal_difference)
        q_values[cell_x, cell_y, action_id] = new_q_value
    
    print("Training complete!\n")

