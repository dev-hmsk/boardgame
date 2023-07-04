from board.board import *

# Testing

#board_setup()
checkers_board = Checkers_Board()
checkers_board.board_setup()
print(checkers_board.visual)
board_state = checkers_board.get_state()

# print(board_state)
# # check_move()
# print(checkers_board.white_pieces[8].name, checkers_board.white_pieces[8].xy_coord, checkers_board.white_pieces[8].team)
# print(checkers_board.white_pieces[8].check_move())
# print(checkers_board.white_pieces[9].name, checkers_board.white_pieces[9].xy_coord, checkers_board.white_pieces[9].team)
# print(checkers_board.white_pieces[9].check_move())

# print("-" * 20)

# print(checkers_board.black_pieces[8].name,
#       checkers_board.black_pieces[8].xy_coord,
#       checkers_board.black_pieces[8].team)
# print(checkers_board.black_pieces[8].check_valid_move())
# print(checkers_board.black_pieces[9].name, checkers_board.black_pieces[9].xy_coord, checkers_board.black_pieces[9].team)
# print(checkers_board.black_pieces[9].check_valid_move())

# # regular_move()
print(checkers_board.is_regular_move_valid((checkers_board.black_pieces[8])))
print(checkers_board.is_regular_move_valid((checkers_board.white_pieces[8])))
