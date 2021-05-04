from collections import deque
import numpy as np
from search_problems import Node, GraphSearchProblem

def breadth_first_search(problem):
    """
    Implement a simple breadth-first search algorithm that takes instances of SimpleSearchProblem (or its derived
    classes) and provides a valid and optimal path from the initial state to the goal state. Useful for testing your
    bidirectional and A* search algorithms.

    :param problem: instance of SimpleSearchProblem
    :return: path: a list of states (ints) describing the path from problem.init_state to problem.goal_state[0]
             num_nodes_expanded: number of nodes expanded by your search
             max_frontier_size: maximum frontier size during search
    """
    ####
    #   COMPLETE THIS CODE
    ####


    max_frontier_size = 0
    num_nodes_expanded = 0
    path = []

    # a dict that remembers the parent of the indexed node,
    # key is the state id, value is the node
    parent_nodes = {}
    # a list that stores the state ids of the visted states
    visited = []
    frontier = deque()

    # declare head node
    head = Node(0, problem.init_state, (0, 0), 0)
    # initial conditions for variables
    num_nodes_expanded += 1
    parent_nodes[head.state] = None
    frontier.append(head)
    visited.append(head.state)

    # keep exploring as long as there is unexplored nodes
    while len(frontier) > 0:
        # update max_frontier_size
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
        current_state = frontier.pop()
        num_nodes_expanded += 1
        for action in problem.get_actions(current_state.state):
            child = problem.get_child_node(current_state, action)
            # if the child node has not been visited
            if child.state not in visited:
                parent_nodes[child.state] = current_state
                visited.append(child.state)
                # if the child is the target state
                if child.state == problem.goal_states[0]:
                    # back trace the path, the path will be reversed
                    curr = child
                    path.append(curr.state)
                    while curr != head:
                        curr = parent_nodes[curr.state]
                        path.append(curr.state)
                    # reverse the path
                    path.reverse()
                    return path, num_nodes_expanded, max_frontier_size
                frontier.append(child)

    return path, num_nodes_expanded, max_frontier_size


if __name__ == '__main__':
    # Simple example
    goal_states = [0]
    init_state = 9
    V = np.arange(0, 10)
    E = np.array([[0, 1],
                  [1, 2],
                  [2, 3],
                  [3, 4],
                  [4, 5],
                  [5, 6],
                  [6, 7],
                  [7, 8],
                  [8, 9],
                  [0, 6],
                  [1, 7],
                  [2, 5],
                  [9, 4]])
    problem = GraphSearchProblem(goal_states, init_state, V, E)
    path, num_nodes_expanded, max_frontier_size = breadth_first_search(problem)
    correct = problem.check_graph_solution(path)
    print("Solution is correct: {:}".format(correct))
    print(path)

    # Use stanford_large_network_facebook_combined.txt to make your own test instances
    E = np.loadtxt('stanford_large_network_facebook_combined.txt', dtype=int)
    V = np.unique(E)
    goal_states = [349]
    init_state = 0
    problem = GraphSearchProblem(goal_states, init_state, V, E)
    path, num_nodes_expanded, max_frontier_size = breadth_first_search(problem)
    correct = problem.check_graph_solution(path)
    print("Solution is correct: {:}".format(correct))
    print(path)