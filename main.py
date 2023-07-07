from board.board import *

"""
Next Steps:

We could likely put the Piece and Board Logic sections within their
respective subclasses.

We could put Visual Logic block with current _generate_visual
funcs in Board() Class. We could also take all of the visual code
and place it in its own class away from Board().

We can wrap this main.py into a main() to begin and operate
the turns of the game. Future logic could show players how many
pieces they have captured, add more info, etc. We need to add an
end state/win condition. Currently the two possible options are
1) all pieces from one team are gone, and 2) no valid moves remain (tie).

We should try and implement logging for dev work vs production.

We should also look into adding a cpu opponent, possibly pytorch. But we
would keep these away from the logic we have currently implemented and import
it as a player character.
"""


"""
Visual Logic
"""
def visual_display(current_piece):
    # Visual Block
    flashing_position = current_piece.xy_coord
    visual = checkers_board.generate_visual_with_flashing(flashing_position)
    piece_number = current_piece.name.split("_")[-1]
    print(f"      {current_piece.team.capitalize()} Players Turn")
    print("   " + "-" * 24)
    print(visual)
    print(f"{current_piece.team.capitalize()} Piece {piece_number} at {current_piece.xy_coord}")

"""
Piece Logic
"""

def show_valid_moves(valid_moves): # Fancy Print Statement for valid_moves
    show_choices = []
    for name, value in valid_moves.items():
        if value:
            show_choices.append(name)
    return show_choices


def process_move(valid_moves, piece, capture=False):
    player_options = show_valid_moves(valid_moves)
    print(f"Here are your valid moves: {player_options}")
    user_input = input("Make a choice: ")
    
    if (user_input in valid_moves) and (capture is True): # If you can capture do so
        selected_move = valid_moves[user_input]
        capture_coord = piece.moves[user_input]
        # print(f"Debug capture {capture_coord}")
        checkers_board.remove_piece_from_game(capture_coord)  # Remove captured Piece from
        checkers_board.move(selected_move, piece)  # Move Player piece to new coord
        checkers_board.remove_from_location(piece.xy_coord) # Remove Player piece from old coord
        # print(f"Debug selected_move {selected_move}")
        # print(f"Debug piece.moves {piece.moves}")
        # piece.xy_coord = selected_move  # Update (x, y) of piece.xy_coord attr
        piece.update_position(selected_move) # Update (x, y) of piece.xy_coord attr
        # print(f"debug of piece.xy_coord {piece.xy_coord}")
        piece.check_valid_move()  # Update piece.moves to reflect new possible moves
        checkers_board.check_king_me(piece)  # Update piece.is_king if possible
        is_game_over() # Check for Victory Condition
        # print(f"Debug of updated piece.moves {piece.moves}") 

        """
        currently a bug where capture flag is incorrectly made false when it should be 
        true. this causes the below elif statement to trigger and the piece during what 
        should be a capture move instead normally moves into the space, but it is occupied by the opp_piece
        """

    elif user_input in valid_moves and (capture is False):  # If you can't capture, move regularly
        print(f"You choice was to move to {user_input}")
        selected_move = piece.moves[user_input]
        checkers_board.move(selected_move, piece)  # Move piece to (x, y) location
        checkers_board.remove_from_location(piece.xy_coord)  # Remove piece from board at its previous (x, y)
        # piece.xy_coord = selected_move  # Update (x, y) of piece.xy_coord attr
        piece.update_position(selected_move) # Update (x, y) of piece.xy_coord attr
        piece.check_valid_move()  # Update piece.moves to reflect new possible moves
        checkers_board.check_king_me(piece)  # Update piece.is_king if possible
    else:
        print("Invalid Move. Try Again")
        process_move(valid_moves, piece)


def check_capturable_moves(selected_piece, team):
    can_this_move = checkers_board.is_regular_move_valid(selected_piece)
    # print(f"Debug for capture can_this_move {can_this_move}")
    capturable_moves = {}
    for move in can_this_move:
        if can_this_move[move] is False:
            check_space = selected_piece.moves[move]
            # print(f"Debug for check_space {check_space}")
            if check_space is not None:
                opp_piece = checkers_board.get_from_location(check_space)
                # print(f"Debug for opp_piece{opp_piece}")
                if opp_piece.team != team:
                    check_capture_condition = checkers_board.check_for_capture(move, opp_piece)
                    # print(f"Debug for check_capture_condition {check_capture_condition}")
                    if check_capture_condition is True:
                        capturable_moves[move] = opp_piece.moves[move]

    return capturable_moves

"""
Turn/Board Logic
"""

def player_turn(team, name):
    print(f"Player {name} Turn")
    if team == "white":
        # Add logic to force capture before piece selection
        force_capture_pieces = board_force_capture(team, checkers_board.white_pieces)
        if force_capture_pieces:
            print(force_capture_pieces)
            process_piece_selection(team, force_capture_pieces)
        else:
            process_piece_selection(team, checkers_board.white_pieces)
    elif team == "black":
        # Add logic to force capture before piece selection
        force_capture_pieces = board_force_capture(team, checkers_board.black_pieces)
        if force_capture_pieces:
            print(force_capture_pieces)
            process_piece_selection(team, force_capture_pieces)
        else:
            process_piece_selection(team, checkers_board.black_pieces)


def board_force_capture(team, all_team_pieces):
    # print("Debug board_force_capture() block")
    force_captures_list = []
    
    for piece in all_team_pieces: # Iterate through all possible pieces and potential captures
        capturable_move = check_capturable_moves(piece, team)
        if capturable_move:
            force_captures_list.append(piece)
    
    if force_captures_list: # If dict contains value captures return it
        # print(f"Debug list_of_force_captures: {force_captures_list}")
        return force_captures_list

    else: # Dict has no valid captures. Return False
        return False

"""
Bug #1 Check recursive logic
"""
def process_piece_selection(team, pieces, recursion=False):
    if recursion is True:
        selected_piece = pieces  # pieces always a single obj here due to prior recursion
        visual_display(selected_piece)  # Visual Board in Terminal
    else:
        selected_piece = select_piece(pieces)

    capturable_moves = check_capturable_moves(selected_piece, team)
    if capturable_moves:
        # print(f"Debug moves before capture {selected_piece.moves}")
        process_move(capturable_moves, selected_piece, capture=True)
        # print(f"Debug moves after capture {selected_piece.moves}")
        # print(f"Debug moves after is_regular_move_valid {selected_piece.moves}")
        new_capture_choices = check_capturable_moves(selected_piece, team)
        # print(f"Debug new_capture_choices{new_capture_choices}")
        if new_capture_choices:  # If new choice start recursion
            process_piece_selection(team, selected_piece, recursion=True)
    else:
        valid_moves = checkers_board.is_regular_move_valid(selected_piece)
        if all(value is False for value in valid_moves.values()):  # Recusively restart turn
            print("This piece has no valid moves. Select another piece")
            process_piece_selection(team, pieces)
        else:
            process_move(valid_moves, selected_piece)


def select_piece(pieces):
    selected_piece = cycle_through_pieces(pieces)
    # print(selected_piece.name, selected_piece.xy_coord)
    return selected_piece


def cycle_through_pieces(list_of_pieces): # Allow player to cycle through all available game_pieces
    list_length = len(list_of_pieces)
    index = 0
    selected_piece = None

    while selected_piece is None:
        current_piece = list_of_pieces[index]
        visual_display(current_piece)   # Visual Board in Terminal
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


def is_game_over():
    if (len(checkers_board.white_pieces) == 0) or (len(checkers_board.black_pieces) == 0):
        print("Game Over")
        global is_game_active
        is_game_active= False

"""
Main() for Checkers Game
"""

# Generate Board & Pieces
checkers_board = Checkers_Board()
checkers_board.board_setup()
# print(checkers_board.xy_coord)
# print(checkers_board.visual)
# print(checkers_board.get_state())

# Turn Order -> wrap in main()
is_game_active = True
while is_game_active is True:
    WHITE_TEAM = "white"
    BLACK_TEAM = "black"
    player_1_name = "Hans"
    player_2_name = "Angel"
    turn1 = player_turn(WHITE_TEAM, player_1_name)
    turn2 = player_turn(BLACK_TEAM, player_2_name)
