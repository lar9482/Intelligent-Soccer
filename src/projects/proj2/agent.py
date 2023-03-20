#!/usr/bin/env python3

from lib.game import Agent, RandomAgent
import sys
import random
import math

from MCTS.node import node

class MinimaxAgent(RandomAgent):
    """An agent that makes decisions using the Minimax algorithm, using a
    evaluation function to approximately guess how good certain states
    are when looking far into the future.

    :param evaluation_function: The function used to make evaluate a
        GameState. Should have the parameters (state, player_id) where
        `state` is the GameState and `player_id` is the ID of the
        player to calculate the expected payoff for.

    :param alpha_beta_pruning: True if you would like to use
        alpha-beta pruning.

    :param max_depth: The maximum depth to search using the minimax
        algorithm, before using estimates generated by the evaluation
        function.
    """
    def __init__(self, evaluate_function, alpha_beta_pruning=False, max_depth=5):
        super().__init__()
        self.evaluate = evaluate_function
        self.alpha_beta_pruning = alpha_beta_pruning
        self.max_depth = max_depth

    def decide(self, state):
        # TODO: Implement this agent!
        #
        # Read the documentation in /src/lib/game/_game.py for
        # information on what the decide function does.
        #
        # Do NOT call the soccer evaluation function that you write
        # directly from this function! Instead, use
        # `self.evaluate`. It will behave identically, but will be
        # able to work for multiple games.
        #
        # Do NOT call any SoccerState-specific functions! Assume that
        # you can only see the functions provided in the GameState
        # class.
        #
        # If you would like to see some example agents, check out
        # `/src/lib/game/_agents.py`.
        
        if not self.alpha_beta_pruning:
            return self.minimax(state, state.current_player, self.max_depth)
        else:
            return self.minimax_with_ab_pruning(state, state.current_player, self.max_depth, float('inf'), -float('inf'))

    def minimax(self, state, player, depth=1):
        # This is the suggested method you use to do minimax.  Assume
        # `state` is the current state, `player` is the player that
        # the agent is representing (NOT the current player in
        # `state`!)  and `depth` is the current depth of recursion.

        print('Executing simple minimax')
        utility, move = self.max_value(state, player, depth)

        # return super().decide(state)
        return move
    
    def minimax_with_ab_pruning(self, state, player, depth=1,
                                alpha=float('inf'), beta=-float('inf')):
        # return super().decide(state)
        print('Executing ab pruning')
        utility, move = self.max_value(state, player, depth, alpha, beta)
        return move

    def max_value(self, state, player, depth=1, alpha=None, beta=None):

        #A "leaf" node is reached if the state is terminal or the depth level has been exhausted
        if (state.is_terminal != None or depth == 0):
            return self.evaluate(state, player), None

        #Placeholder variables for the best utility and move
        value = -float('inf')
        move = random.choice(state.actions)

        for action in state.actions:
            #Get the state that results from executing the "action" on the current state
            result_state = state.act(action)
            
            #Skip actions that return invalid states
            if (result_state is None):
                continue
            
            #Get utility/best-action from the tree level below(aka min level)
            value2, action2 = self.min_value(result_state, result_state.current_player, depth, alpha, beta)

            #Keep track of utility/action pair that has a higher utility.
            if (value2 > value):
                value, move = value2, action

                #If alpha-beta pruning is enabled, keep track of the highest utility so far 
                # through alpha 
                if (alpha != None):
                    alpha = max(alpha, value)
            
            #If alpha-beta pruning is enabhled, immediately return utility/action pair whose utility
            #happens less than beta. This indicates that the best utility has been found
            if (beta != None and beta >= value):
                return value, move

        #Return the best utility/action pair of this level.
        return value, move

    def min_value(self, state, player, depth=1, alpha=None, beta=None):

        #A "leaf" node is reached if the state is terminal or the depth level has been exhausted
        if (state.is_terminal != None or depth == 0):
            return self.evaluate(state, player), None


        #Placeholder variables for the best utility and move
        value = float('inf')
        move = random.choice(state.actions)
        
        for action in state.actions:
            result_state = state.act(action)
            
            #Skip actions that return invalid states
            if (result_state is None):
                continue
            
            #Get utility/best-action from the tree level below(aka max level)
            value2, action2 = self.max_value(result_state, result_state.current_player, depth-1, alpha, beta)

            #Keep track of utility/action pair that has a lower utility.
            if (value2 < value):
                value, move = value2, action

                if (beta != None):
                    beta = min(beta, value)
                
            if (alpha != None and value <= alpha):
                return value, move

        #Return the best utility/action pair of this level.
        return value, move

class MonteCarloAgent(RandomAgent):
    """An agent that makes decisions using Monte Carlo Tree Search (MCTS),
    using an evaluation function to approximately guess how good certain
    states are when looking far into the future.

    :param evaluation_function: The function used to make evaluate a
        GameState. Should have the parameters (state, player_id) where
        `state` is the GameState and `player_id` is the ID of the
        player to calculate the expected payoff for.

    :param max_playouts: The maximum number of playouts to perform
        using MCTS.
    """
    def __init__(self, evaluate_function, max_playouts=100):
        super().__init__()

        #Basically the playout policy
        self.evaluate = evaluate_function

        #The number of playouts that need to be happen to choose a node.
        self.max_playouts = max_playouts

    def decide(self, state):
        # TODO: Implement this agent!
        #
        # Read the documentation in /src/lib/game/_game.py for
        # information on what the decide function does.
        #
        # Do NOT call the soccer evaluation function that you write
        # directly from this function! Instead, use
        # `self.evaluate`. It will behave identically, but will be
        # able to work for multiple games.
        #
        # Do NOT call any SoccerState-specific functions! Assume that
        # you can only see the functions provided in the GameState
        # class.
        #
        # If you would like to see some example agents, check out
        # `/src/lib/game/_agents.py`.

        return self.monte_carlo(state, state.current_player)

    def monte_carlo(self, state, player):
        # This is the suggested method you use to do MCTS.  Assume
        # `state` is the current state, `player` is the player that
        # the agent is representing (NOT the current player in
        # `state`!).
        tree = node(state, player)

        for curr_playout in range(0, self.max_playouts):
            
            #Select a leaf node in the tree according to the selection policy.
            leaf_node = self.select(tree)

            #Given all actions, expand leaf_node's children and get the child that has the highest evaluation
            child_node = self.expand(leaf_node)

            #Simulate the soccer game from the child node.
            (utility, final_state) = self.simulate(child_node)

            self.propagate(utility, final_state, child_node)

        return super().decide(state)
    
    def select(self, tree):
        leaf_node = tree

        #If the current leaf_node has children, then perform a selection policy search.
        while (leaf_node.children != []):

            #Keeping track of the node that maximizes the selection policy
            max_selection_utility = -sys.maxsize - 1
            possible_successor = leaf_node

            #Given the children of the current leaf node, 
            # identify the node that maximizes the selection policy
            for child_node in leaf_node.children:
                curr_selection_utility = self.selection_policy(child_node)

                if (curr_selection_utility > max_selection_utility):
                    max_selection_utility = curr_selection_utility
                    possible_successor = child_node
            
            leaf_node = possible_successor

        return leaf_node
    
    #Implementation of a simple UCB selection policy
    def selection_policy(self, node):        
        exploit_term = (node.total_utility) / (node.total_playouts)
        explore_term = math.sqrt(2) * math.sqrt(
            math.log(node.parent.total_playouts) / (node.total_playouts)
        )
        return exploit_term + explore_term

    #Expands children nodes to the inputted leaf node 
    #based on all possible actions avaliable for the leaf node's state.
    #The child node with the highest evaluation is returned
    def expand(self, leaf_node):
        curr_state = leaf_node.state
        
        #Keep track of the child node that has the highest evaluation.
        possible_successor_node = None
        max_eval = -sys.maxsize - 1

        #For every action in the leaf node's state, construct a child node from the taken action.
        #Also keep track of the children's maximum evaluation.
        for action in curr_state.actions:
            new_state = curr_state.act(action)

            if (new_state is None):
                continue
            
            eval = self.evaluate(new_state, new_state.current_player)

            #Given the new state with its associated evaluation, make a new child node
            #for the inputted leaf node.
            new_node = node(new_state, new_state.current_player)
            leaf_node.children.append(new_node)
            new_node.parent = leaf_node

            if (eval > max_eval):
                max_eval = eval
                possible_successor_node = new_node

        #Return the child node with the highest evaluation
        return possible_successor_node
    
    def simulate(self, child):

        #Keep track of the current state and previously seen states.
        curr_state = child.state
        seen_states = [curr_state]
        
        #Loop until the state is terminal or has been repeated.
        while (True):

            #Track the resultant state that has the maximium evaluation
            #according to the playout policy
            result_state = None
            max_eval = -sys.maxsize - 1

            #For every action, get the resultant state that returns the highest evaluation
            for action in curr_state.actions:
                new_state = curr_state.act(action)
                if (new_state is None):
                    continue
                new_eval = self.evaluate(new_state, new_state.current_player)

                if (new_eval > max_eval):
                    max_eval = new_eval
                    result_state = new_state

            #Test if the result state is terminal or has been repeated
            if (result_state.is_terminal != None or result_state in seen_states):
                break
            
            #Append result state to be tested for repeating states later
            seen_states.append(result_state)
            curr_state = result_state
        
        return (self.evaluate(curr_state, curr_state.current_player), curr_state)
    
    def propagate(self, utility, final_state, leaf_node):
        curr_node = leaf_node

        #For every node from the current leaf node to the root of the tree,
        #update the utility and playouts.
        while (curr_node != None):
            if (curr_node.player_id == final_state.current_player):
                curr_node.total_utility += utility

            curr_node.total_playouts += 1

            curr_node = curr_node.parent