from board import Board

if __name__ == '__main__':
    board_str = '000807002050036000100500000017000603060000040302000910000002005000750090400901000'
    board = Board(board_str=board_str)
    sols = board.solve_board()
    for sol in sols:
        sol.display_board()