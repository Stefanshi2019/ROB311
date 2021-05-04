import numpy as np


### WARNING: DO NOT CHANGE THE NAME OF THIS FILE, ITS FUNCTION SIGNATURE OR IMPORT STATEMENTS


def initialize_greedy_n_queens(N: int) -> list:
    """
    This function takes an integer N and produces an initial assignment that greedily (in terms of minimizing conflicts)
    assigns the row for each successive column. Note that if placing the i-th column's queen in multiple row positions j
    produces the same minimal number of conflicts, then you must break the tie RANDOMLY! This strongly affects the
    algorithm's performance!

    Example:
    Input N = 4 might produce greedy_init = np.array([0, 3, 1, 2]), which represents the following "chessboard":

     _ _ _ _
    |Q|_|_|_|
    |_|_|Q|_|
    |_|_|_|Q|
    |_|Q|_|_|

    which has one diagonal conflict between its two rightmost columns.

    You many only use numpy, which is imported as np, for this question. Access all functions needed via this name (np)
    as any additional import statements will be removed by the autograder.

    :param N: integer representing the size of the NxN chessboard
    :return: numpy array of shape (N,) containing an initial solution using greedy min-conflicts (this may contain
    conflicts). The i-th entry's value j represents the row  given as 0 <= j < N.
    """

    # tracks the conflict value of each location on the chess board
    board_conflict = np.zeros((N, N), dtype=int)
    greedy_init = np.zeros(N, dtype=int)
    # First queen goes in a random spot
    rand = np.random.randint(0, N)
    greedy_init[0] = rand
    update_board(board_conflict, [0, greedy_init[0]], N)
    # start with col 1
    for col in range(1, N):
        # find the rows with minimum conflict to place
        cost = float('inf')
        mincost_list = []
        for row in range(N):
            if board_conflict[col][row] < cost:
                mincost_list.clear()
                mincost_list.append(row)
                cost = board_conflict[col][row]
            elif board_conflict[col][row] == cost:
                mincost_list.append(row)
        # randomly select a row from rows of minimum cost
        best_row = mincost_list[np.random.randint(0, len(mincost_list))]
        # update board
        greedy_init[col] = int(best_row)
        # update board_conflict
        update_board(board_conflict, [col, best_row], N)


    return greedy_init


def update_board(board_conflict, coord: list, N: int):
    # increment board_conflict by 1 on all directions from current coordinate
    col = coord[0]
    row = coord[1]
    for i in range(N):
        board_conflict[col][i] += 1
    for i in range(N):
        board_conflict[i][row] += 1

    cur_col = col
    cur_row = row
    while (cur_col >= 0 and cur_col < N and cur_row >= 0 and cur_row < N):
        board_conflict[cur_col][cur_row] += 1
        cur_col += 1
        cur_row += 1

    cur_col = col
    cur_row = row
    while (cur_col >= 0 and cur_col < N and cur_row >= 0 and cur_row < N):
        board_conflict[cur_col][cur_row] += 1
        cur_col += 1
        cur_row += -1

    cur_col = col
    cur_row = row
    while (cur_col >= 0 and cur_col < N and cur_row >= 0 and cur_row < N):
        board_conflict[cur_col][cur_row] += 1
        cur_col += -1
        cur_row += 1

    cur_col = col
    cur_row = row
    while (cur_col >= 0 and cur_col < N and cur_row >= 0 and cur_row < N):
        board_conflict[cur_col][cur_row] += 1
        cur_col += -1
        cur_row += -1

    board_conflict[col][row] -= 5

    return 0


def print_board(greedy_init):
    # print the current board
    board = np.zeros((len(greedy_init), len(greedy_init)), dtype=int)
    for i in range(len(greedy_init)):
        board[i, greedy_init[i]] = 1
    print("current board: \n", np.array(board).T)


if __name__ == '__main__':
    # You can test your code here
    # pass

    init = initialize_greedy_n_queens(9)
