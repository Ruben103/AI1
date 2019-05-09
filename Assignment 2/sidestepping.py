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