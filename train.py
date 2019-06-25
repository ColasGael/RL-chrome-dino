"""Train the AI agent.

Authors:
    Gael Colas
"""

#from util import *
from args import get_game_args
from dino import Dino
from agent import AIAgent

class Gym:
    """'Gym' class: train the AI agent
    
    Attributes:
        'args' (ArgumentParser): parser gethering all the Game parameters
        'dino' (Bird, default=None): Dino controller
        
        't' (int): number of time steps since the beginning of the game
        
        'agent' (AIAgent, default=None): AI agent playing the game
    """
    
    def __init__(self, args):
        super(Gym).__init__()
        self.args = args
        
        # environment parameters
        self.dino = Dino(args)
        
        # game parameters
        self.t = 0
        
        # to play with an AI
        self.isHuman = (args.agent == "human")
        if not self.isHuman:
            self.agent = AIAgent(args, self.dino)
            # load saved parameters
            if self.args.load_save:
                load_agent(self.agent, self.args.save_filename)
    
    def 
    
    def step(self):
        """Play one time step in the game.
        """        
        # take an action
        self.agent.choose_action()     
        
        # feed the transition information to the agent
        self.agent.set_transition(isCrashed) 
        
        # update the number of time steps
        self.t += 1
    
                
    def play(self):
        # start the first game
        self.dino.start()
        
        while True:
            if self.dino.is_playing():
                self.step()
            else:
                self.agent.reset()
    

if __name__ == '__main__':
    # get arguments needed to play the Game
    args = get_game_args()
    # launch the game
    Gym(args).play()
    
