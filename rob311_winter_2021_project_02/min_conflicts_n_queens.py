import numpy as np
### WARNING: DO NOT CHANGE THE NAME OF THIS FILE, ITS FUNCTION SIGNATURE OR IMPORT STATEMENTS


def min_conflicts_n_queens(initialization: list) -> (list, int):
    """
    Solve the N-queens problem with no conflicts (i.e. each row, column, and diagonal contains at most 1 queen).
    Given an initialization for the N-queens problem, which may contain conflicts, this function uses the min-conflicts
    heuristic(see AIMA, pg. 221) to produce a conflict-free solution.

    Be sure to break 'ties' (in terms of minimial conflicts produced by a placement in a row) randomly.
    You should have a hard limit of 1000 steps, as your algorithm should be able to find a solution in far fewer (this
    is assuming you implemented initialize_greedy_n_queens.py correctly).

    Return the solution and the number of steps taken as a tuple. You will only be graded on the solution, but the
    number of steps is useful for your debugging and learning. If this algorithm and your initialization algorithm are
    implemented correctly, you should only take an average of 50 steps for values of N up to 1e6.

    As usual, do not change the import statements at the top of the file. You may import your initialize_greedy_n_queens
    function for testing on your machine, but it will be removed on the autograder (our test script will import both of
    your functions).

    On failure to find a solution after 1000 steps, return the tuple ([], -1).

    :param initialization: numpy array of shape (N,) where the i-th entry is the row of the queen in the ith column (may
                           contain conflicts)

    :return: solution - numpy array of shape (N,) containing a-conflict free assignment of queens (i-th entry represents
    the row of the i-th column, indexed from 0 to N-1)
             num_steps - number of steps (i.e. reassignment of 1 queen's position) required to find the solution.
    """

    N = len(initialization)
    num_steps = 0
    max_steps = 1000

    ### YOUR CODE GOES HERE
    board_conflict = np.zeros((N, N), dtype = int)
    board = initialization
    # update board conflict for initialization
    for i in range(len(board)):
        update_board(i, board[i], board_conflict, True)

    # go for max max_steps
    for idx in range(max_steps):
        # if problem is solved, return
        if problem_solved(board_conflict, board):
            return board, idx
        else:
            # otherwise randomly choose a conflicted col
            conflicted_col = np.random.randint(0, len(board))
            while has_conflict(conflicted_col, board_conflict, board) == False:
                conflicted_col = np.random.randint(0, len(board))

            # find the coordinate of the conflicted queen
            conflicted_row = board[conflicted_col]
            new_col = conflicted_col
            # pick it up
            new_row = reduce(conflicted_col, conflicted_row, board_conflict)
            # and place it down
            board[new_col] = new_row
            update_board(new_col, new_row, board_conflict, True)
            num_steps += 1

    return [], -1


def reduce(col, row, board_conflict):

    # subtract the conflicts caused by this coordinate for now
    update_board(col, row, board_conflict, False)
    min_conflict_rows = []
    min_conflict = float('inf')
    # find the best rows to place again
    for row in range(len(board_conflict[col])):
        if board_conflict[col][row] < min_conflict:
            min_conflict_rows.clear()
            min_conflict_rows.append(row)
            min_conflict = board_conflict[col][row]
        elif board_conflict[col][row] == min_conflict:
            min_conflict_rows.append(row)

    # return a random row from the min conflict rows
    return min_conflict_rows[np.random.randint(0, len(min_conflict_rows))]


def print_board(greedy_init):
    # print the current board
    board = np.zeros((len(greedy_init), len(greedy_init)), dtype=int)
    for i in range(len(greedy_init)):
        board[i, greedy_init[i]] = 1
    print("current board: \n", np.array(board).T)


def has_conflict(col:int, board_conflict, board):
    # check if current queen is conflicting, returns true if it does, false otherwise
    # if it is conflicting, the conflict value that its location must be greater than 1
    if board_conflict[col, board[col]] != 1:
        return True
    else:
        return False


def update_board( col, row, board_conflict, inc: bool):
    # increment board_conflict by 1 or -1, depending on inc, on all directions from current coordinate
    N = len(board_conflict)
    val = None
    if inc:
        val = 1
    else:
        val = -1

    # update row by fixing col
    for i in range(N):
        board_conflict[col][i] += val
    for i in range(N):
        board_conflict[i][row] += val

    cur_col = col
    cur_row = row
    while(cur_col >= 0 and cur_col < N and cur_row >= 0 and cur_row < N ):
        board_conflict[cur_col][cur_row] += val
        cur_col += 1
        cur_row += 1

    cur_col = col
    cur_row = row
    while(cur_col >= 0 and cur_col < N and cur_row >= 0 and cur_row < N ):
        board_conflict[cur_col][cur_row] += val
        cur_col += 1
        cur_row += -1

    cur_col = col
    cur_row = row
    while(cur_col >= 0 and cur_col < N and cur_row >= 0 and cur_row < N ):
        board_conflict[cur_col][cur_row] += val
        cur_col += -1
        cur_row += 1

    cur_col = col
    cur_row = row
    while(cur_col >= 0 and cur_col < N and cur_row >= 0 and cur_row < N ):
        board_conflict[cur_col][cur_row] += val
        cur_col += -1
        cur_row += -1

    if inc:
        board_conflict[col][row] -= 5
    else:
        board_conflict[col][row] += 5

    return 0


def problem_solved(board_conflict, board):
    # if all queens have conflicting value = 1, problem is solved
    for col in range(len(board)):
        if board_conflict[col][board[col]] != 1:
            print( col, board[col], " is problematic")
            return False
    print("problem is solved")
    return True


if __name__ == '__main__':
    # Test your code here!
    from initialize_greedy_n_queens import initialize_greedy_n_queens
    from support import plot_n_queens_solution

    N = 1003
    # Use this after implementing initialize_greedy_n_queens.py
    assignment_initial = initialize_greedy_n_queens(N)
    # Plot the initial greedy assignment
    plot_n_queens_solution(assignment_initial)

    assignment_solved, n_steps = min_conflicts_n_queens(assignment_initial)
    # Plot the solution produced by your algorithm
    plot_n_queens_solution(assignment_solved)
