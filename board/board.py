# Game_Piece Super & Sub class
class Game_Piece():
    def __init__(self, color, number):
        self.name = color + "_piece_" + str(number)
        self.xy_coord = None
        self.team = color

    def update_position(self, xy_coord):
        self.xy_coord = xy_coord


class Checkers_Game_Piece(Game_Piece):
    def __init__(self, color, number):
        super().__init__(color, number)
        self.is_king = False
        self.moves = {
            "move_nw": None,
            "move_ne": None,
            "move_sw": None,
            "move_se": None
        }

    def king_me(self):
        self.is_king = True
        return
    """
    def demote(self):  # Not currently required
        self.is_king = False
        return
    """

    def check_valid_move(self):
        self.moves.update({key: None for key in self.moves})  # Reset possible moves before check
        if (self.xy_coord[0] - 1 >= 1) and (self.xy_coord[1] + 1 <= 8):  # Check NW
            self.moves["move_nw"] = self.xy_coord[0] - 1, self.xy_coord[1] + 1
        if (self.xy_coord[0] + 1 <= 8) and (self.xy_coord[1] + 1 <= 8):  # Check NE
            self.moves["move_ne"] = self.xy_coord[0] + 1, self.xy_coord[1] + 1
        if (self.xy_coord[0] - 1 >= 1) and (self.xy_coord[1] - 1 >= 1):  # Check SW
            self.moves["move_sw"] = self.xy_coord[0] - 1, self.xy_coord[1] - 1
        if (self.xy_coord[0] + 1 <= 8) and (self.xy_coord[1] - 1 <= 8):  # Check SE
            self.moves["move_se"] = self.xy_coord[0] + 1, self.xy_coord[1] - 1
        """
        If coordinate is less than 1 or greater than 8 in x or y 
        its invalid so remove it and set to None. We hardcode because 
        board game min/max dimensions are not known to a Checkers_Game_Piece()
        """
        for key, xy_coord in self.moves.items():
            try:
                if xy_coord is not None and (xy_coord[0] < 1) or (xy_coord[1] < 1) or (xy_coord[0] > 8) or (xy_coord[1] > 8):
                    self.moves[key] = None
            except TypeError:
                """
                This fixes "NoneType object is not subscriptable"
                It occurs if a piece is at the edge of a board
                """
                pass
        # print(f"Debug self.moves {self.moves}")
        return self.moves


# Board Super & Sub class
class Board():

    def __init__(self, dimension):
        self.dimension = dimension
        self.x_coord = dimension[0]
        self.y_coord = dimension[1]
        self.xy_coord = self._generate_dimension() # This is a dict that contains all (x,y) locations and Game_Piece objs on board
        self.board_space_color = self._generate_board_space_color(self.xy_coord)
        self.black_spaces = self.board_space_color[0] # Sorted List 
        self.white_spaces = self.board_space_color[1] # Sorted List
        self.visual = self._generate_visual_board() # Updates terminal with visual

    def _generate_dimension(self):
        board_coor = {}
        for x_coord in range(1, self.x_coord + 1):
            for y_coord in range(1, self.y_coord + 1):
                xy_coord = (x_coord, y_coord)
                board_coor[xy_coord] = None
        return board_coor

    def _generate_board_space_color(self, xy_coord):
        # (1,1) or bottom-most left is a black square
        black_spaces = []
        white_spaces = []
        for location in xy_coord:
            x_coord = location[0]
            y_coord = location[1]
            # Black Spaces aka legal piece spaces
            if x_coord % 2 == 0 and y_coord % 2 == 0:
                black_spaces.append(location)
            if x_coord % 2 != 0 and y_coord % 2 != 0:
                black_spaces.append(location)
            # White Spaces aka empty spaces
            if x_coord % 2 != 0 and y_coord % 2 == 0:
                white_spaces.append(location)
            if x_coord % 2 == 0 and y_coord % 2 != 0:
                white_spaces.append(location)

        sorted_black_list = sorted(black_spaces, key=lambda x: x[0])
        sorted_white_list = sorted(white_spaces, key=lambda x: x[0])
        return sorted_black_list, sorted_white_list  # Return black and then white

    def generate_visual_with_flashing(self, flashing_position):  # Public wrapper for assorted private _generate_visual funcs
        return self._generate_visual_board(flashing_position)
    
    def _generate_visual_board(self, flashing_position=None):
        """
        Function:
            Generates the visual representation of the board
        
        Parameters:
        - flashing_position: (x, y) coordinate to be highlighted as flashing.

        Description:
        The function iterates through each row and column of the board to build the visual.
        It creates an empty `board_display` string to store the generated visual representation.

        For each row (y-coordinate) in reverse order:
            - The y-coordinate is added to the 'board_display string
              as the left-side coordinate label.

            - For each column (x-coordinate) from 1 to self.x_coord:
                - The `(x, y)` coordinate is assigned to xy_coord.
                - If `xy_coord` matches the `flashing_position`,
                  the`flashing` variable is set to True, else set to False.

                - The visual representation of the position is generated using
                  the `_generate_position_visual`function, passing `xy_coord`
                  and `flashing` as arguments.

                - The generated visual_piece is appended to the `board_display` string.

            - A newline character is added to the `board_display`
              string to start a new row.
        
        After iterating through all rows, the horizontal coordinate 
        labels are added to the `board_display` string.
        
        Returns:
        - board_display: string representing the entire board
        """
            
        board_display = ""
        for y in range(self.y_coord, 0, -1):
            board_display += f" {y} "
            for x in range(1, self.x_coord + 1):
                xy_coord = (x, y)
                if xy_coord == flashing_position:
                    flashing = True
                else:
                    flashing = False
                board_display += self._generate_position_visual(xy_coord, flashing)
            board_display += "\n"
        board_display += "   "
        for x in range(1, self.x_coord + 1):
            board_display += f" {x} "
        print("\033[H\033[J")  # Visual trick to make terminal look cleaner. Can be safely commented out to debug
        return board_display

    def _generate_position_visual(self, xy_coord, flashing=False):
        """
       Function:
        - Generates the board spaces and pieces
        - Overlays game_piece on spaces as appropriate
        - Highlights currently selected piece through flashing=True arg

        Params:
        - xy_coord: The (x, y) coordinate of the position.
        - flashing: Specifies whether selected piece is flashing.

        Logic:
        - The function checks the `xy_coord` position on the board and 
          determines the visual representation based on the following conditions:

            - If the position is `None` and belongs to the black spaces,
              it generates a black tile visual space.

            - If the position is `None` and belongs to the white spaces,
              it generates a dark_grey or white tile visual space.

            - If the position is not `None`, it represents a game piece.
              The function retrieves the piece and generates the visual
              representation based on its team.

                - For white pieces, if `flashing` is True, it generates a
                  flashing white piece representation;
                  otherwise, a normal white piece representation.
                
                - For black pieces, if `flashing` is True, it generates a
                  flashing dark grey piece representation;
                  otherwise, a normal dark grey piece representation.

        Returns:
        - visual_space for empty spaces
        - flashing_visual_piece for currently selected piece
        - non_flashing_visual_piece for non-currently selected piece

        """
        if self.xy_coord[xy_coord] is None and (xy_coord in self.black_spaces):  # If empty space on black tile
            background_color = "\033[30m"  # Black option
            reset_color = "\033[0m"  # Neutral terminal color
            visual_space = f"{background_color}   {reset_color}"
            return visual_space
        elif self.xy_coord[xy_coord] is None and (xy_coord in self.white_spaces):  # If empty space on white tile
            background_color = "\033[100m"  # Dark Grey option
            # background_color = "\033[47m" # White option
            reset_color = "\033[0m"  # Neutral terminal color
            visual_space = f"{background_color}   {reset_color}"
            return visual_space
        else:
            piece = self.xy_coord[xy_coord]
            if piece.is_king is True:
                visual_piece = "K"
            if piece.is_king is False:
                visual_piece = "o"
            if piece.team == "white":
                if flashing:
                    flashing_visual_piece = f"[\033[37;5m{visual_piece}\033[0m]"
                    return flashing_visual_piece
                else:
                    non_flashing_visual_piece = f" {visual_piece} "
                    return non_flashing_visual_piece
            if piece.team == "black":
                if flashing:
                    flashing_visual_piece = f"[\033[5;90m{visual_piece}\033[0m]"
                    return flashing_visual_piece
                else:
                    non_flashing_visual_piece = f" \033[90m{visual_piece}\033[0m "
                    return non_flashing_visual_piece

    def _place_at_location(self, xy_coord, piece):
        if self.xy_coord[xy_coord] is None:  # If space is empty, place piece and return True
            self.xy_coord[xy_coord] = piece
            return True, (f"Valid move, {piece.name} has been placed at {xy_coord}")
        else:  # If space is full, return False
            return False, (f"Invalid move, {self.xy_coord[xy_coord]} is already located at {xy_coord}")

    def get_from_location(self, xy_coord):  # Return whatever is at the given x,y coord
        try:
            return self.xy_coord[xy_coord]
        except KeyError:
            return None

    def remove_from_location(self, xy_coord, capture=False):  # Remove piece at location
        if self.xy_coord[xy_coord] is None:
            return False, ("Nothing is here")
        if self.xy_coord[xy_coord] is not None:  # Something is here, return True and the piece at this location and set x,y to None
            piece_to_return = self.xy_coord[xy_coord]
            self.xy_coord[xy_coord] = None
            return True, piece_to_return, (f"{piece_to_return} is located here. Removing {piece_to_return}")

    def move(self, xy_coord, piece): 
        """
         This is one way to do it, but we could also use the 
         above get + remove to first check if a move if valid
        """
        check = self._place_at_location(xy_coord, piece)
        if check[0] is True:
            print(check[1])
        if check[0] is False:
            print(check[1])

    def get_state(self):
        return self.xy_coord

    def clear_board(self):
        for all_keys in self.xy_coord:
            self.xy_coord[all_keys] = None


class Checkers_Board(Board):
    def __init__(self):
        super().__init__((8, 8))
        # List of white/black objects
        self.white_pieces = self._create_pieces("white")  # List
        self.black_pieces = self._create_pieces("black")  # List
        self.all_king_rows = self._create_king_row()
        self.white_side_king_row = self.all_king_rows[0]  # This is (x, 8) row list
        self.black_side_king_row = self.all_king_rows[1]  # This is (x, 1) row list

    def board_setup(self):  # Place all Checker Pieces
        white_start_coord_unsort = []
        black_start_coord_unsort = []
        for location in self.xy_coord:
            if location[1] >= 6:  # Top of Board. White Pieces
                if location[0] % 2 == 1 and location[1] % 2 == 1:
                    white_start_coord_unsort.append(location)
                if location[0] % 2 == 0 and location[1] % 2 == 0:
                    white_start_coord_unsort.append(location)
            if location[1] <= 3:  # Bottom of Board. Black Pieces
                if location[0] % 2 == 1 and location[1] % 2 == 1:
                    black_start_coord_unsort.append(location)
                if location[0] % 2 == 0 and location[1] % 2 == 0:
                    black_start_coord_unsort.append(location)
        white_start_coord = sorted(white_start_coord_unsort, key=lambda y: y[1])
        black_start_coord = sorted(black_start_coord_unsort, key=lambda y: y[1], reverse=True)

        for i in range(0, len(white_start_coord)):  # White Piece Placement
            white_xy_coord = (white_start_coord[i])
            white_piece = self.white_pieces[i]
            self._place_at_location(white_xy_coord, white_piece)
            self.white_pieces[i].update_position(white_xy_coord)

        for i in range(0, len(black_start_coord)):  # Black Piece Placement
            black_xy_coord = (black_start_coord[i])
            black_piece = self.black_pieces[i]
            self._place_at_location(black_xy_coord, black_piece)
            self.black_pieces[i].update_position(black_xy_coord)
        self.visual = self._generate_visual_board()  # Update visual board in terminal

    def _create_pieces(self, name):
        piece_list = []
        for i in range(1, 13):
            obj = Checkers_Game_Piece(name, i)
            piece_list.append(obj)
        return piece_list

    def _create_king_row(self):
        white_side_king_row = []
        black__side_king_row = []
        for x_coord in range(1,9):
            white_side_king_row.append((x_coord, 8))
            black__side_king_row.append((x_coord, 1))

        return white_side_king_row, black__side_king_row

    def is_regular_move_valid(self, piece):  # Valid Non-King moves
        piece.check_valid_move()  # Update piece.moves
        if piece.is_king: # king_moves represent ability to move in any direction
            nw = piece.moves["move_nw"]  # NW
            ne = piece.moves["move_ne"]  # NE
            sw = piece.moves["move_sw"]  # SW
            se = piece.moves["move_se"]  # SE
            king_moves = {
                "move_nw": False,
                "move_ne": False,
                "move_sw": False,
                "move_se": False
            }
            if nw is not None:
                nw_space = self.get_from_location(nw)
                if nw_space is None:
                    king_moves["move_nw"] = True
            if ne is not None:
                ne_space = self.get_from_location(ne)
                if ne_space is None:
                    king_moves["move_ne"] = True
            if sw is not None:
                sw_space = self.get_from_location(sw)
                if sw_space is None:
                    king_moves["move_sw"] = True
            if se is not None:
                se_space = self.get_from_location(se)
                if se_space is None:
                    king_moves["move_se"] = True
            return king_moves

        elif piece.team == "white":  # White starts Top and must move Down
            sw = piece.moves["move_sw"]  # SW
            se = piece.moves["move_se"]  # SE
            white_moves = {
                "move_sw": False,
                "move_se": False
            }
            if sw is not None:
                sw_space = self.get_from_location(sw)
                if sw_space is None:
                    white_moves["move_sw"] = True
            if se is not None:
                se_space = self.get_from_location(se)
                if se_space is None:
                    white_moves["move_se"] = True
            return white_moves

        elif piece.team == "black":  # Black starts Bottom and must move Up
            nw = piece.moves["move_nw"]  # NW
            ne = piece.moves["move_ne"]  # NE
            black_moves = {
                "move_nw": False,
                "move_ne": False
            }
            if nw is not None:
                nw_space = self.get_from_location(nw)
                if nw_space is None:
                    black_moves["move_nw"] = True
            if ne is not None:
                ne_space = self.get_from_location(ne)
                if ne_space is None:
                    black_moves["move_ne"] = True
            return black_moves

    def check_for_capture(self, starting_loc, opp_piece):
        # print(f"Debug check_fo_capture starting_loc arg {starting_loc}")
        space_behind = opp_piece.moves[starting_loc]
        # print(f"Debug check_for_capture() space_behind {space_behind}")
        if space_behind is not None:
            check_space = self.get_from_location(space_behind)
            # print(f"Debug check_for_capture() check_space {check_space}")
            if check_space is None:
                # print(f"Debug Space at {space_behind} behind {opp_piece} is Empty")
                print("You must capture this piece")
                return True
            else:
                return False
        else:
            return False

    def remove_piece_from_game(self, xy_coord): 
        """
        Removes piece from the board and its 
        respective teams list of pieces
        """
        piece_to_remove = self.xy_coord[xy_coord]
        name_to_remove = piece_to_remove.name

        if piece_to_remove.team == "white":
            for piece in self.white_pieces:
                if piece.name == name_to_remove:
                    self.white_pieces.remove(piece)
        elif piece_to_remove.team == "black":
            for piece in self.black_pieces:
                if piece.name == name_to_remove:
                    self.black_pieces.remove(piece)
        self.xy_coord[xy_coord] = None


    def check_king_me(self, regular_piece):
        """
        Check if a piece is currently on a king_row.
        If so, update the pieces internal king flag using
        king_me()
        """
        if (regular_piece.team == "white") and (regular_piece.xy_coord in self.black_side_king_row): 
            regular_piece.king_me()
            # print(f"Debug for piece.is_king {regular_piece.is_king}")
        
        elif (regular_piece.team == "black") and (regular_piece.xy_coord in self.white_side_king_row): 
            regular_piece.king_me()
            # print(f"Debug for piece.is_king {regular_piece.is_king}")
