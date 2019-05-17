def sidestepping(board):
    returnBoard = board.copy()
    nqueens = len(returnBoard)
    for column in returnBoard:
        rand = random.uniform(0,1)
        bothWays = True if 0 < returnBoard[column] < nqueens-1 else False
        if not bothWays:
            returnBoard[column] += -1 if returnBoard[column] else 1
            continue
        returnBoard[column] += 1 if rand < 0.5 else -1
    return returnBoard