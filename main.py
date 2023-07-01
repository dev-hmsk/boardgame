from board.board import Board, Checkers

# Testing

checkers_board = Checkers()

print(checkers_board.visual)

# for pieces in checkers_board.white_pieces:
#     print(pieces.name)
#     print(pieces.xy_coor)

# for pieces in checkers_board.black_pieces:
#     print(type(pieces))
#     print(type(pieces.name))
#     print(pieces.xy_coor)
print(type((checkers_board.black_pieces[1])))
print(checkers_board.black_pieces[1].name)
# print(type(checkers_board.white_pieces))

print(checkers_board.board_setup())
print(checkers_board.visual)

piece_at_1_1 = (checkers_board.get_from_location((1,1)))
piece_at_8_8 = (checkers_board.get_from_location((8,8)))
print(piece_at_8_8.name)
print(piece_at_8_8.xy_coor)