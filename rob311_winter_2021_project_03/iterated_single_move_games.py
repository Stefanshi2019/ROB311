from abc import ABC, abstractmethod
import numpy as np


class SingleMoveGamePlayer(ABC):
    """
    Abstract base class for a symmetric, zero-sum single move game player.
    """
    def __init__(self, game_matrix: np.ndarray):
        self.game_matrix = game_matrix
        self.n_moves = game_matrix.shape[0]
        super().__init__()

    @abstractmethod
    def make_move(self) -> int:
        pass


class IteratedGamePlayer(SingleMoveGamePlayer):
    """
    Abstract base class for a player of an iterated symmetric, zero-sum single move game.
    """
    def __init__(self, game_matrix: np.ndarray):
        super(IteratedGamePlayer, self).__init__(game_matrix)

    @abstractmethod
    def make_move(self) -> int:
        pass

    @abstractmethod
    def update_results(self, my_move, other_move):
        """
        This method is called after each round is played
        :param my_move: the move this agent played in the round that just finished
        :param other_move:
        :return:
        """
        pass

    @abstractmethod
    def reset(self):
        """
        This method is called in between opponents (forget memory, etc.)
        :return:
        """
        pass


class UniformPlayer(IteratedGamePlayer):
    def __init__(self, game_matrix: np.ndarray):
        super(UniformPlayer, self).__init__(game_matrix)

    def make_move(self) -> int:
        """

        :return:
        """
        return np.random.randint(0, self.n_moves)

    def update_results(self, my_move, other_move):
        """
        The UniformPlayer player does not use prior rounds' results during iterated games.
        :param my_move:
        :param other_move:
        :return:
        """
        pass

    def reset(self):
        """
        This method is called in between opponents (forget memory, etc.)
        :return:
        """
        pass


class FirstMovePlayer(IteratedGamePlayer):
    def __init__(self, game_matrix: np.ndarray):
        super(FirstMovePlayer, self).__init__(game_matrix)

    def make_move(self) -> int:
        """
        Always chooses the first move
        :return:
        """
        return 0

    def update_results(self, my_move, other_move):
        """
        The FirstMovePlayer player does not use prior rounds' results during iterated games.
        :param my_move:
        :param other_move:
        :return:
        """
        pass

    def reset(self):
        """
        This method is called in between opponents (forget memory, etc.)
        :return:
        """
        pass


class CopycatPlayer(IteratedGamePlayer):
    def __init__(self, game_matrix: np.ndarray):
        super(CopycatPlayer, self).__init__(game_matrix)
        self.last_move = np.random.randint(self.n_moves)

    def make_move(self) -> int:
        """
        Always copies the last move played
        :return:
        """
        return self.last_move

    def update_results(self, my_move, other_move):
        """
        The CopyCat player simply remembers the opponent's last move.
        :param my_move:
        :param other_move:
        :return:
        """
        self.last_move = other_move

    def reset(self):
        """
        This method is called in between opponents (forget memory, etc.)
        :return:
        """
        self.last_move = np.random.randint(self.n_moves)


def play_game(player1, player2, game_matrix: np.ndarray, N: int = 1000) -> (int, int):
    """

    :param player1: instance of an IteratedGamePlayer subclass for player 1
    :param player2: instance of an IteratedGamePlayer subclass for player 2
    :param game_matrix: square payoff matrix
    :param N: number of rounds of the game to be played
    :return: tuple containing player1's score and player2's score
    """
    p1_score = 0.0
    p2_score = 0.0
    n_moves = game_matrix.shape[0]
    legal_moves = set(range(n_moves))
    for idx in range(N):
        move1 = player1.make_move()
        move2 = player2.make_move()
        if move1 not in legal_moves:
            print("WARNING: Player1 made an illegal move: {:}".format(move1))
            if move2 not in legal_moves:
                print("WARNING: Player2 made an illegal move: {:}".format(move2))
            else:
                p2_score += np.max(game_matrix)
                p1_score -= np.max(game_matrix)
            continue
        elif move2 not in legal_moves:
            print("WARNING: Player2 made an illegal move: {:}".format(move2))
            p1_score += np.max(game_matrix)
            p2_score -= np.max(game_matrix)
            continue
        player1.update_results(move1, move2)
        player2.update_results(move2, move1)

        p1_score += game_matrix[move1, move2]
        p2_score += game_matrix[move2, move1]

    return p1_score, p2_score


class StudentAgent(IteratedGamePlayer):
    """
    The agent uses a combination of Q-learning and Nash equilibrium strategy.

    Q-learning is a model-free reinforcement learning algorithm for Markov decision processes.
    It works by finding an optimal policy that maximizes the total reward over successive processes.
    Given current state, it identifies the optimal action to be taken.
    The Q learning takes the following form:
        Q(s, a) = Q_-1(s, a) + alpha * (Reward(s, a) + gamma * max Q(s',a') - Q_-1(s, a)
    where s and a denote past state and action taken, s' denotes current state, and a' is the next action.
    Since the reward functions are well-known and deterministic, we set gamma = 0.1, forcing the agent to
    mostly value immediate rewards. Since we are playing for a thousand games against each opponent, we expect
    there are enough samples for the model to learn, we choose alpha = 0.1. Although, through testing, alpha =
    0.1, 0.5, 0.9 do not make much difference in win rate.

    Before Q-learning learns from enough samples and becomes effective, we will use Nash equilibrium strategy.
    We calculate the equilibrium by the fraction of positive reward to the sum of all 3 positive rewards.
    For example, the equilibrium for decision 0 / Rock is p(0) = b/(a+b+c), where a,b, and c are the rewards from
    the game matrix. Then a random value between 0 and 1 is drawn and an action is taken depending on what
    range it falls into. For example if random value p(0) < rdval < p(0) + p(1), action 1 is taken.



    """
    def __init__(self, game_matrix: np.ndarray):
        """
        Initialize your game playing agent. here
        :param game_matrix: square payoff matrix for the game being played.
        """
        super(StudentAgent, self).__init__(game_matrix)
        self.a = self.game_matrix[1][0]
        self.b = self.game_matrix[0][2]
        self.c = self.game_matrix[2][1]
        self.Erock = self.b / (self.a + self.b + self.c)
        self.Epaper = self.a / (self.a + self.b + self.c)

        self.Q = np.ones((9, 3))
        self.prev_state = 0
        self.alpha = 0.1
        self.gamma = 0.1
        self.turns = 0
        # YOUR CODE GOES HERE
        pass

    def make_move(self) -> int:
        """
        Play your move based on previous moves or whatever reasoning you want.
        :return: an int in (0, ..., n_moves-1) representing your move
        """
        # YOUR CODE GOES HERE
        move = 0

        if self.turns < 50:
            x = np.random.rand()
            if x <self.Erock:
                return 0
            elif x < (self.Epaper + self.Erock):
                return 1
            else:
                return 2
        else:
            move = int(np.argmax(self.Q[self.prev_state, :]))
        return move

    def update_results(self, my_move, other_move):
        """
        Update your agent based on the round that was just played.
        :param my_move:
        :param other_move:
        :return: nothing
        """
        # YOUR CODE GOES HERE
        self.a = self.game_matrix[1][0]
        self.b = self.game_matrix[0][2]
        self.c = self.game_matrix[2][1]
        self.Erock = self.b / (self.a + self.b + self.c)
        self.Epaper = self.a / (self.a + self.b + self.c)

        cur_state = 3 * my_move + other_move
        reward = self.game_matrix[my_move][other_move]
        if self.turns > 1:
            self.Q[self.prev_state, my_move] = self.Q[self.prev_state, my_move] + \
                                               self.alpha * (reward + self.gamma * np.max(self.Q[cur_state]) - self.Q[self.prev_state, my_move])
        self.prev_state = cur_state
        self.turns += 1


    def reset(self):
        """
        This method is called in between opponents (forget memory, etc.).
        :return: nothing
        """
        # YOUR CODE GOES HERE
        self.Q = np.ones((9, 3))
        self.prev_state = 0
        self.alpha = 0.1
        self.gamma = 0
        self.turns = 0


if __name__ == '__main__':
    """
    Simple test on standard rock-paper-scissors
    The game matrix's row (first index) is indexed by player 1 (P1)'s move (i.e., your move)
    The game matrix's column (second index) is indexed by player 2 (P2)'s move (i.e., the opponent's move)
    Thus, for example, game_matrix[0, 1] represents the score for P1 when P1 plays rock and P2 plays paper: -1.0 
    because rock loses to paper.
    """
    game_matrix = np.array([[0.0, -2.0, 1.0],
                            [2.0, 0.0, -5.0],
                            [-1.0, 5.0, 0.0]])
    # uniform_player = UniformPlayer(game_matrix)
    first_move_player = FirstMovePlayer(game_matrix)
    uniform_player = UniformPlayer(game_matrix)
    student_player = StudentAgent(game_matrix)



    # Now try your agent

    student_score, first_move_score = play_game(student_player, first_move_player, game_matrix)

    print("Your player's score: {:}".format(student_score))
    print("First-move player's score: {:}".format(first_move_score))