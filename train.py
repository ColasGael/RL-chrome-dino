"""Train the AI agent.

Authors:
    Gael Colas
"""

import threading

from util import *
from args import get_game_args
from dino import Dino
from agent import AIAgent

class Gym:
    """'Gym' class: train the AI agent
    
    Attributes:
        'args' (ArgumentParser): parser gethering all the Game parameters
        'dino' (Dino): Dino controller
        
        'highscore' (tuple of int, (human, AI)): the best score achieved by a human and an AI
        'isHuman' (bool): whether a human or an AI is playing the game
        't' (int): number of time steps since the beginning of the game
        
        'agent' (AIAgent, default=None): AI agent playing the game
    """
    
    def __init__(self, args):
        super(Gym).__init__()
        self.args = args
                
        # environment parameters
        self.dino = Dino(args)
        
        # game parameters
        self.highscore = load_highscore(args.highscore_filename)
        self.t = 0
        
        # to play with an AI
        self.isHuman = (args.agent == "human")
        if not self.isHuman:
            self.agent = AIAgent(args, self.dino)
            # load saved parameters
            if self.args.load_save:
                load_agent(self.agent, self.args.save_filename)
                
        # listen to user inputs
        self.inputs_list = []
        threading.Thread(target=input_thread, args=(self.inputs_list,)).start()

    def step(self):
        """Play one time step in the game.
        """        
        # take an action
        self.agent.choose_action()     
        
        # feed the transition information to the agent
        self.agent.set_transition() 
        
        # update the number of time steps
        self.t += 1
    
    def play(self):
        """Play games continuously.
        """
        # display command info
        display_info(self.dino.get_n_sim(), self.highscore, self.args.commands_filename)
        handle_user_command(self)
        
        # start the first game
        self.dino.start()
        
        while True:              
            # check if the game is not failed
            if not self.dino.is_crashed():                
                if not self.isHuman: 
                    # check if the game is not paused
                    if not self.dino.is_playing() and self.args.play_bg:
                        self.dino.game.resume()
                    
                    # take a step if the AI is playing
                    if self.dino.is_playing():
                        self.step()

            # otherwise launch a new game
            else:
                # reset the number of steps
                self.t = 0
                
                # current score
                score = self.dino.get_score()
                # check if the highscore is beaten
                human_score = max(score * self.isHuman, self.highscore[0])
                ai_score = max(score * (not self.isHuman), self.highscore[1])
                # update the highscore
                self.highscore = (human_score, ai_score)
                update_score(self.highscore, self.args.highscore_filename)
                
                # display command info
                display_info(self.dino.get_n_sim(), self.highscore, self.args.commands_filename)
                handle_user_command(self)

                if not self.isHuman: 
                    # save the last simulation
                    self.agent.reset()
                else: 
                    self.dino.start()
                

if __name__ == '__main__':
    # get arguments needed to play the Game
    args = get_game_args()
    # launch the game
    Gym(args).play()
    
