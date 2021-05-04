"""
    Problem 3 Template file
"""
import random
import math

import numpy as np

"""
Problem Statement
--------------------
Implement the planning algorithm called Rapidly-Exploring Random Trees (RRT)
for a problem setup given by the "RRT_dubins_problem" class.

INSTRUCTIONS
--------------------
1. The only file to be submitted is this file "rrt_planning.py". Your implementation
   can be tested by running "RRT_dubins_problem.py" (see the "main()" function).
2. Read all class and function documentation in "RRT_dubins_problem.py" carefully.
   There are plenty of helper functions in the class that you should use.
3. Your solution must meet all the conditions specificed below.
4. Below are some DOs and DONTs for this problem.

Conditions
-------------------
There are some conditions to be satisfied for an acceptable solution.
These may or may not be verified by the marking script.

1. The solution loop must not run for more that a certain number of random points
   (Specified by a class member called MAX_ITER). This is mainly a safety
   measure to avoid time-out related issues and will be generously set.
2. The planning function must return a list of nodes that represent a collision free path
   from the start node to the goal node. The path states (path_x, path_y, path_yaw)
   specified by each node must be a Dubins-style path and traverse from node i-1 -> node i.
   (READ the documentation of the node to understand the terminology)
3. The returned path should be a valid list of nodes with a Dubins-style path connecting the nodes. 
   i.e. the list should have the start node at index 0 and goal node at index -1. 
   For all other indices i in the list, the parent node for node i should be at index i-1,  
   (READ the documentation of the node to understand the terminology)
4. The node locations must not lie outside the map boundaries specified by
   "RRT_dubins_problem.map_area"

DO(s) and DONT(s)
-------------------
1. DO rename the file to rrt_planning.py for submission.
2. Do NOT change change the "planning" function signature.
3. Do NOT import anything other than what is already imported in this file.
4. We encourage you to write helper functions in this file in order to reduce code repetition
   but these functions can only be used inside the "planning" function.
   (since only the planning function will be imported)
"""

def planning(rrt_dubins, display_map=False):
    """
        Execute RRT planning using dubins-style paths. Make sure to populate the node_lis

        Inputs
        -------------
        rrt_dubins  - (RRT_DUBINS_PROBLEM) Class conatining the planning
                      problem specification
        display_map - (boolean) flag for animation on or off (OPTIONAL)

        Outputs
        --------------
        (list of nodes) This must be a valid list of connected nodes that form
                        a path from start to goal node

        NOTE: In order for rrt_dubins.draw_graph function to work properly, it is important
        to populate rrt_dubins.nodes_list with all valid RRT nodes.
    """
    # Fix Randon Number Generator seed
    random.seed(1)
    path = []
    # LOOP for max iterations
    i = 0
    while i < rrt_dubins.max_iter:
        i += 1

        # Generate a random vehicle state (x, y, yaw)
        x = random.uniform(rrt_dubins.x_lim[0], rrt_dubins.x_lim[1])
        y = random.uniform(rrt_dubins.y_lim[0], rrt_dubins.y_lim[1])
        yaw = random.uniform(-math.pi, math.pi)
        rand_node = rrt_dubins.Node(x, y, yaw)

        # Find an existing node nearest to the random vehicle state
        nearest_node = find_nearest_node(rrt_dubins, rand_node)
        curr_node = rrt_dubins.propogate(nearest_node, rand_node)

        # Check if the path between nearest node and random state has obstacle collision
        # Add the node to nodes_list if it is valid
        if rrt_dubins.check_collision(curr_node):
            rrt_dubins.node_list.append(curr_node)
            # try to extend to the goal node
            reachable = rrt_dubins.propogate(curr_node, rrt_dubins.goal)
            # if no collision, goal can be reached
            if rrt_dubins.check_collision(reachable) == True:
                return back_trace(reachable)

        # Draw current view of the map
        # PRESS ESCAPE TO EXIT
        if display_map:
            rrt_dubins.draw_graph()

        # Check if new_node is close to goal
        if True:
            print("Iters:", i, ", number of nodes:", len(rrt_dubins.node_list))


    if i == rrt_dubins.max_iter:
        print('reached max iterations')

    # Return path, which is a list of nodes leading to the goal

    return path


def find_nearest_node(rrt_dubins, rand_node):
    # find the nearest valid node to rand_node
    nearest_node = None
    min_cost = float('inf')
    for node in rrt_dubins.node_list:
        cost = math.sqrt((rand_node.x - node.x) ** 2 + (rand_node.y - node.y) ** 2)
        if cost < min_cost:
            min_cost = cost
            nearest_node = node
    return nearest_node


def back_trace(node):
    # trace the path once the goal is reached
    path = []
    prev = node
    while prev != None:
        path.append(prev)
        prev = prev.parent
    path.reverse()

    return path

