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
        
        return obstacle_state
        
    def is_playing(self):
        """Check if the game is playing (ie not paused and not game over). 
        """
        return self.game.get_playing()
        
    def is_crashed(self):
        """Check if the agent has crashed on an obstacle.
        """
        return self.game.get_crashed()