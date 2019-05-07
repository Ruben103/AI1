import sys


def max_value(state):
    max = -100000000000

    if state == 1:
        return -1

    for move in range(1, 4):
        if state-move > 0:
            m = min_value(state-move)
            max = m if m > max else max

    return max


def min_value(state):
    min = 10000000000000

    if state == 1:
        return 1

    for move in range(1, 4):
        if state-move > 0:
            m = max_value(state-move)
            min = m if m < min else min

    return min


def minimax_decision(state, turn):
    bestmove = None

    if turn == 1:  # MAX' turn
        max = -100000000000

        for move in range(1, 4):
            m = max_value(state - move)
            if m > max:
                max = m
                bestmove = move

    else:
        min = 10000000000000

        for move in range(1, 4):
            m = min_value(state-move)
            if m < min:
                min = m
                bestmove = move

    return bestmove


def play_nim(state):
    turn = 0

    while state != 1:
        move = minimax_decision(state, turn)
        print(str(state) + ": " + ("MAX" if not turn else "MIN") + " takes " + str(move))

        state -= move
        turn = 1 - turn

    print("1: " + ("MAX" if not turn else "MIN") + " looses")


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
