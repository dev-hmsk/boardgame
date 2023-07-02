from board.board import *

# Testing
checkers_board = Checkers_Board()
checkers_board.board_setup()
print(checkers_board.visual)
board_state = checkers_board.get_state()
print(checkers_board.black_pieces[9].xy_coord)
print(checkers_board.black_pieces[9].check_move())