class Pawn:
    # Member variables
    # bool is_master: true for a master pawn ("king") only
    # string color: either "red" or "blue"
    # (int, int) coordinates: the (row, col) position of this pawn


    def __init__(self, is_master, color, coordinates):
        self.is_master = is_master

        self.color = color

        self.coordinates = coordinates