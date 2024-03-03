import random

from CheckersSolver import CheckersSolver
from MinMaxSearch import alpha_beta_search
from MinMaxSearch import minmax_decision
def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move


def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None


def alpha_beta_player(game, state):
    return alpha_beta_search(state, game)


def minmax_player(game,state):
    return minmax_decision(state,game)

def custom_player(game, state):
    solver = CheckersSolver(state)
    solver.add_variables()
    solver.add_constraints()
    solver.add_objective()
    return solver.solve()