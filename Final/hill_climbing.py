def hill_climbing(board):
    """
    Algorithm:
        Additional while loop implemented such that the algorithm keeps searching for bette solutions using
        sidestepping() until there is no improvement found n-times (improvementCounter).
        We can modify this counter to have it search more or fewer times.
    """
    improvementCounter = 3
    while improvementCounter != 0:
        for column in range(len(board)):
            bestRow = board[column]
            currentState = evaluate_state(board)
            for row in range(len(board)): 
                #iterate over the rows for each column
                board[column] = row
                nextState = evaluate_state(board)
                if nextState > currentState:
                    currentState = nextState
                    bestRow = row

            board[column] = bestRow
            boardCopy = sidestepping(board)
            nextState = evaluate_state(boardCopy)

        if nextState > currentState:
            board = boardCopy.copy()
            currentState = nextState
            improvementCounter = 3
        else:
            improvementCounter -= 1

    return board