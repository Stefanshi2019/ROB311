# mdp_grid_task.py: Project 4
#
# --
# Artificial Intelligence
# ROB 311 Winter 2020
# Programming Project 4
#
# --
# University of Toronto Institute for Aerospace Studies
# Stars Lab
#
# Course Instructor:
# Dr. Jonathan Kelly
# jkelly@utias.utoronto.ca
#
# Teaching Assistant:
# Matthew Giamou
# mathhew.giamau@robotics.utias.utoronto.ca
#
# Abhinav Grover
# abhinav.grover@robotics.utias.utoronto.ca

###
# Imports
###

import numpy as np
from mdp_env import mdp_env

class grid_env(mdp_env):
    """
        cleaning_env class stores all the cleaning enviroment related functions and attributes.
        This is a grid world environment with two terminal states and 6 adjoining states.

        Attributes
        ------------------
            states_names:  List of names associated with the Unique state IDs
            action_names:  List of names associated with the Unique action IDs
            transition_model:  Matrix of size (SxSxA) specifying all of the
                               transition probabilities
    """
    def __init__(self):
        """
            INIT function
        """

        # Init the super class
        states = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        terminal = (3, 6)
        actions = (0, 1, 2, 3)
        rewards = (-0.04, -0.04, -0.04, 1, -0.04, -0.04, -1, -0.04, -0.04, -0.04, -0.04)
        super().__init__(states, actions, terminal, rewards)

        # Init owner attributes
        self.state_positions = [[1,3], [2,3], [3,3], [4,3], \
                                [1,2],        [3,2], [4,2], \
                                [1,1], [2,1], [3,1], [4,1]]
        self.state_names = ("(1,3)", "(2,3)", "(3,3)", "(4,3)", \
                            "(1,2)",          "(3,2)", "(4,2)", \
                            "(1,1)", "(2,1)", "(3,1)", "(4,1)")
        self.action_names = ("U", "D", "L", "R")
        self.transition_model = []
        self.init_stochatic_model()

    def init_stochatic_model(self):
        """
            init_stochatic_model method initializes the transition probability table for the the
            cleaning task.
                Inputs:
                    get_transition_model: User Implemented method that defines the transition model
                    for the cleaning environment
        """
        P = np.zeros([len(self.states), len(self.states), len(self.actions)])

        ## OPTIONAL
        P[0, 0] = [0.9, 0.1, 0.9, 0.1]
        P[0, 1] = [0.1, 0.1, 0.0, 0.8]
        P[0, 4] = [0.0, 0.8, 0.1, 0.1]

        P[1, 1] = [0.8, 0.8, 0.2, 0.2]
        P[1, 0] = [0.1, 0.1, 0.8, 0.0]
        P[1, 2] = [0.1, 0.1, 0.0, 0.8]

        P[2, 2] = [0.8, 0.0, 0.1, 0.1]
        P[2, 1] = [0.1, 0.1, 0.8, 0.0]
        P[2, 3] = [0.1, 0.1, 0.0, 0.8]
        P[2, 5] = [0.0, 0.8, 0.1, 0.1]

        P[4, 4] = [0.2, 0.2, 0.8, 0.8]
        P[4, 0] = [0.8, 0.0, 0.1, 0.1]
        P[4, 7] = [0.0, 0.8, 0.1, 0.1]

        P[5, 5] = [0.1, 0.1, 0.8, 0.0]
        P[5, 2] = [0.8, 0.0, 0.1, 0.1]
        P[5, 6] = [0.1, 0.1, 0.0, 0.8]
        P[5, 9] = [0.0, 0.8, 0.1, 0.1]

        P[7, 7] = [0.1, 0.9, 0.9, 0.1]
        P[7, 4] = [0.8, 0.0, 0.1, 0.1]
        P[7, 8] = [0.1, 0.1, 0.0, 0.8]

        P[8, 8] = [0.8, 0.8, 0.2, 0.2]
        P[8, 7] = [0.1, 0.1, 0.8, 0.0]
        P[8, 9] = [0.1, 0.1, 0.0, 0.8]

        P[9, 9] = [0.0, 0.8, 0.1, 0.1]
        P[9, 8] = [0.1, 0.1, 0.8, 0.0]
        P[9, 5] = [0.8, 0.0, 0.1, 0.1]
        P[9, 10] = [0.1, 0.1, 0.0, 0.8]

        P[10, 10] = [0.1, 0.9, 0.1, 0.9]
        P[10, 9] = [0.1, 0.1, 0.8, 0.0]
        P[10, 6] = [0.8, 0.0, 0.1, 0.1]

        self.transition_model = P

    def print_env(self):
        """
            This function prints the environment using state names
        """
        print("\n------------- Environment -------------- ")
        print_string = ""
        row = self.state_positions[0][1]
        col = self.state_positions[0][0]
        for j in range(len(self.states)):
            # Nextline for change in row
            if row != self.state_positions[j][1]:
                print_string += "\n"
                row = self.state_positions[j][1]
            if abs(col - self.state_positions[j][0]) == 2:
                print_string += "\t"
            col = self.state_positions[j][0]

            # Print state_name
            print_string += "\t" + self.state_names[j] + ","
            if self.states[j] in self.terminal:
                print_string = print_string + "T"
        print(print_string)

    def print_transition_model(self):
        """
            This function prints the whole transition table
        """
        print("\n------------- Transition Model -------------- ")
        print("rows -> from-state | columns -> to-state")

        print_string = "\t\t\t"
        for i in range(len(self.states)):
            print_string += self.state_names[i] + "\t\t\t\t"

        print_string += "\n"
        for i in range(len(self.states)):
            print_string += self.state_names[i] + "\t"
            for j in range(len(self.states)):
                print_string += str(self.transition_model[i, j, 0])
                for k in range(1, len(self.actions)):
                    print_string += ", " + str(self.transition_model[i, j, k])
                print_string += "\t"
            print_string += "\n"
        print(print_string)