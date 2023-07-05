# Piece Super & Sub class
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
        self.moves = {
            "move_nw": None,
            "move_ne": None,
            "move_sw": None,
            "move_se": None
        }

    def check_valid_move(self):
        self.moves.update({key: None for key in self.moves})  # Reset possible moves before check
        xy_coord_copy = self.xy_coord
        if (xy_coord_copy[0] - 1 >= 1) and (xy_coord_copy[1] + 1 <= 8):  # Check NW
            self.moves["move_nw"] = xy_coord_copy[0] - 1, xy_coord_copy[1] + 1
        if (xy_coord_copy[0] + 1 <= 8) and (xy_coord_copy[1] + 1 <= 8):  # Check NE
            self.moves["move_ne"] = xy_coord_copy[0] + 1, xy_coord_copy[1] + 1
        if (xy_coord_copy[0] - 1 >= 1) and (xy_coord_copy[1] - 1 >= 1):  # Check SW
            self.moves["move_sw"] = xy_coord_copy[0] - 1, xy_coord_copy[1] - 1
        if (xy_coord_copy[0] + 1 <= 8) and (xy_coord_copy[1] - 1 <= 8):  # Check SE
            self.moves["move_se"] = xy_coord_copy[0] + 1, xy_coord_copy[1] - 1
        return self.moves


# Board Super & Sub class
class Board():

    def __init__(self, dimension):
        self.dimension = dimension
        self.x_coord = dimension[0]
        self.y_coord = dimension[1]
        self.xy_coord = self._generate_dimension()
        self.board_space_color = self._generate_board_space_color(self.xy_coord)
        self.black_spaces = self.board_space_color[0]
        self.white_spaces = self.board_space_color[1]
        self.visual = self._generate_visual()

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
        # Return black and then white
        return sorted_black_list, sorted_white_list

    def _generate_position_visual(self, xy_coord, flashing=False):
        if self.xy_coord[xy_coord] is None and (xy_coord in self.black_spaces):
            # If empty space on black tile
            background_color = "\033[30m" # Black
            reset_color = "\033[0m"
            visual_check = f"{background_color}   {reset_color}"
            return visual_check
        elif self.xy_coord[xy_coord] is None and (xy_coord in self.white_spaces):
            # If empty space on white tile
            background_color = "\033[100m" # Dark Grey
            #background_color = "\033[47m" # White 
            reset_color = "\033[0m"
            visual_check = f"{background_color}   {reset_color}"
            return visual_check
        else:
            piece = self.xy_coord[xy_coord]
            # board_location = piece.xy_coord
            if piece.team == "white":
                if flashing:
                    return "[\033[37;5mo\033[0m]"
                else:
                    return " o "
            if piece.team == "black":
                if flashing:
                    return "\033[5;90m[o]\033[0m"
                else:
                    return " \033[90mo\033[0m "

    def _generate_visual(self, flashing_position=None):  # Generate visual representation with coordinates on the outside
        visual_object = ""
        for y in range(self.y_coord, 0, -1):
            visual_object += f" {y} "
            for x in range(1, self.x_coord + 1):
                xy_coord = (x, y)
                if xy_coord == flashing_position:
                    flashing = True
                else:
                    flashing = False
                visual_object += self._generate_position_visual(xy_coord, flashing)
            visual_object += "\n"
        visual_object += "   "
        for x in range(1, self.x_coord + 1):
            visual_object += f" {x} "
        # print("\033[H\033[J") # Visual Trick to make it look cleaner.
        return visual_object

    def _place_at_location(self, xy_coord, piece):
        if self.xy_coord[xy_coord] is None:  # If space is empty, place piece and return True
            self.xy_coord[xy_coord] = piece
            return True, (f"Valid move, {piece.name} has been placed at {xy_coord}")
        else:  # If space is full, return False
            return False, (f"Invalid move, {self.xy_coord[xy_coord]} is already located at {xy_coord}")

    def get_from_location(self, xy_coord):  # Return whatever is at the given x,y coord
        return self.xy_coord[xy_coord]

    def remove_from_location(self, xy_coord, capture=False):  # Remove piece at location
        if self.xy_coord[xy_coord] is None:
            return False, ("Nothing is here")
        if self.xy_coord[xy_coord] is not None:  # Something is here, return True and the piece at this location and set x,y to None
            piece_to_return = self.xy_coord[xy_coord]
            self.xy_coord[xy_coord] = None
            return True, piece_to_return, (f"{piece_to_return} is located here. Removing {piece_to_return}")

    def move(self, xy_coord, piece): # This is one way to do it, but I could also use the above in get + remove to first check if a move if valid
        check = self._place_at_location(xy_coord, piece)
        if check[0] is True:
            print(check[1])
        if check[0] is False:
            print(check[1])

    def get_state(self):  # Gives me the dictionary in all its glory
        return self.xy_coord

    def clear_board(self):
        for all_keys in self.xy_coord:
            self.xy_coord[all_keys] = None


class Checkers_Board(Board):
    def __init__(self):
        super().__init__((8, 8))
        # List of white/black objects
        self.white_pieces = self.create_pieces("white")
        self.black_pieces = self.create_pieces("black")

    def board_setup(self):  # Place all Checker Pieces
        white_start_coord_unsort = []
        black_start_coord_unsort = []
        for location in self.xy_coord:
            # Top of Board. White Pieces
            if location[1] >= 6:
                if location[0] % 2 == 1 and location[1] % 2 == 1:
                    white_start_coord_unsort.append(location)
                if location[0] % 2 == 0 and location[1] % 2 == 0:
                    white_start_coord_unsort.append(location)
            # Bottom of Board. Black Pieces
            if location[1] <= 3:
                if location[0] % 2 == 1 and location[1] % 2 == 1:
                    black_start_coord_unsort.append(location)
                if location[0] % 2 == 0 and location[1] % 2 == 0:
                    black_start_coord_unsort.append(location)
        white_start_coord = sorted(white_start_coord_unsort, key=lambda y: y[1])
        black_start_coord = sorted(black_start_coord_unsort, key=lambda y: y[1], reverse=True)
        
        # White Piece Placement
        for i in range(0, len(white_start_coord)):
            white_xy_coord = (white_start_coord[i])
            white_piece = self.white_pieces[i]
            self._place_at_location(white_xy_coord, white_piece)
            self.white_pieces[i].update_position(white_xy_coord)
        # Black Piece Placement
        for i in range(0, len(black_start_coord)):
            black_xy_coord = (black_start_coord[i])
            black_piece = self.black_pieces[i]
            self._place_at_location(black_xy_coord, black_piece)
            self.black_pieces[i].update_position(black_xy_coord)
        # Update Visual
        self.visual = self._generate_visual()

    def create_pieces(self, name):
        piece_list = []
        for i in range(1, 13):
            obj = Checkers_Game_Piece(name, i)
            piece_list.append(obj)
        return piece_list

    def is_regular_move_valid(self, piece):
        check_move = piece.check_valid_move()
        if piece.team == "white":  # White starts Top and must move Down
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

        if piece.team == "black":  # Black starts Bottom and must move Up
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

    def can_capture(self, starting_loc, opp_piece):
        # We add the opposite direction
        # So we if start from the sw of the opp piece we check the ne
        print(f"can_capture starting_loc arg debug {starting_loc}")
        space_behind = opp_piece.moves[starting_loc]
        print(f"can_capture() space_behind debug {space_behind}")
        if space_behind is not None:
            check_space = self.get_from_location(space_behind)
            print(f"can_capture() check_space debug {check_space}")
            if check_space is None:
                print(f"Space at {space_behind} behind {opp_piece} is Empty")
                print("You must capture this piece")
                return True
            else:
                return False
        else:
            return False

    def remove_piece(self, xy_coord):
        piece_to_remove = self.xy_coord[xy_coord]
        name_to_remove = piece_to_remove.name
        if piece_to_remove is not None:
            if piece_to_remove.team == "white":
                for piece in self.white_pieces:
                    if piece.name == name_to_remove:
                        self.white_pieces.remove(piece)
            elif piece_to_remove.team == "black":
                for piece in self.black_pieces:
                    if piece.name == name_to_remove:
                        self.black_pieces.remove(piece)
            self.xy_coord[xy_coord] = None
