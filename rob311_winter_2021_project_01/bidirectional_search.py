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

    #head = Node(problem.init_state, problem.init_state, (problem.init_state,problem.init_state), 0)
    #tail = Node(problem.goal_states[0], problem.goal_states[0], (problem.goal_states[0],problem.goal_states[0]), 0)
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

    # initial conditions for vars
    head_parents[head] = head
    tail_parents[tail] = tail
    head_visited.add(head)
    tail_visited.add(tail)
    head_frontier.append(head)
    tail_frontier.append(tail)

    # front size tracks the cost from head or tail to current node
    head_front_size = dict()
    tail_front_size = dict()
    head_front_size[head] = 0
    tail_front_size[tail] = 0

    # keep traversing unexplored nodes
    while len(head_frontier) != 0 and len(tail_frontier) != 0:
        # pop two nodes from head frontier and tail frontier as current nodes
        curr_hn = head_frontier.pop()
        num_nodes_expanded += 1
        curr_tn = tail_frontier.pop()
        num_nodes_expanded += 1

        # if the current node is visited by the other side, then we know this is a intersection
        if curr_hn in tail_visited:
            # traverse all existing intersections and return intersection that results in optimal path,
            # as well as the total number of paths found
            optimal_state, path_found = check_intersect(head_visited, tail_visited, head_front_size, tail_front_size)
            if optimal_state != -1:
                # trace the optimal path
                path = trace_path(optimal_state, head_parents, tail_parents, head, tail)
            # stop if 1000 intersections are found, otherwise the function goes time out
            if path_found > 1000:
                break
            continue
        # if the current node is visited by the other side, then we know this is a intersection
        if curr_tn in head_visited:
            # traverse all existing intersections and return intersection that results in optimal path,
            # as well as the total number of paths found
            optimal_state, path_found= check_intersect(head_visited, tail_visited, head_front_size, tail_front_size)
            if optimal_state != -1:
                # trace the optimal path
                path = trace_path(optimal_state, head_parents, tail_parents, head, tail)
            # stop if 1000 intersections are found, otherwise the function goes time out
            if path_found > 1000:
                break
            continue

        # do bfs once from head side
        for child in problem.neighbours[curr_hn]:
            if child not in head_visited:
                head_parents[child] = curr_hn
                head_visited.add(child)
                head_frontier.append(child)
                head_front_size[child] = head_front_size[curr_hn] + 1

        # do bfs once from tail side
        for child in problem.neighbours[curr_tn]:
            if child not in tail_visited:
                tail_parents[child] = curr_tn
                tail_visited.add(child)
                tail_frontier.append(child)
                tail_front_size[child] = tail_front_size[curr_tn] + 1

    return path, num_nodes_expanded, max_frontier_size


# find all existing intersections, and tracks the total costs for paths going through each intersection
def check_intersect(head_visited, tail_visited, head_front_size, tail_front_size):
    dict_intersects = {}
    optimal_cost = float('inf')
    optimal_intersect = -1
    path_found = 0
    for state in head_visited:
        if state in tail_visited:
            cost = head_front_size[state] + tail_front_size[state]
            dict_intersects[state] = cost
            path_found += 1
            # keep track of the intersection that results in optimal costs
            if cost < optimal_cost:
                optimal_cost = cost
                optimal_intersect = state

    return optimal_intersect, path_found


# trace path with given head, tail, and intersection
def trace_path(intersect, head_parents, tail_parents, head, tail):
    path1 = []
    curr = head_parents[intersect]
    while curr != head:
        path1.append(curr)
        curr = head_parents[curr]
    path1.append(head)
    path1.reverse()

    path2 = []
    curr = intersect
    while curr != tail:
        path2.append(curr)
        curr = tail_parents[curr]
    path2.append(tail)
    # path3 = [child]
    pat = path1 + path2
    return pat


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

    #Use stanford_large_network_facebook_combined.txt to make your own test instances
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