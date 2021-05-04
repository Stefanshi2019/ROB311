import queue
import numpy as np
from search_problems import Node, GridSearchProblem, get_random_grid_problem
import matplotlib.pyplot as plt

def a_star_search(problem):
    """
    Uses the A* algorithm to solve an instance of GridSearchProblem. Use the methods of GridSearchProblem along with
    structures and functions from the allowed imports (see above) to implement A*.

    :param problem: an instance of GridSearchProblem to solve
    :return: path: a list of states (ints) describing the path from problem.init_state to problem.goal_state[0]
             num_nodes_expanded: number of nodes expanded by your search
             max_frontier_size: maximum frontier size during search
    """
    ####
    #   COMPLETE THIS CODE
    ####
    num_nodes_expanded = 0
    max_frontier_size = 0
    path = []

    # declare start and goal nodes
    goal = Node(problem.goal_states[0], problem.goal_states[0], (problem.goal_states[0], problem.goal_states[0]) , 0)
    head = Node(problem.init_state, problem.init_state, (problem.init_state, problem.init_state), 0)
    num_nodes_expanded += 1

    # set variables
    visited = set()
    frontier = queue.PriorityQueue()

    visited.add(head.state)
    frontier.put((0 + problem.heuristic(head.state), head))

    # if goal is head itself, return itself
    if head.state == goal.state:
        path.append(head.state)
        return path, num_nodes_expanded, max_frontier_size

    # otherwise keep parsing new unexplored nodes
    while frontier.empty() == False:

        # update the maximum frontier size
        if frontier.qsize() > max_frontier_size:
            max_frontier_size = frontier.qsize()

        # extract the current node to explore
        curr_node = frontier.get()[1]
        num_nodes_expanded += 1  # update the number of nodes expanded

        # explore the children of current nodes
        for action in problem.get_actions(curr_node.state):
            child = problem.get_child_node(curr_node, action)
            # if this child has not been visited
            if child.state not in visited:
                # put child in priority queue along with its heuristics
                visited.add(child.state)
                frontier.put((child.path_cost + problem.heuristic(child.state), child))
                # if the child is the target, return the path
                if child.state == problem.goal_states[0]:
                    node = child
                    while node != head:
                        path.append(node.state)
                        node = node.parent
                    path.append(head.state)
                    path.reverse()
                    return path, num_nodes_expanded, max_frontier_size
    # return empty path if not found
    return path, num_nodes_expanded, max_frontier_size


def search_phase_transition():
    """
    Simply fill in the prob. of occupancy values for the 'phase transition' and peak nodes expanded within 0.05. You do
    NOT need to submit your code that determines the values here: that should be computed on your own machine. Simply
    fill in the values!

    :return: tuple containing (transition_start_probability, transition_end_probability, peak_probability)
    """
    ####
    #   REPLACE THESE VALUES
    ####
    transition_start_probability = 0.3
    transition_end_probability = 0.5
    peak_nodes_expanded_probability = 0.35
    return transition_start_probability, transition_end_probability, peak_nodes_expanded_probability


if __name__ == '__main__':
    # Test your code here!
    # Create a random instance of GridSearchProblem
    p_occ = 0.25
    #M = 10
    #N = 10
    N_arr = [20, 100, 500]
    # for N in N_arr:
    occ_prob = []
    solved = []
    avg_nodes_expanded = []
    N = 500

    p_occ = 0.1
    while p_occ <= 0.9:
        solve = 0
        nodes_generate = 0
        problem = get_random_grid_problem(p_occ, N, N)
        path, num_nodes_expanded, max_frontier_size = a_star_search(problem)
        #print(path)
        nodes_generate += num_nodes_expanded
        if path:
            solve += 1
        avg_nodes_expanded.append(nodes_generate // N)
        solved.append(solve)
        occ_prob.append(p_occ)
        p_occ += 0.05
        print(p_occ)



    print(occ_prob)
    print("solved are ", solved)
    print(avg_nodes_expanded)
    plt.plot(occ_prob, solved)
    #plt.plot(occ_prob, avg_nodes_expanded)
    plt.show()
            # x, y = problem.get_position(problem.init_state)
            # x2, y2 = problem.get_position(problem.goal_states[0])
            # print("start is ", x, ' ', y, ' ,end is ', x2, ' ', y2)
            # print(path)
            # correct = problem.check_solution(path)
            # print("Solution is correct: {:}".format(correct))
            # Plot the result
        #problem.plot_solution(path)

    # problem = get_random_grid_problem(p_occ, M, N)
    # # Solve it
    # path, num_nodes_expanded, max_frontier_size = a_star_search(problem)
    # # Check the result
    # x, y =problem.get_position(problem.init_state)
    # x2, y2 = problem.get_position(problem.goal_states[0])
    # print("start is ", x, ' ', y, ' ,end is ', x2, ' ', y2)
    # print(path)
    # correct = problem.check_solution(path)
    # print("Solution is correct: {:}".format(correct))
    # # Plot the result
    # problem.plot_solution(path)

    # Experiment and compare with BFS