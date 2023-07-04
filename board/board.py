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
        self.visual = self._generate_visual()

    def _generate_dimension(self):
        board_coor = {}
        for x_coord in range(1, self.x_coord + 1):
            for y_coord in range(1, self.y_coord + 1):
                xy_coord = (x_coord, y_coord)
                board_coor[xy_coord] = None
        return board_coor

    def _generate_position_visual(self, xy_coord, flashing=False):
        if self.xy_coord[xy_coord] is None:
            return "[ ]"
        else:
            if flashing:
                return "[\033[37;5m*\033[0m]"
            else:
                return "[*]"

    def _generate_visual(self, flashing_position=None):  # Generate visual representation with coordinates on the outside
        """
        Currently this exists as a visual debugging tool 
        during game logic testing.
        
        To be done at end:

        The below ANSII prints {var} as blinking text in the bash terminal.
        Keep for later use in _generate_visual static method.

        After all game logic is created and functional we should abstract
        the GUI visual away from Board(). We could possibly tie the visual
        updates to the Board.get_state() function to then trigger a "clear" 
        cmd in the bash terminal and re-print the visual object to simulate
        a refreshing/updating board. This could allow us to have a Visual()
        that only executes when we ask it to actually function as a visual
        game within the terminal without being tied to the underlying game

        var = "*"
        var_blink = (f"\033[37;5m{var}\033[0m")
        bracket_left = "["
        bracket_right = "]"
        print(bracket_left+var_blink+bracket_right)
        """

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
        print("\033[H\033[J") # Visual Trick to make it look cleaner.
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
        if capture:
            # Add capture and .pop
            pass
        else:
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
        for i in range(1, 9):
            # Top of the Board. White Pieces
            self._place_at_location((i, 7), self.white_pieces[i-1])
            self.white_pieces[i-1].update_position((i, 7))
            self._place_at_location((i, 8), self.white_pieces[i+self.x_coord-1])
            self.white_pieces[i+self.x_coord-1].update_position((i, 8))

            # Bottom of the Board. Black Pieces
            self._place_at_location((i, 1), self.black_pieces[i-1])
            self.black_pieces[i-1].update_position((i, 1))
            self._place_at_location((i, 2), self.black_pieces[i+self.x_coord-1])
            self.black_pieces[i+self.x_coord-1].update_position((i, 2))

        # Update Visual
        self.visual = self._generate_visual()

    def create_pieces(self, name):
        piece_list = []
        for i in range(1, self.x_coord + self.y_coord + 1):
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
    # def is_enemy_present():

    # def can_capture(opp_piece):
    #     opposite_dictionary = {
            
    #     }
    #     # i need to check direction relative to piece