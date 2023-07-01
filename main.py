


class Board():

    def __init__(self, dimension):
        self.dimension = dimension  # Must be a tuple
        self.x_coor = dimension[0]
        self.y_coor = dimension[1]
        self.xy_coor = self._generate_dimension()

    def _generate_dimension(self):
        board_coor = {}

        for x_coor in range(1, self.x_coor + 1):
            for y_coor in range(1, self.y_coor + 1):
                xy_coor = ("x" + str(x_coor) + "y" + str(y_coor))
                board_coor[xy_coor] = None
        return board_coor
    
    def _place(self, xy_coor, item):

        if self.xy_coor[xy_coor] is None:  # If space is empty, place item and return True
            self.xy_coor[xy_coor] = item
            return True, (f"Valid move, {item} has been placed at {xy_coor}")
        
        else: # If space is full, return False
            return False, (f"Invalid move, {self.xy_coor[xy_coor]} is already located at {xy_coor}")

    def get(self, xy_coor): # Return whatever is at the given x,y coor
        return self.xy_coor[xy_coor]
        
    def remove(self, xy_coor): # Remove item at location if able
        if self.xy_coor[xy_coor] is None:
            return False, ("Nothing is here")

        if self.xy_coor[xy_coor] is not None:  # Something is here, return True and the piece at this location and set x,y to None
            piece_to_return = self.xy_coor[xy_coor]
            self.xy_coor[xy_coor] = None
            return True, piece_to_return, (f"{piece_to_return} is located here. Removing {piece_to_return}")

    def move(self, xy_coor, item):
        check = self._place(xy_coor, item)

        if check[0] == True:
            print(check[1])

        if check[0] == False:
            print(check[1])
        
    def get_state(self):
        return self.xy_coor


test_dim = (4, 4)
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