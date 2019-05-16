import sys
import random

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

    for queen in range(0, len(board)):
        for other_queen in range(queen+1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
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

def simulated_annealing(board):
    """
    Implement this yourself.
    :param board:
    :return:
    """
    pass

""" 
 The following functions perform a genetic algorithm search
"""

def random_select(population):
	""" 
	random_select generates a random probability.
	It then plucks a random member from the population and compares evaluates its 
	fitness. This fitness score is converted to a probability of reproducing.
	If said probability is greater than or equal to the initial random probability,
	this individual will reproduce.
	If not, then another individual is chosen at random and evaluated.
	This is done n times, and if no suitable individual is found, the random probability is reduced.
	"""
	fitness_threshold = random.uniform(0,1)
	while fitness_threshold >= 0:
		n = len(population)
		while n > 0:
			parent = random.choice(population)
			if (evaluate_state(parent) / ((len(parent) - 1) * len(parent) / 2)) >= fitness_threshold:
				return parent
			n -= 1
		fitness_threshold -= 0.01
	return population[0]

def reproduce(parent_one, parent_two):
	"""
	reproduce combines the genome of two individuals by taking a random
	index and splicing together each genome before and after that point. 
	two parents only produce one child, for ease of returning the child.
	"""
	c = random.randint(1, len(parent_one) - 1)
	child = parent_one[:c] + parent_two[c:]
	return child

def mutate(child):
	"""
	mutate randomly selects and alters one chromozome in a genome
	"""
	c = random.randint(0, len(child) - 1)
	child[c] = random.randint(0, len(child) - 1)
	return child

def best_individual(population):
	"""
	best_individual searches through the population and returns the 
	first individual with the highest fitness value, relative to the optimal fitness
	"""
	optimum = (len(population[0]) - 1) * len(population[0]) / 2
	while optimum > 0:
		for individual in population:
			if evaluate_state(individual) == optimum:
				return individual
		optimum -= 1
	return population[0]

def genetic_algorithm(board, nqueens):
	"""
	A population of 10 is randomly generated, 10 pairs of individuals are 
	selected (duplicates possible) psuedo-randomly based on their fitness.
	10 children are created to form a new population. This continues for 100 
	generations, or until a solution is found.
	"""
	population = []
	population.append(board)
	generations = 0
	for d in range(1, 10):
		population.append(init_board(nqueens))
	while generations < 100:
		new_population = []
		for i in range(0, 10):
			parent_one = random_select(population)
			parent_two = random_select(population)
			child = reproduce(parent_one, parent_two)
			mutation = random.random()
			if mutation > 0.97:
				child = mutate(child)
			if evaluate_state(child) == ((len(child) - 1) * len(child) / 2):
				print('\nSolved puzzle in ' + str(generations) + ' generations!')
				board = child.copy()
				return board
			new_population.append(child)
		population = new_population.copy()
		generations += 1
	best = best_individual(population)
	board = best.copy()
	return board



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
    algorithm = input('1: random, 2: hill-climbing, 3: simulated annealing, 4: genetic algorithm \n')

    try:
        algorithm = int(algorithm)

        if algorithm not in range(1, 5):
            raise ValueError

    except ValueError:
        print('Please input a number in the given range!')
        return False

    board = init_board(nqueens)
    print('Initial board: \n')
    print_board(board)

    if algorithm is 1:
        random_search(board)
    if algorithm is 2:
        hill_climbing(board)
    if algorithm is 3:
        simulated_annealing(board)
    if algorithm is 4:
        board = genetic_algorithm(board, nqueens)
    
    numberConflicts = count_conflicts(board)
    print('\nModified board:')
    print_board(board)
    print("Conflicting queens: " + str(numberConflicts) )


# This line is the starting point of the program.
if __name__ == "__main__":
    main()
