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