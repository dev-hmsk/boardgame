from board.board import *


# Testing

# Generate Board & Pieces
checkers_board = Checkers_Board()
checkers_board.board_setup()
print(checkers_board.visual)
# print(checkers_board.get_state())


def cycle_through_pieces(list_of_pieces):
    list_length = len(list_of_pieces)
    index = 0
    selected_piece = None

    while selected_piece is None:
        current_piece = list_of_pieces[index]
        print(f"Current piece: {current_piece.name} at position {current_piece.xy_coord}")
        flashing_position = current_piece.xy_coord
        visual = checkers_board._generate_visual(flashing_position)
        print(visual)
        
        user_input = input("Enter 'q' for previous, 'e' for next or 's' to select: ")
        
        if user_input == "q":
            index = (index - 1) % list_length
            continue
        elif user_input == "e":
            index = (index + 1) % list_length
            continue
        elif user_input == "s":
            selected_piece = current_piece
        else:
            print("Invalid Input. Try Again")

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
    else:
        print("Invalid Move. Try Again")
        make_valid_move(valid_moves, piece)


def capture_piece(capturable_moves, piece):
    player_options = show_valid_moves(capturable_moves)
    print(f"capturable_moves debug {capturable_moves}")
    print(f"Here are your valid capture moves: {player_options}")
    user_input = input("Make a choice: ")
    if user_input in capturable_moves:
        selected_move = capturable_moves[user_input]
        capture_coord = piece.moves[user_input]
        print(f"capture debug {capture_coord}")
        checkers_board.remove_piece(capture_coord)
        checkers_board.move(selected_move, piece) # Move Player piece to new coord
        checkers_board.remove_from_location(piece.xy_coord) # Remove Player piece from old coord
        print(f"selected_move debug{selected_move}")
        print(f"piece.moves debug {piece.moves}")
        piece.xy_coord = selected_move  # Update (x, y) of piece.xy_coord attr
        print(f"debug of piece.xy_coord {piece.xy_coord}")
        piece.check_valid_move()  # Update piece.moves to reflect new possible moves
        print(f"Debug below of updated piece.moves {piece.moves}")
        
    else:
        print("Invalid Move. Try Again")
        make_valid_move(capturable_moves, piece)


def select_piece(pieces):
    selected_piece = cycle_through_pieces(pieces)
    print(selected_piece.name, selected_piece.xy_coord)
    return selected_piece


def check_capturable_moves(selected_piece, team):
    can_this_move = checkers_board.is_regular_move_valid(selected_piece)
    print("Debug for capture")
    print(can_this_move)

    capturable_moves = {}
    for move in can_this_move:
        if can_this_move[move] is False:
            check_space = selected_piece.moves[move]
            if check_space is not None:
                opp_piece = checkers_board.get_from_location(check_space)
                if opp_piece.team != team:
                    check_capture_condition = checkers_board.can_capture(move, opp_piece)
                    if check_capture_condition is True:
                        capturable_moves[move] = opp_piece.moves[move]
    return capturable_moves


def process_piece_selection(team, pieces):
    selected_piece = select_piece(pieces)

    capturable_moves = check_capturable_moves(selected_piece, team)
    if capturable_moves:
        capture_piece(capturable_moves, selected_piece)
    else:
        valid_moves = checkers_board.is_regular_move_valid(selected_piece)
        if all(value is False for value in valid_moves.values()):
            print("This piece has no valid moves. Select another piece")
            process_piece_selection(team, pieces)  # Recusively restart turn
        else:
            make_valid_move(valid_moves, selected_piece)


def player_turn(team, name):
    print(f"Player {name} Turn")
    if team == "white":
        # Add Logic to force capture before piece selection
        process_piece_selection(team, checkers_board.white_pieces)
    elif team == "black":
        # Add Logic to force capture before piece selection
        process_piece_selection(team, checkers_board.black_pieces)


def board_force_capture():
    '''
    I need to have the game force the player to capture
    a piece if available and not give him a choice to select another
    '''


# Turn Order
is_game_active = True
while is_game_active is True:
    WHITE_TEAM = "white"
    BLACK_TEAM = "black"
    player_1_name = "Hans"
    player_2_name = "Wes"
    turn1 = player_turn(WHITE_TEAM, player_1_name)
    turn2 = player_turn(BLACK_TEAM, player_2_name)



"""
Old player_turn code before abstraction
"""

# def player_turn(team, name):
#     print(f"Player {name} Turn")
#     if team == "white":
#         selected_piece = cycle_through_pieces(checkers_board.white_pieces)
#     elif team == "black":
#         selected_piece = cycle_through_pieces(checkers_board.black_pieces)
       
#     print(selected_piece.name, selected_piece.xy_coord)
#     can_this_move = checkers_board.is_regular_move_valid(selected_piece) # checks direction of potential moves. returns dict
#     print("Debug for capture")
#     print(can_this_move)
    
#     if any(value is False for value in can_this_move.values()): # If potential move is blocked checked why
#         capturable_move = {} # Make dict of all potential capturable moves
#         for move in can_this_move:
#             print(f"move in can_this_move {move}")
#             if can_this_move[move] is False: # If move is illegal, check for piece
#                 check_space = selected_piece.moves[move] # check_space is the (x, y) of a potential move space given by the moved piece
#                 print(f"check space dode {check_space}")
#                 if check_space is not None: # If piece exists check team
#                     opp_piece = checkers_board.get_from_location(check_space)
#                     print(f"opp piece {opp_piece}")
#                     if opp_piece.team != team: # If enemy, check for capture conditions
#                         check_capture_condition = checkers_board.can_capture(move, opp_piece)  # Return True/False if capturable
#                         if check_capture_condition is True: # If capturable, add move to list
#                             capturable_move[move] = opp_piece.moves[move]

#         print(f"These moves allow you to capture pieces {capturable_move}")
#         if capturable_move:  # If dict is not empty proceed to capture
#             capture_piece(capturable_move, selected_piece)
#         else:
#             valid_moves = checkers_board.is_regular_move_valid(selected_piece)
#             if all(value is False for value in valid_moves.values()):
#                 print("This piece has no valid moves. Select another piece")
#                 player_turn(team, name)
#             else:
#                 make_valid_move(valid_moves, selected_piece)
#     else:
#         valid_moves = checkers_board.is_regular_move_valid(selected_piece)
#         make_valid_move(valid_moves, selected_piece)