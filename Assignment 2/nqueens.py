import sys
import random
import math

MAXQ = 100


def in_conflict(column, row, other_column, other_row):
    """
    Checks if two locations are in conflict with each other.
    :param column: Column of queen 1.
    :param row: Row of queen 1.
    :param other_column: Column of queen 2.
    :param other_row: Row of queen 2.
    :return: True if the queens are in conflict, else False.
    """
    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


def in_conflict_with_another_queen(row, column, board):
    """
    Checks if the given row and column correspond to a queen that is in conflict with another queen.
    :param row: Row of the queen to be checked.
    :param column: Column of the queen to be checked.
    :param board: Board with all the queens.
    :return: True if the queen is in conflict, else False.
    """
    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True
    return False


def count_conflicts(board):
    """
    Counts the number of queens in conflict with each other.
    :param board: The board with all the queens on it.
    :return: The number of conflicts.
    """
    cnt = 0

    for column in range(0, len(board)):
        for other in range(column, len(board)):
            if in_conflict(column, board[column], other, board[other]):
                cnt += 1

    return cnt


def evaluate_state(board):
    """
    Evaluation function. The maximal number of queens in conflict can be 1 + 2 + 3 + 4 + .. +
    (nquees-1) = (nqueens-1)*nqueens/2. Since we want to do ascending local searches, the evaluation function returns
    (nqueens-1)*nqueens/2 - countConflicts().
    :param board: list/array representation of columns and the row of the queen on that column
    :return: evaluation score
    """
    return (len(board)-1)*len(board)/2 - count_conflicts(board)


def print_board(board):
    """
    Prints the board in a human readable format in the terminal.
    :param board: The board with all the queens.
    """
    print("\n")

    for row in range(len(board)):
        line = ''
        for column in range(len(board)):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(row, column, board) else 'q'
            else:
                line += '.'
        print(line)


def init_board(nqueens):
    """
    :param nqueens integer for the number of queens on the board
    :returns list/array representation of columns and the row of the queen on that column
    """

    board = []

    for column in range(nqueens):
        board.append(random.randint(0, nqueens-1))

    return board


"""
------------------ Do not change the code above! ------------------
"""

def random_search(board):
    """
    This function is an example and not an efficient solution to the nqueens problem. What it essentially does is flip
    over the board and put all the queens on a random position.
    :param board: list/array representation of columns and the row of the queen on that column
    """

    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break

        for column, row in enumerate(board):  # For each column, place the queen in a random row
            board[column] = random.randint(0, len(board)-1)

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    print('Final state is:')
    print_board(board)

def sidestepping(board):
    returnBoard = board.copy()
    nqueens = len(returnBoard)
    for column in returnBoard:
        rand = random.uniform(0,1)
        multiplier = 0
        if returnBoard[column] > 0 and returnBoard[column] < nqueens-1:
            bothWays = True
        else:
            bothWays = False
        if not bothWays:
            if returnBoard[column] == 0:
                multiplier = 1
            else:
                multiplier = -1
            returnBoard[column] += multiplier
            continue
        if rand < 0.45: #go down
            returnBoard[column] += 1
        if rand > 0.55:
            returnBoard[column] -= 1
    return returnBoard

def hill_climbing(board):
    """
    Algorithm:
        Additional while loop implemented such that the algorithm keeps searching for bette solutions using
        sidestepping() until there is no improvement found n-times (improvementCounter).
        We can modify this counter to have it search more or fewer times.
    """
    improvementCounter = 3
    boardCopy = board.copy()

    while improvementCounter != 0:
        for column in range(len(board)):
            minHeuristic = count_conflicts(board)
            for row in range(len(board)): 
                #iterate over the rows for each column
                boardCopy[column] = row
                currentHeuristic = count_conflicts(boardCopy)
                if currentHeuristic < minHeuristic:
                    minHeuristic = currentHeuristic
                    board[column] = row

        boardCopy = sidestepping(boardCopy)
        prelConflicts = count_conflicts(boardCopy)
        if prelConflicts < minHeuristic:
            board = boardCopy.copy()
            minHeuristic = prelConflicts
            improvementCounter = 3
        else:
            improvementCounter -= 1

    return count_conflicts(board)

    while improvementCounter != 0:
        for column in range(len(board)):
            minHeuristic = count_conflicts(board)
            for row in range(len(board)): 
                #iterate over the rows for each column
                boardCopy[column] = row
                currentHeuristic = count_conflicts(boardCopy)
                if currentHeuristic < minHeuristic:
                    minHeuristic = currentHeuristic
                    board[column] = row

        boardCopy = sidestepping(boardCopy)
        prelConflicts = count_conflicts(boardCopy)
        if prelConflicts < minHeuristic:
            board = boardCopy.copy()
            minHeuristic = prelConflicts
            improvementCounter = 3
        else:
            improvementCounter -= 1

    return count_conflicts(board)

def randomWalk(board):
	rand1 = random.randint(1, len(board) - 1)
	rand2 = random.randint(0, len(board) - 1)
	board[rand1] = rand2
	return board

def probDistribution(T, E):
    """
    This distribution is a variation of the Fermi Dirac equation used in physics.
    The nice aspect of it, is that for high values of T, the probability is high (which we want)
    While for low values of T, the probability low.
    We adapted the while loop such that we decrement T instead of incrementing (like the assignment said)
    The property that we want to decrease the probability of accepting a random walk as time increases
    is still preserved.
    """
    p = 1/(math.exp(E/T) + 1) * 2
    return p

def simulated_annealing(board):
    """
    Implement this yourself.
    :param board:
    :return:
    """
    T = 20
    stopCriterium = False
    state = evaluate_state(board)
    iteration = 1
    while not stopCriterium:
        T -= 1
        iteration += 1
        print("\nIteration " + str(iteration))
        if T <= 0.05:
            return state
        nextBoard = randomWalk(board.copy())
        print("random walk: ")
        print_board(nextBoard)
        print("board: ")
        print_board(board)
        nextState = evaluate_state(nextBoard)
        E = nextState - state
        print("difference " + str(E))
        if E > 0:
            # This means the next State is better:
            state = nextState
            board = nextBoard
            
        else:
            rand = random.uniform(0,1)
            p = probDistribution(T, E)
            print("Probability: " + str(p) + " \nrandom number: " + str(rand) + "\n")
            if p > rand:
                board = nextBoard
                state = nextState
            

def main():
    """
    Main function that will parse input and call the appropriate algorithm. You do not need to understand everything
    here!
    """

    try:
        if len(sys.argv) is not 2:
            raise ValueError

        nqueens = int(sys.argv[1])
        if nqueens < 1 or nqueens > MAXQ:
            raise ValueError

    except ValueError:
        print('Usage: python nqueens.py NUMBER')
        return False

    print('Which algorithm to use?')
    algorithm = input('1: random, 2: hill-climbing, 3: simulated annealing \n')

    try:
        algorithm = int(algorithm)

        if algorithm not in range(1, 4):
            raise ValueError

    except ValueError:
        print('Please input a number in the given range!')
        return False

    board = init_board(nqueens)
    print('Initial board: \n')
    print_board(board)
    print("Conflicting queens: " + str(count_conflicts(board)))

    if algorithm is 1:
        random_search(board)
    if algorithm is 2:
        hill_climbing(board)
    if algorithm is 3:
        simulated_annealing(board)
    
    numberConflicts = evaluate_state(board)
    print('Modified board:')
    print_board(board)
    print("Evaluate state: " + str(numberConflicts) )


# This line is the starting point of the program.
if __name__ == "__main__":
    main()