def hill_climbing(board):
    """
    Algorithm:
        For each column; check which position in that row minimizes the heuristic function of having 
        the least conflicts. Move the queen to that position in the column.
        Go to next column
    """
    
    for column in range(len(board)):
        boardCopy = board.copy()
        minHeuristic = count_conflicts(board)
        for row in range(len(board)): 
            #iterate over the rows for each column
            boardCopy[column] = row
            currentHeuristic = count_conflicts(boardCopy)
            if currentHeuristic < minHeuristic:
                board[column] = row
