from board.board import Board

# Testing

test_dim = (5, 5)
board_1 = Board(test_dim)
test_item1 = "test_obj_1"
test_item2 = "test_obj_2"
test_move1 = (1,1)
test_move2 = (1,2)

print(board_1.visual)
board_1.move(test_move1, test_item1)

board_1.move(test_move2, test_item2)
board_1.move((3,3),"hewo")
print(board_1.visual)
board_1.move((4,4),"uwu")
board_1.move((4,4),"whats")
board_1.move((1,2),"this")
print(board_1.visual)

board_1.clear_board()
print(board_1.visual)
