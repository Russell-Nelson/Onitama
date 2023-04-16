class Player:
    # Member variables
    # Card hand[2]: The two cards that are currently available to the player
    # string color: "red" or "blue"
    # bool has_master: tracks whether this player still has their master
    # Pawn[] pawns: a list of the pieces that the player has on the board

    def __init__(self, card1, card2, color, state):
        self.hand = [None] * 2
        self.hand[0] = card1
        self.hand[1] = card2
        self.color = color
        self.has_master = True
        self.pawns = []
        if (color == "blue"):
            for column in range(5):
                self.pawns.append(state.board[0][column].pawn)
        else:
            for column in range(5):
                self.pawns.append(state.board[4][column].pawn)
