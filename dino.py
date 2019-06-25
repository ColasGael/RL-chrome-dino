"""Control the Dino character.

Authors:
    Gael Colas
"""

import time

from game import Game


class Dino:
    """'Dino' class: control the Dino character.
    
    Attributes:
        'game' (Game): interface between Python and Chrome Javascript
    """
    def __init__(self, args):
        super(Dino).__init__()
        
        self.dt = args.dt
        self.game = Game(args)
        self.start()
        
    def start(self):
        """Start a game.
        
        Remarks:
            For the first game: jump to start the game.
        """
        if self.game.get_n_sim() == 0: # first game
            self.jump()
        else: # next games
            self.game.restart()
    
    def run(self):
        """Do nothing (run).
        """
        time.sleep(self.dt)
    
    def jump(self):
        """Make the Dino jump.
        """
        self.game.press_up()
        time.sleep(self.dt)
        
    def duck(self):
        """Make the Dino duck.
        """
        self.game.set_duck(self.dt)
        
    def get_state(self):
        """Get the state of the Dino.
        """
        # current dino state
        dino_state = self.game.get_dino_state()
        # next obstacle state
        obstacle_state = self.game.get_obstacle()
          
        if not obstacle_state: # no obstacle created yet
            return None
          
        # combined state
        obstacle_state.update(dino_state)
        
        obstacle_state['dt'] = obstacle_state['dx'] / (100*obstacle_state['speed'])
        
        return obstacle_state
        
    def is_playing(self):
        """Check if the game is playing (ie not paused and not game over). 
        """
        return self.game.get_playing()
        
    def is_crashed(self):
        """Check if the agent has crashed on an obstacle.
        """
        return self.game.get_crashed()
    
    def get_score(self):
        """Get the current score.
        
        Return:
            'score' (int): current score
        """
        score = self.game.get_score()
        return score
        
    def get_n_sim(self):
        """Get the current score.
        
        Return:
            'n_sim' (int): number of simulations played
        """
        n_sim = self.game.get_n_sim()
        return n_sim
        
    def quit(self):
        """Quit the game.
        """
        self.game.end()