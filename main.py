import os
import pickle as pkl
from enum import IntEnum
import random

processed_levels_path = "./TheVGLC-master/Super Mario Bros/Processed/"

# Class specifying directions
class Action(IntEnum):
    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3

# Convert direction obect to tuple 
def actions_to_dxdy(action: Action):
    mapping = {
        Action.LEFT: (-1, 0),
        Action.DOWN: (0, -1),
        Action.RIGHT: (1, 0),
        Action.UP: (0, 1),
    }
    return mapping[action]

# Get tiles surrounding a tile
def get_tile(level,x,y,action):
    max_x = len(level[0])-1
    max_y = len(level)-1
    action = actions_to_dxdy(action=action)
    if action[0] + x > max_x or action[0] + x < 0:
        return None
    if action[1] + y > max_y or action[1] + y < 0:
        return None
    return level[action[1]+y][action[0]+x]
    
# Get ascii levels from VGLC
def get_levels(processed_levels_path):
    processed_levels = {}
    if "processed_levels.pkl" not in os.listdir():
        for file_name in os.listdir(processed_levels_path):
            with open (processed_levels_path + file_name,"r") as file:
                processed_levels[file_name.split(".")[0]] = str(file.read()).split("\n")[:-1]
        with open("processed_levels.pkl","wb") as file:
            pkl.dump(processed_levels,file)
    else:
        with open("processed_levels.pkl","rb") as file:
            processed_levels = pkl.load(file)
    return processed_levels

# Parse all ascii levels to get directional constraints for each unique tile set
def get_constraints(processed_levels):
    constraints = {}
    directions = [Action.LEFT,Action.DOWN,Action.RIGHT,Action.UP]
    for level in processed_levels.values():
        
        for y in range(len(level)):
            
            for x in range(len(level[y])):
                
                current_tile = level[y][x]
                if current_tile not in constraints.keys():
                    constraints[current_tile] = [dict() for i in range(4)]

                for tile_step in directions:
                    tile = get_tile(level,x,y,tile_step)
                    if tile:
                        if tile in constraints[current_tile][tile_step].keys():      
                            constraints[current_tile][tile_step][tile] += 1
                        else:
                            constraints[current_tile][tile_step][tile] = 1
    return constraints

# Generate an empty level
def get_empty_layout(x,y,tile_map): 
    map = [[set(tile_map.keys()) for x_val in range(x)] for y_val in range(y)]
    return map

# Generate level from an empty layout and a seet
def generate_level(x,y,tile_map,constraints):
    
    level = get_empty_layout(x,y,tile_map)

    for y_val in range(y):
        level[y_val][0] = "-"
    
    for y_val in range(y):
        level[y_val][x-1] = "-"

    for x_val in range(0,x):
        level[0][x_val] = '-'

    for x_val in range(15):
        level[y-1][x_val] = "X" 

    for x_val in range(15):
        level[y-1][x - x_val-1] = "X" 
   
    for x_val in range(15,x-15):
        level[y-1][x_val] = get_floor_tile(level[y-1][x_val-1],constraints)

    update_constraints(x,y,level,constraints)

    # Then populate the center
    # Maybe we should do it from the bottom up
    # Should we do MDPs? Markov chains?
    # OK lets do WFC + MdMC, but then why do WFC?
    try:
        while(not is_stable(x,y,level)):
            wave_function_collapse(x,y,level,constraints)
        

        for y_val in range(y):
            level[y_val] = "".join(level[y_val] )

        level = "\n".join(level)    

    except:
        # Basically if something happens which makes further progression difficult/impossible
        # Start from the beginning
        return generate_level(x,y,tile_map,constraints)
    return level

# Check if any value in level is anything but a string
def is_stable(x,y,level):
    for y_val in range(y):
        for x_val in range(x):
            if type(level[y_val][x_val]) == set or type(level[y_val][x_val]) == list:
                return False
    return True

# Whenever this is called, do the following in this order
# 1. Find most constrained, or set of least constrained cells
# 2. Based on cells surrounding it, disambiguate it more
# 3. For any values which are stable, disambiguate cells around them
def wave_function_collapse(x,y,level,constraints):

    # First find most constrained cell then perform wave function collapse
    x_val,y_val = find_least_constrained(x,y,level)
    level[y_val][x_val] = get_next_tile(level[y_val][x_val],level[y_val-1][x_val],level[y_val][x_val-1],level[y_val+1][x_val],level[y_val][x_val+1],constraints)
    update_constraints(x,y,level,constraints)

    
def find_least_constrained(x,y,level):
    least_constraints = 13 # Maximum possible constraints
    cells = []
    for y_val in range(y):
        for x_val in range(x):
            tile = level[y_val][x_val]
            if type(tile) == set or type(tile) == list:
                if len(tile) <= least_constraints:
                    least_constraints = len(tile)
                    cells.append(((x_val,y_val),least_constraints))
    
    least_constrained = [cell[0] for cell in cells if cell[1] == least_constraints]
    if least_constrained:
        return random.choice(least_constrained)
    else:
        print("ERROR HERE")
        least_constrained = [cell[0] for cell in cells]
        return random.choice(least_constrained)

# WFC for the floor
def get_floor_tile(prev_floor,constraints):
    constraining = []
    if type(prev_floor) != set:
        constraining.append(constraints[prev_floor][Action.RIGHT])
    return do_the_collapse(set(["X","-"]),constraining,constraints)

# Wave function collpse for all other type of tiles
def get_next_tile(tile_set,below_tile,left_tile,top_tile,right_tile,constraints):
    constraining = []
    if type(below_tile) is str:
        constraining.append(constraints[below_tile][Action.UP])
    if type(left_tile) is str:
        constraining.append(constraints[left_tile][Action.RIGHT])
    if type(top_tile) is str:
        constraining.append(constraints[top_tile][Action.DOWN])
    if type(right_tile) is str:
        constraining.append(constraints[right_tile][Action.LEFT])

    return do_the_collapse(tile_set,constraining,constraints)

# Perform collapse
def do_the_collapse(tile_set, constraining, constraints):
    possible_tiles = [set(constraint.keys()) for constraint in constraining ]
    possible_tiles = set.intersection(*possible_tiles)
    possible_tiles = set.intersection(tile_set)
    
    # If there are no constraining tiles, choose from the entire tile set
    if not possible_tiles:
        possible_tiles = tile_set
    
    probabilities = {tile: 0 for tile in constraints.keys()}

    # For any tile and constraint, additively compile probability of each tile
    for constraint in constraining:
        tile_counts = {tile: 0.01 for tile in possible_tiles}

        for tile, count in constraint.items():
            if tile in possible_tiles:
                tile_counts[tile] += count

        for tile,counts in tile_counts.items():
            total_counts = sum(tile_counts.values())

            probabilities[tile] = probabilities[tile]+(counts/total_counts) 
    
    chosen_tile = random.choices(list(probabilities.keys()), weights=list(probabilities.values()))[0]
    return chosen_tile

# After WFC, update all surrounding tiles
def update_constraints(xl,yl,level,constraints):
    directions = [Action.LEFT, Action.DOWN, Action.RIGHT, Action.UP]

    for y in range(1, yl-1 - 1):  # Exclude edges
        for x in range(1, xl - 1):  # Exclude edges
            current_tile = level[y][x]

            if type(current_tile) is not set:
                continue  # Skip stable tiles

            neighbors = {
                Action.LEFT: level[y][x - 1],
                Action.DOWN: level[y + 1][x],
                Action.RIGHT: level[y][x + 1],
                Action.UP: level[y - 1][x]
            }
            possible_tiles = []
            for direction,neighbor in neighbors.items():
                if type(neighbor) == str:
                    possible_tiles.append(set(constraints[neighbor][direction].keys()))
            if possible_tiles:
                level[y][x] = set.intersection(*possible_tiles)

# Get all unique tiles and map them to a number
def create_tile_map(tileset):
    map = {}
    for tile in range(len(tileset)):
        map[tileset[tile]] = tile 
    return map

processed_levels = get_levels(processed_levels_path=processed_levels_path)

constraints = get_constraints(processed_levels)

tile_map = create_tile_map(list(constraints.keys()))

num_levels = 200
for i in range(num_levels):
    print(i)
    if i < 100:
        generated_level = generate_level(200,14,tile_map,constraints) 
    else:
        generated_level = generate_level(100,10,tile_map,constraints) 
    with open("./Generated_Levels/mario_"+str(i)+".txt","w+") as file:
        file.write(generated_level)
