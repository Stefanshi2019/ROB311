from collections import deque
import numpy as np
from search_problems import Node, GraphSearchProblem
from breadth_first_search import *

def bidirectional_search(problem):
    """
        Implement a bidirectional search algorithm that takes instances of SimpleSearchProblem (or its derived
        classes) and provides a valid and optimal path from the initial state to the goal state.

        :param problem: instance of SimpleSearchProblema
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
    paths = []

    # head = Node(0, problem.init_state, (problem.init_state,problem.init_state), 0)
    # tail = Node(0, problem.goal_states[0], (problem.goal_states[0],problem.goal_states[0]), 0)
    #
    head = problem.init_state
    tail = problem.goal_states[0]
    num_nodes_expanded += 2

    # # a dict that remembers the parent of the indexed node,
    # # key is the state id, value is the node
    # parent_nodes = {}
    # a list that stores the state ids of the visted states
    head_visited = set()
    tail_visited = set()
    head_frontier = deque()
    tail_frontier = deque()
    head_parents = {}
    tail_parents = {}

    head_parents[head] = head
    tail_parents[tail] = tail

    # initial conditions for vars
    head_visited.add(head)
    tail_visited.add(tail)
    head_frontier.append(head)
    tail_frontier.append(tail)

    intersect_costs = dict()
    optimal_intersect = -1
    optimal_cost = float('inf')
    moretrials = 0
    while len(head_frontier) != 0 and len(tail_frontier) != 0:
        # if len(head_frontier) + len(tail_frontier)  > max_frontier_size:
        #     max_frontier_size = len(frontier)
        curr_hn = head_frontier.pop()
        num_nodes_expanded += 1
        for child in problem.neighbours[curr_hn]:
            if child not in head_visited:
                head_parents[child] = curr_hn
                head_visited.add(child)
                # if this node is visited by the other side, then we know there is a path
                if child in tail_visited:
                    # cost = head_parents[child].path_cost + tail_parents[child].path_cost + 2
                    # if cost < optimal_cost:
                    #     optimal_cost = cost
                    #     optimal_intersect = child
                    path1 = []
                    curr = head_parents[child]
                    while curr != head:
                        path1.append(curr)
                        curr = head_parents[curr]
                    path1.append(head)
                    path1.reverse()

                    path2 = []
                    curr = child
                    while curr != tail:
                        path2.append(curr)
                        curr = tail_parents[curr]
                    path2.append(tail)
                    #path3 = [child]
                    pat = path1 + path2
                    if len(pat) < optimal_cost:
                        optimal_cost = len(pat)
                        path = pat
                        optimal_intersect = child
                head_frontier.append(child)

        curr_tn = tail_frontier.pop()
        num_nodes_expanded += 1
        for child in problem.neighbours[curr_tn]:

            if child not in tail_visited:
                tail_parents[child] = curr_tn
                tail_visited.add(child)
                # if this node is visited by the other side, then we know there is a path
                if child in head_visited:
                    path1 = []
                    curr = head_parents[child]
                    while curr != head:
                        path1.append(curr)
                        curr = head_parents[curr]
                    path1.append(head)
                    path1.reverse()

                    path2 = []
                    curr = child
                    while curr != tail:
                        path2.append(curr)
                        curr = tail_parents[curr]
                    path2.append(tail)
                    #path3 = [child]
                    pat = path1 + path2
                    if len(pat) < optimal_cost:
                        optimal_cost = len(pat)
                        path = pat
                        optimal_intersect = child

                tail_frontier.append(child)

        if optimal_intersect != -1:
            if moretrials == 10:
                break
            moretrials += 1

    # if optimal_intersect != -1:
    #     path1 = problem.trace_path(head_parents[optimal_intersect], head.state)
    #     path2 = problem.trace_path(tail_parents[optimal_intersect], tail.state)
    #     pathtemp = [optimal_intersect]
    #     path2.reverse()
    #     path = path1 + pathtemp + path2
    #print(intersect_costs)
    #print(paths)
    # if len(paths) != 0:
    #     path = paths[0]
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
    path, num_nodes_expanded, max_frontier_size = bidirectional_search(problem)
    correct = problem.check_graph_solution(path)
    print("Solution is correct: {:}".format(correct))
    print(path)

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
    path, num_nodes_expanded, max_frontier_size = bidirectional_search(problem)
    correct = problem.check_graph_solution(path)
    print("Solution is correct: {:}".format(correct))
    print(path)

    # Be sure to compare with breadth_first_search!