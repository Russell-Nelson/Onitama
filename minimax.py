from onitama import Onitama
import numpy as np

# blue winning gives a higher positive value
def evaluation(state):
    eval = 0
    eval += len(state.blue_player.pawns) - len(state.red_player.pawns)
    return eval

def evaluation2(state):
    if (state.game_is_over() == "blue wins"):
        return 10
    elif (state.game_is_over() == "red wins"):
        return -10
    else:
        return len(state.blue_player.pawns) - len(state.red_player.pawns)

def evaluation3(state):
    if (state.game_is_over() == "blue wins"):
        return 10
    elif (state.game_is_over() == "red wins"):
        return -10
    else:
        ret_value = len(state.blue_player.pawns) - len(state.red_player.pawns)
        for pawn in state.blue_player.pawns:
            ret_value -= abs(pawn.coordinates[0] - 4) / 40
            ret_value -= abs(pawn.coordinates[1] - 2) / 25
        return ret_value


# This algorithm is pulled from the public repo of code for the book "Artificial Intelligence: A Modern Approach"
# https://github.com/aimacode
def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action
