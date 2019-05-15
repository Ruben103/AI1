import sys


def negamax_full(state, turn, transTable):
    bestmove = None
    max = -10000000000

    if state == 1:
        return -1, -1

    if transTable[state] != [0,0]:
        return transTable[state]

    for move in range(1, 4):
        if state - move > 0:
            m = -negamax_full(state-move, turn, transTable)[1]
            if m > max:
                max = m
                bestmove = move
    
    transTable[state] = [bestmove, max]
    return bestmove, max               

def play_nim(state):
    turn = 0
    transTable = [[0, 0]] * (state+1)

    while state != 1:
        move = negamax_full(state, turn, transTable)[0]
        print(str(state) + ": " + ("MAX" if not turn else "MIN") + " takes " + str(move))

        state -= move
        turn = 1 - turn

    print("1: " + ("MAX" if not turn else "MIN") + " looses")
#    for i, s in enumerate(transTable):
#        winning = "winning" if s[1] == 1 else "losing"
#        print(f"{i} straws. Take {s[0]}. you are {winning}")


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
