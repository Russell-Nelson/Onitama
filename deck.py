from card import Card
import random

class Deck:
    # Member variables
    # Card deck[]: all of the cards in a game

    def __init__(self):
        # this initializer makes all 16 unique cards in the game.
        self.deck= [None] * 16
        self.deck[0] = Card("TIGER", "blue", [(-2, 0), (1, 0)])
        self.deck[1] = Card("CRAB", "blue", [(-1, 0), (0, -2), (0, 2)])
        self.deck[2] = Card("MONKEY", "blue", [(-1, -1), (-1, 1), (1, -1), (1, 1)])
        self.deck[3] = Card("CRANE", "blue", [(-1, 0), (1, -1), (1, 1)])
        self.deck[4] = Card("DRAGON", "red", [(-1, -2), (-1, 2), (1, -1), (1, 1)])
        self.deck[5] = Card("ELEPHANT", "red", [(-1, -1), (-1, 1), (0, -1), (0, 1)])
        self.deck[6] = Card("MANTIS", "red", [(-1, -1), (-1, 1), (1, 0)])
        self.deck[7] = Card("BOAR", "red", [(-1, 0), (0, -1), (0, 1)])
        self.deck[8] = Card("FROG", "red", [(-1, -1), (0, -2), (1, 1)])
        self.deck[9] = Card("GOOSE", "blue", [(-1, -1), (0, -1), (0, 1), (1, 1)])
        self.deck[10] = Card("HORSE", "red", [(-1, 0), (0, -1), (1, 0)])
        self.deck[11] = Card("EEL", "blue", [(-1, -1), (0, 1), (1, -1)])
        self.deck[12] = Card("RABBIT", "blue", [(-1, 1), (0, 2), (1, -1)])
        self.deck[13] = Card("ROOSTER", "red", [(-1, 1), (0, 1), (0, -1), (1, -1)])
        self.deck[14] = Card("OX", "blue", [(-1, 0), (0, 1), (1, 0)])
        self.deck[15] = Card("COBRA", "red", [(-1, 1), (0, -1), (1, 1)])

        # Then shuffles them.
        random.shuffle(self.deck)
