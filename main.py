from board.board import *


# Testing

# Generate Board & Pieces
checkers_board = Checkers_Board()
checkers_board.board_setup()
print(checkers_board.visual)


def cycle_through_pieces(list_of_pieces):
    list_length = len(list_of_pieces)
    index = 0
    selected_piece = None
    while selected_piece is None:
        current_piece = list_of_pieces[index]
        print(f"Current piece: {current_piece.name}")
        user_input = input("Enter 'q' for previous, 'e' for next or 's' to select: ")
        if user_input == "q":
            index = (index + 1) % list_length  # Cycle to the next index
            continue
        if user_input == "e":
            index = (index - 1) % list_length  # Cycle to the next index
            continue
        elif user_input == "s":
            selected_piece = current_piece
    return selected_piece


def show_valid_moves(valid_moves):
    show_choices = []
    for name, value in valid_moves.items():
        if value:
            show_choices.append(name)
    return show_choices


def make_valid_move(valid_moves, piece):
    player_options = show_valid_moves(valid_moves)
    print(f"Here are your valid moves: {player_options}")
    user_input = input("Make a choice: ")
    if user_input in valid_moves:
        print(f"You choice was to move to {user_input}")
        selected_move = piece.moves[user_input]
        checkers_board.move(selected_move, piece)  # Move piece to (x, y) location
        checkers_board.remove_from_location(piece.xy_coord)  # Remove piece from board at its previous (x, y)
        piece.xy_coord = selected_move  # Update (x, y) of piece.xy_coord attr
        piece.check_valid_move()  # Update piece.moves to reflect new possible moves

        print(checkers_board._generate_visual())
    else:
        print("Invalid Move. Try Again")
        make_valid_move(valid_moves, piece)

def player_turn(team, name):
    print(f"Player {name} Turn")
    if team == "white":
        selected_piece = cycle_through_pieces(checkers_board.white_pieces)

    elif team == "black":
        selected_piece = cycle_through_pieces(checkers_board.black_pieces)
       
    print(selected_piece.name, selected_piece.xy_coord)
    can_this_move = checkers_board.is_regular_move_valid(selected_piece)
    
    if all(value is False for value in can_this_move.values()):  # Check to see if select piece is capable of making a valid move
        print("This piece has no valid moves. Choose another piece")
        player_turn(team, name)

    else:
        if selected_piece.team == "white":
            valid_white_moves = checkers_board.is_regular_move_valid(selected_piece)
            make_valid_move(valid_white_moves, selected_piece)
        if selected_piece.team == "black":
            valid_black_moves = checkers_board.is_regular_move_valid(selected_piece)
            make_valid_move(valid_black_moves, selected_piece)


# Turn Order
is_game_active = True
while is_game_active == True:
    WHITE_TEAM = "white"
    BLACK_TEAM = "black"
    player_1_name = "Hans"
    player_2_name = "Wes"
    turn1 = player_turn(WHITE_TEAM, player_1_name)
    turn2 = player_turn(BLACK_TEAM, player_2_name)
