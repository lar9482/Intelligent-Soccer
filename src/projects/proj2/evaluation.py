#!/usr/bin/env python3

import math, random
from ...lib.game import discrete_soccer

def soccer(state, player_id):
    ## TODO: Implement this function!
    #
    # The soccer evaluation function *must* look into the game state
    # when running. It will then return a number, where the larger the
    # number, the better the expected reward (or lower bound reward)
    # will be.
    #
    # For a good evaluation function, you will need to
    # SoccerState-specific information. The file
    # `src/lib/game/discrete_soccer.py` provides a description of all
    # useful SoccerState properties.
    if not isinstance(state, discrete_soccer.SoccerState):
        raise ValueError("Evaluation function incompatible with game type.")
    pass

def connect_four(state, player_id):
    return 0
