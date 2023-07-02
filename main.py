from board.board import *

# Testing
checkers_board = Checkers()
checkers_board.board_setup()
print(checkers_board.visual)
print(checkers_board.black_pieces[0].name, checkers_board.black_pieces[0].xy_coord)
remove1 = checkers_board.remove_from_location((1,1))
print(remove1[1].name,remove1[1].xy_coord)
print(checkers_board.visual)
board_state = checkers_board.get_state()
checkers_board.clear_board()
board_state = checkers_board.get_state()