import sys

def negamax_full(state, transTable):
    bestmove = None
    max = -10000000000

    if state == 1:
        transTable[state] = [1, -1]
        return 1, -1

    # Transposition Table: If state is evaluated before, return those results.
    if transTable[state] != [0,0]:
        return transTable[state]

    for move in range(1, 4):
        if state - move > 0:
            m = -negamax_full(state-move, transTable)[1] # Switch to other player
            if m > max:
                max = m
                bestmove = move
    
    # Add results to transposition table
    transTable[state] = [bestmove, max]
    return bestmove, max               

def play_nim(state):
    turn = 0
    transTable = [[0, 0]] * (state+1) # [bestmove, eval]

    while state != 1:
        move, eval = negamax_full(state, transTable) # Turn not necessary for Negamax
        print(str(state) + ": " + ("MAX" if not turn else "MIN") + " takes " + str(move))
        state -= move
        turn = 1 - turn

    print("1: " + ("MAX" if not turn else "MIN") + " loses")
    


def main():
    """
    Main function that will parse input and call the appropriate algorithm. You do not need to understand everything
    here!
    """

    try:
        if len(sys.argv) is not 2:
            raise ValueError

        state = int(sys.argv[1])
        if state < 1 or state > 100:
            raise ValueError

        play_nim(state)

    except ValueError:
        print('Usage: python nim.py NUMBER')
        return False


if __name__ == '__main__':
    main()
