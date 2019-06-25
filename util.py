"""Useful functions for the Game.

Authors:
    Gael Colas
"""

import numpy as np
import ujson as json
import threading

def input_thread(inputs_list):
    """Save the user inputs.
    """
    c = input()
    inputs_list.append(c)
    
def display_info(n_sim, highscore, commands_filename):
    """Display the current highscore and the current highscore.
    
    Args:
        'n_sim' (int): number of simulations played
        'highscore' (tuple of int, (human, AI)): the best score achieved by a human and an AI
        'commands_filename' (str): filename of the text file listing the commands used in the game
    """
    simulation_text = "Simulations: {}\n".format(n_sim)
    
    score_text = "Highscore Human: {}\nHighscore AI: {}\n".format(*highscore)
     
    with open(commands_filename, "r") as commands_file:
        commands_text = commands_file.read()
            
    input_text = "\nENTER COMMAND:\n"
   
    print(simulation_text, score_text, commands_text, input_text, sep='\n')
    
    
def handle_user_command(gym):
    """Handle user commands.
    
    Args:
        'gym' (Gym): agent training gym
        
    Remarks:
        The possible commands are specified in "commands.txt".
    """
    # list of user commands
    inputs_list = gym.inputs_list
    
    if not inputs_list:
        return
        
    # execute the last command
    c = inputs_list[-1]
    
    if c == "s":
        save_agent(gym.agent, gym.args.save_filename)
    elif c == "q":
        gym.agent.dino.quit()
    elif c == "h":
        gym.isHuman = True
    elif c == "a":
        gym.isHuman = False    
       
    # reset the list of user commands
    gym.inputs_list = []
    # launch a new thread
    threading.Thread(target=input_thread, args=(gym.inputs_list,)).start()

    
def load_highscore(highscore_filename):
    """Load the highscore stored in a text file.
    
    Args:
        'highscore_filename' (str): filename of the highscore text file
    
    Return:
        'highscore' (tuple of int, (human, AI)): the best score achieved by a human and an AI
    """
    human_score, ai_score = -1, -1
    
    # try opening the highscore file
    try:
        highscore_file = open(highscore_filename, "r")
        
        # if the file exists, read the score from it
        for line in highscore_file.readlines():
            name, score = line.split(" ")
            
            if "human" in name:
                human_score = int(score)
            elif "ai" in name:
                ai_score = int(score)
        
    except FileNotFoundError:
        print("No highscore file '{}' found. Creating a new one...".format(highscore_filename))
        open(highscore_filename, "w")
    
    highscore = [human_score, ai_score]
    
    return highscore

def update_score(highscore, highscore_filename):
    """Update the highscore text file with the new highscore.
    
    Args:
        'highscore' (tuple of int, (human, AI)): the best score achieved by a human and an AI
        'highscore_filename' (str): filename of the highscore text file
    """
    with open(highscore_filename, "w") as highscore_file:
        highscore_file.write("human {}\nai {}".format(highscore[0], highscore[1]))
        
def save_agent(agent, out_filename):
    """Save the agent parameters to a JSON file.
    
    Args:
        'agent' (AIAgent): AI agent to save
        'out_filename' (str): name of the output file
    """
    with open(out_filename, "w") as out_file:
        json.dump(agent.mdp_data, out_file)
    
    print("The AI agent has been saved to: {}".format(out_filename))
    
def load_agent(agent, in_filename):
    """Load the saved agent parameters from a JSON file.
    
    Args:
        'agent' (AIAgent): AI agent to load the parameters into
        'in_filename' (str): name of the input file
    """
    with open(in_filename, "r") as in_file:
        mdp_data = json.load(in_file)
    
    # convert all the list to np.arrays
    agent.mdp_data = {
        'num_states': mdp_data['num_states'],
        'state_discretization': [np.array(states_list) for states_list in mdp_data['state_discretization']],
        'transition_counts': np.array(mdp_data['transition_counts']),
        'transition_probs': np.array(mdp_data['transition_probs']),
        'reward_counts': np.array(mdp_data['reward_counts']),
        'reward': np.array(mdp_data['reward']),
        'value': np.array(mdp_data['value'])
    }
    print("The AI agent has been loaded from: {}".format(in_filename))
