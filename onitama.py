from move import Move
from game_state import Game_state
import random
import numpy as np
import copy

# This class is based around the Game class from the public repo of code for the book "Artificial Intelligence: A Modern Approach"
# https://github.com/aimacode
class Onitama:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        allowable_moves = []
        player = state.current_player
        for pawn in player.pawns:
            for c in range(2):
                for m in range(len(player.hand[c].movement)):
                    move = Move(pawn.coordinates[0], pawn.coordinates[1], c, m)
                    if move.is_valid(state, player):
                        allowable_moves.append(move)
        return allowable_moves

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        new_state = copy.deepcopy(state)
        move.perform_move(new_state, new_state.current_player)
        return new_state

    def utility(self, state, player):
        """Return the value of this final state to player."""
        # TODO: check how this is used in minimax
        if (player.color == "blue"):
            if (state.game_is_over() == "blue wins"):
                return np.inf
            else:
                return -np.inf
        else:
            if (state.game_is_over() == "red wins"):
                return np.inf
            else:
                return -np.inf

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        if not state.game_is_over():
            return False
        else:
            return True

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.current_player

    def display(self, state):
        """Print or otherwise display the state."""
        state.print_game_state()

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))
            

def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None

