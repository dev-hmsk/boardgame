class Board():

    def __init__(self, dimension):
        self.dimension = dimension  # Must be a tuple
        self.x_coor = dimension[0]
        self.y_coor = dimension[1]
        self.xy_coor = self._generate_dimension()
        self.visual = self._generate_visual()

    def _generate_dimension(self):
        board_coor = {}
        for x_coor in range(1, self.x_coor + 1):
            for y_coor in range(1, self.y_coor + 1):
                xy_coor = (x_coor,y_coor)
                board_coor[xy_coor] = None
        return board_coor
    
    def _generate_visual(self): # Iterate through all keys and represent their values visually. (1,1) starts at top left
        visual_object = ""
        for y in range(1, self.y_coor + 1):
            for x in range(1, self.x_coor + 1):
                xy_coor = (x, y)
                if self.xy_coor[xy_coor] is None:
                    visual_object += "[ ]"
                else:
                    visual_object += "[*]"
            visual_object += "\n"
        return visual_object
        
    def _place(self, xy_coor, item):
        if self.xy_coor[xy_coor] is None:  # If space is empty, place item and return True
            self.xy_coor[xy_coor] = item
            self.visual = self._generate_visual()
            return True, (f"Valid move, {item} has been placed at {xy_coor}")

        else: # If space is full, return False
            return False, (f"Invalid move, {self.xy_coor[xy_coor]} is already located at {xy_coor}")

    def get(self, xy_coor): # Return whatever is at the given x,y coor
        return self.xy_coor[xy_coor]

    def remove(self, xy_coor): # Remove item at location if able
        if self.xy_coor[xy_coor]is None:
            return False, ("Nothing is here")

        if self.xy_coor[xy_coor] is not None:  # Something is here, return True and the piece at this location and set x,y to None
            piece_to_return = self.xy_coor[xy_coor]
            self.xy_coor[xy_coor] = None
            return True, piece_to_return, (f"{piece_to_return} is located here. Removing {piece_to_return}")

    def move(self, xy_coor, item): # This is one way to do it, but i could also use the above in get + remove to first check if a move if valid
        check = self._place(xy_coor, item)

        if check[0] is True:
            print(check[1])

        if check[0] is False:
            print(check[1])

    def get_state(self): # Gives me the dictionary in all its glory
        return self.xy_coor
    
    def clear_board(self):
        for all_keys in self.xy_coor:
            self.xy_coor[all_keys] = None
            self.visual = self._generate_visual()

