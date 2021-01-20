import sys
from board import Board

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Expecting one input string for the sodoku board")
        exit(-1)

    board_str = ''.join([s for s in sys.argv[1] if s.isdigit()])
    if len(board_str) != 81:
        print("Invalid starting board (expected 81 digits, but got %d digits instead)" % len(board_str))
        exit(-1)
    board = Board(board_str=board_str)
    sols = board.solve_board()
    print("%d solutions found" % len(sols))
    for idx, sol in enumerate(sols):
        print("\nSolution #%d\n" % (idx+1))
        sol.display_board()
