from board.board import Board

# Testing

test_dim = (5, 5)
board_1 = Board(test_dim)
test_item1 = "test_obj_1"
test_item2 = "test_obj_2"
test_move1 = "x1y1"
test_move2 = "x1y2"


print(board_1.move(test_move1, test_item1))
print(board_1.get_state())

print(board_1.move(test_move1, test_item1))
print(board_1.get_state())

print(board_1.remove(test_move1))
print(board_1.get_state())