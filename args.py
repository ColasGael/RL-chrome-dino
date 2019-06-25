"""Command-line arguments for the Game.

Authors:
    Gael Colas
"""

import argparse


def get_game_args():
    """Get arguments needed to play the Game."""
    
    parser = argparse.ArgumentParser('Get arguments needed to play the Game.')
    
    # add arguments needed to interact with the JavaScript game
    add_env_args(parser)
    # add arguments defining the simulation run
    add_sim_args(parser)
    # add arguments relative to the RL algorithm     
    add_RL_args(parser)
    
    parser.add_argument('--commands_filename',
                        type=str,
                        default="commands.txt",
                        help="Filename of the text file listing the commands used in the game.")
    parser.add_argument('--highscore_filename',
                        type=str,
                        default="highscore.txt",
                        help="Filename of the text file where the highscores are stored.")
    parser.add_argument('--agent',
                        type=str,
                        default="ai",
                        choices=("human", "ai"),
                        help="Whether to use a human or an AI agent.")
                        
    args = parser.parse_args()

    return args

def add_env_args(parser):
    """Add arguments needed to interact with the JavaScript game."""
    parser.add_argument('--game_url',
                        type=str,
                        default='chrome://dino',
                        help="Url to access the game.")
    parser.add_argument('--chrome_driver_path',
                        type=str,
                        default='./chromedriver.exe',
                        help="Path to the Chrome driver for Selenium.")
    parser.add_argument('--dino_sprite_1x',
                        type=str,
                        default='',
                        help="Path to the custom Dino sprite (LDPI version).")                        
    parser.add_argument('--dino_sprite_2x',
                        type=str,
                        default='',
                        help="Path to the custom Dino sprite (HDPI version).")     

def add_sim_args(parser):
    """Add arguments defining the simulation run.
    By default the parameters are the one from the original game.
    """
    parser.add_argument('--initial_speed',
                        type=float,
                        default=6.,
                        help="Initial speed of the dino.")
    parser.add_argument('--max_speed',
                        type=float,
                        default=13.,
                        help="Maximum speed of the dino.")
    parser.add_argument('--acceleration',
                        type=float,
                        default=0.001,
                        help="Speed increment as the dino runs.")
    parser.add_argument('--clear_time',
                        type=int,
                        default=0, #3000,
                        help="How long the horizon is free of obstacles in the beginning.")
    parser.add_argument('--play_bg',
                        type=bool,
                        default=True,
                        help="Whether to let the AI train in the background.")
                        

def add_RL_args(parser):
    """Add arguments relative to the Reinforcement Learning algorithm."""
    parser.add_argument('--dt',
                        type=float,
                        default=0.01,
                        help="Time discretization between two successive actions (in s).")
    parser.add_argument('--n_t',
                        type=int,
                        default=20,
                        help="Discretization of dt = number of points on time-axis.")
    parser.add_argument('--max_dt',
                        type=int,
                        default=1.,
                        help="Upper bound on dt for discretization.")
    parser.add_argument('--n_v',
                        type=int,
                        default=8,
                        help="Discretization of dino speed = number of points on velocity-axis.")
    parser.add_argument('--gamma',
                        type=float,
                        default=0.995,
                        help="Discount factor.")
    parser.add_argument('--eps',
                        type=float,
                        default=1.,
                        help="Epsilon-greedy coefficient.")
    parser.add_argument('--tolerance',
                        type=float,
                        default=0.01,
                        help="Convergence criterium for Value Iteration.")
    parser.add_argument('--save_filename',
                        type=str,
                        default='ai_save.json',
                        help="Name of the JSON file saving the agent parameters.")
    parser.add_argument('--load_save',
                        type=bool,
                        default=False,
                        help="Whether to load the agent parameters from the saved file.")
     