import numpy as np
import random

"""
The Cell class represents a cell located at a given position in the dungeon
Its wall type is one of 16 possible configurations for walls as given in the Dungeon.conversion dictionary
"""
class Cell:
    def __init__(self,wall_type):
        
        self.wall_type = wall_type
        # cells are initialized as not being keypoints
        self.is_entrance = False
        self.is_treasure = False
        self.is_exit = False
        
        # below a list of wall types featuring a specific wall
        self.south_walls = [3,6,7,9,11,12,13]
        self.west_walls = [4,7,8,10,12,13,14]
        self.north_walls = [1,5,8,9,11,13,14]
        self.east_walls = [2,5,6,10,11,12,14]
        
    """
    The functions below determine whether a given cell has a certain wall based on their wall_type
    """
    def has_west_wall(self):
        if self.wall_type in self.west_walls:
            return True
        else: 
            return False
    def has_north_wall(self):
        if self.wall_type in self.north_walls:
            return True
        else: 
            return False
    def has_east_wall(self):
        if self.wall_type in self.east_walls:
            return True
        else: 
            return False
    def has_south_wall(self):
        if self.wall_type in self.south_walls:
            return True
        else: 
            return False

"""
The Dungeon class gives us the size of the dungeon and its cells
As well as many utility functions
"""
class Dungeon:
    def __init__(self, width, height):

        self.width = width 
        self.height = height 
        self.ncells = self.width*self.height # number of cells in the dungeon
        
        # dictionary for cell wall type/configuration to string conversion
        # ██ are walls
        # :: are broken/open walls
        self.conversion = {
            0: """██::██
::  ::
██::██""", # no walls
            1: """██████
::  ::
██::██""", # single wall north
            2: """██::██
::  ██
██::██""", # single wall east
            3: """██::██
::  ::
██████""", # single wall south
            4: """██::██
██  ::
██::██""", # single wall west
            5: """██████
::  ██
██::██""", # double wall north + east
            6: """██::██
::  ██
██████""", # double wall east + south
            7: """██::██
██  ::
██████""", # double wall south + west
            8: """██████
██  ::
██::██""", # double wall west + north
            9: """██████
::  ::
██████""", # double wall north + south
            10: """██::██
██  ██
██::██""", # double wall west + east
            11: """██████
::  ██
██████""", # triple wall north + east + south
            12: """██::██
██  ██
██████""", # triple wall east + south + west
            13: """██████
██  ::
██████""", # triple wall south + west + north
            14: """██████
██  ██
██::██""", # triple wall west + north + east
            15: """██████
██  ██
██████""" # quadruple wall
        }
        
        # creates a 2d-array of cells representing our dungeon
        self.cells = [[Cell(np.random.choice(15)) for x in range(self.width)] for y in range(self.height)]
        
    
    """
    Prints a text representation of the dungeon
    Entrance is green, treasure is yellow, exit is red
    """
    def __repr__(self):
        # print multiline strings next to each other
        for y in range(self.height):
            lines = []
            for x in range(self.width):
                if self.cells[y][x].is_entrance:                    
                    lines.append(self.conversion[self.cells[y][x].wall_type].replace("  ","\033[0;32m██\033[0;0m").splitlines())
                elif self.cells[y][x].is_treasure:
                    lines.append(self.conversion[self.cells[y][x].wall_type].replace("  ","\033[0;33m██\033[0;0m").splitlines())
                elif self.cells[y][x].is_exit:
                    lines.append(self.conversion[self.cells[y][x].wall_type].replace("  ","\033[0;31m██\033[0;0m").splitlines())
                else:
                    lines.append(self.conversion[self.cells[y][x].wall_type].splitlines())            
            for line in zip(*lines):
                print(*line, sep='')
        return("")     
    

        
    """
    Returns a list of cells immediately (neighbours) connected to the one at (x,y) (with open walls)
    """  
    def find_connected_cells(self,x,y):
        connected_cells = []
        if y != 0:
            if (self.cells[x][y].has_west_wall() == False and self.cells[x][y-1].has_east_wall() == False): connected_cells.append([x,y-1])
        if y != 3:        
            if (self.cells[x][y].has_east_wall() == False and self.cells[x][y+1].has_west_wall() == False): connected_cells.append([x,y+1])
        if x != 3:
            if (self.cells[x][y].has_south_wall() == False and self.cells[x+1][y].has_north_wall() == False): connected_cells.append([x+1,y])
        if x != 0:
            if (self.cells[x][y].has_north_wall() == False and self.cells[x-1][y].has_south_wall() == False): connected_cells.append([x-1,y])
        return connected_cells
        
    
    """
    Finds and returns the longest existing path in a given dungeon, i.e. longest streak of connected cells
    """
    def find_longest_path(self):
        previous_longest_path = []
        longest_path = []
        mid_indices = [[1,1],[1,2],[2,1],[2,2]]
        # start on middle cells which have the best chance to be on the longest path
        while len(mid_indices) > 0:
            ind = mid_indices[0]
            mid_indices.remove(ind)
            current_longest_path = []
            neighbours = []
            current_longest_path.append(ind)            
            # from there, find neighbours of neighbours until none exist
            neighbours = self.find_connected_cells(ind[0],ind[1])
            while len(neighbours) > 0:
                neighbour = neighbours[0]
                current_longest_path.append(neighbour)
                neighbours.remove(neighbour)
                if neighbour in mid_indices: mid_indices.remove(neighbour)
                new_neighbours = self.find_connected_cells(neighbour[0],neighbour[1])
                neighbours += [ngb for ngb in new_neighbours if ngb not in current_longest_path] 
            # if we found a longer path than before, update it
            if len(current_longest_path) > len(previous_longest_path):
                previous_longest_path = list(current_longest_path) 
        [longest_path.append(path) for path in previous_longest_path if path not in longest_path]
        longest_path.sort()
        return longest_path
    
    
    """
    Sample three cells along the longest path of the dungeon (connected_cells) and make them keypoints
    """
    def add_key_points(self,connected_cells):        
        key_indices = random.sample(connected_cells,3)
        self.cells[key_indices[0][0]][key_indices[0][1]].is_entrance = True
        self.cells[key_indices[1][0]][key_indices[1][1]].is_treasure = True  
        self.cells[key_indices[2][0]][key_indices[2][1]].is_exit = True
