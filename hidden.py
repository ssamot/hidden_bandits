# This is a very simple implementation of the UCT Monte Carlo Tree Search algorithm in Python 2.7.
# The function UCT(rootstate, itermax, verbose = False) is towards the bottom of the code.
# It aims to have the clearest and simplest possible code, and for the sake of clarity, the code
# is orders of magnitude less efficient than it could be made, particularly by using a 
# state.GetRandomMove() or state.DoRandomRollout() function.
# 
# Example GameState classes for Nim, OXO and Othello are included to give some idea of how you
# can write your own GameState use UCT in your 2-player game. Change the game to be played in 
# the UCTPlayGame() function at the bottom of the code.
# 
# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
# 
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
# 
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai


# Modified my ssamot@essex.ac.uk so it addapt to

from math import *
import random

class GameState:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic 
        zero-sum game, although they can be enhanced and made quicker, for example by using a 
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
    """
    def __init__(self):
            self.playerJustMoved = 2 # At the root pretend the player just moved is player 2 - player 1 has the first move
        
    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        self.playerJustMoved = 3 - self.playerJustMoved
        
    def GetMoves(self):
        """ Get all possible moves from this state.
        """
    
    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm. 
        """

    def __repr__(self):
        """ Don't need this - but good style.
        """
        pass


class HiddenStateGame:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic
        zero-sum game, although they can be enhanced and made quicker, for example by using a
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
    """
    observation_policy = {}
    # B, D, Action
    observation_policy[(0,0,1)] = (1.0, 0.1)
    observation_policy[(0,0,2)] = (0.0, 0.5)

    observation_policy[(0,1,1)] = (0.0,0.5)
    observation_policy[(0,1,2)] = (1.0,0.1)

    observation_policy[(1,0,1)] = (0.0,0.4)
    observation_policy[(1,0,2)] = (1.0,0.2)

    observation_policy[(1,1,1)] = (1.0,0.2)
    observation_policy[(1,1,2)] = (0.0,0.4)

    states = list(set([(B,D) for (B,D, a) in observation_policy.keys() ]))

    dist_rewards = None



    def __init__(self):
        self.playerJustMoved = 0 # dummy root




    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = HiddenStateGame()
        st.playerJustMoved = self.playerJustMoved
        st.assignRandomAction()
        return st

    def DoMove(self, action):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """

        #print "action", action, self.playerJustMoved
        if(self.playerJustMoved == 0):
            self.playerJustMoved = 1

        elif(self.playerJustMoved == 1):
            self.playerJustMoved = 2
            self.action = action
        elif(self.playerJustMoved == 2):
            self.playerJustMoved = 3
        #print self.playerJustMoved
        #print "sdfsadf", self.playerJustMoved



    def isChance(self):
        return (self.playerJustMoved == 0)

    def assignRandomAction(self):
        ## pick a random guy playing
        state = random.choice(HiddenStateGame.states)
        ## ask him what he would do
        self.state = state
        state_0 = (state[0], state[1], 1)
        state_1 = (state[0], state[1], 2)

        prob_action, _ = HiddenStateGame.observation_policy[state_0]
        prob_action_other, _ = HiddenStateGame.observation_policy[state_1]

        dist_actions = [0,0]
        dist_actions[0] = prob_action
        dist_actions[1]  = prob_action_other

        action = self.weighted_choice(dist_actions)



        #HiddenStateGame.dist_rewards = dist_rewards


        #print dist_actions, action
        #print action
        #print action
        #print dist_actions, action
        self.action = action
        #print "After clone", self.state, self.action, dist_actions, dist_rewards



    def chooseRandomAction(self):
        #print self.action, "adfsalkdfsjf"
        #print self.action
        return self.action
        #return self.action


    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        #print self.playerJustMoved

        if(self.isChance()):
            return [0,1]

        if(self.playerJustMoved < 2):
            return [0,1]
        else:
            return []


    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of player.
        """
        state = self.state
        action = self.action

        state_action, reward_dist = HiddenStateGame.observation_policy[(state[0], state[1], action+1)]
        dist_rewards = [0,0]
        dist_rewards[0] = 1.0-reward_dist
        dist_rewards[1] = reward_dist

        result = float(self.weighted_choice(dist_rewards))

        return result


    def weighted_choice(self, choices):

        total = sum(w for w in choices)
        r = random.uniform(0, total)
        upto = 0
        for c, w in enumerate(choices):
           if upto + w >= r:
              return c
           upto += w
        assert False, "Shouldn't get here"


    def __repr__(self):
        """ Don't need this - but good style.
        """
        return str(self.action) + " " + str(self.playerJustMoved) + " " + str(HiddenStateGame.dist_rewards)


class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves() # future child nodes
        self.playerJustMoved = state.playerJustMoved # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n


    def AddChanceChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result



    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) \
               + " score:" + str(self.wins/float(self.visits)) +  "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state = rootstate)

    for i in range(itermax):

        #print "iter", "=================================="
        node = rootnode
        state = rootstate.Clone()
        # if(node.visits > 0):
        #     print node.wins/float(node.visits)


        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            if(state.isChance()):
                m = state.chooseRandomAction()
                state.DoMove(m)

                node = node.childNodes[m]
                #print "chance", m
            else:
                #print "select"
                node = node.UCTSelectChild()
                state.DoMove(node.move)

        #print "finisehd with untried actions"

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)

            if(state.isChance()):
                m = state.chooseRandomAction()
                state.DoMove(m)
            else:
                m = random.choice(node.untriedMoves)
                state.DoMove(m)
            if(m in node.untriedMoves):
                node = node.AddChild(m,state) # add child and descend tree
        #print "finished with choice actions"

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal

            state.DoMove(random.choice(state.GetMoves()))

        #print "finished with simulation"

        # Backpropagate
        score = state.GetResult(node.playerJustMoved)
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(score) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    if (verbose): print rootnode.TreeToString(0)
    else: print rootnode.ChildrenToString()

    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
                
def playHiddenGame():
    state = HiddenStateGame()
    #print state.action
    m = UCT(rootstate = state, itermax = 10000, verbose = True)

if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players. 
    """
    playHiddenGame()

            
                          
            

