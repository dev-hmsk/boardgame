from board.board import *


# Testing

#board_setup()
checkers_board = Checkers_Board()
checkers_board.board_setup()
# print(checkers_board.visual)
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
# print(checkers_board.is_regular_move_valid((checkers_board.black_pieces[8])))
# print(checkers_board.is_regular_move_valid((checkers_board.white_pieces[8])))
valid_white_moves = checkers_board.is_regular_move_valid((checkers_board.white_pieces[8]))

valid_black_moves = checkers_board.is_regular_move_valid((checkers_board.black_pieces[8]))

def show_valid_moves(valid_moves):
    show_choices = []
    for name, value in valid_moves.items():
        if value:
            show_choices.append(name)
    return show_choices

def make_valid_move(valid_moves):
    player_options = show_valid_moves(valid_moves)
    print(f"Here are your valid moves: {player_options}")
    user_input = input("Make a choice: ")
    if user_input in valid_moves:
        print(f"You choice was to move to {user_input}")
        # Put move piece logic here
    else:
        print("Invalid Move. Try Again")
        make_valid_move(valid_moves)

user_move_input = make_valid_move(valid_black_moves)