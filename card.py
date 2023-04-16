class Card:
    # Member variables
    # string name: the animal name of the card
    # string starting_color: either "red" or "blue" for initializing the game
    # (int, int) movement[]: an array of possible moves that the card allows in terms of relative position.


    def __init__(self, name, starting_color, movement):
        self.name = name

        self.starting_color = starting_color

        self.movement = movement