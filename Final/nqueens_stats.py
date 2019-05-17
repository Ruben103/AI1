def main():
    """
    Replace original main function by this function to perform the program a 
    desired amount of times. The program will return a success rate range from
    0 to 1, where 0 indicates a succes rate of 0%, and 1 indicates a succes rate of 100%.
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

    optimumCounter = 0
    optimum = ((len(board)-1) * len(board)/2)
    print("Optimum: " + str(optimum) + "\n")
    iterations = int(input("How many runs do you want?"))

    for x in range(iterations):
        board = init_board(nqueens)
        if algorithm is 1:
            random_search(board)
        if algorithm is 2:
            board = hill_climbing(board)
        if algorithm is 3:
            board = simulated_annealing(board)
        if algorithm is 4:
            board = genetic_algorithm(board, nqueens)
        conflicts = count_conflicts(board)
        optimumCounter += 1 if not conflicts else 0
        print(optimum - conflicts, end = " ")

    print("\n\nSucces ratio: " + str(optimumCounter/iterations))