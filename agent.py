"""AI agent using RL to beat the game.

Authors:
    Gael Colas
    Sanyam Mehra (CS229 teaching staff): HW4 solutions
"""

import numpy as np

# handled type of obstacles
OBSTACLE_TYPES = {'CACTUS_SMALL': 0, 'CACTUS_LARGE': 1, 'PTERODACTYL': 2}
MAX_CONSECUTIVE_OBS = 3
PTERODACTYL_HEIGHTS = [50, 75, 100]

class AIAgent:
    """AI agent controlling the Dino.
    The AI agent is trained by Reinforcement Learning.
    Every time the agent finishes a simulation, he builds an approximate Markov Decision Process based on the transition and the reward observed.
    At the end of the simulation, he computes the approximated value function through Value Iteration.
    This value function is then used to choose the best actions of the next simulation.
    
    Attributes:
        'args' (ArgumentParser): parser gethering all the Game parameters
        'gamma' (float): discount factor
        'eps' (float): epsilon-greedy coefficient
        'mdp' (MDP): approximate MDP current parameters
        
        'dino' (Dino): Dino controller
        
        'state' (dict): the current state of the Dino
        'action' (int): the current action 
                action = 1 if 'jumping', 2 if 'ducking', 0 otherwise
    """
    
    def __init__(self, args, dino):
        super(AIAgent).__init__()
        
        # RL parameters
        self.args = args
        self.gamma = args.gamma
        self.eps = args.eps
        self.tolerance = args.tolerance
        # initialize the approximate MDP parameters
        self.initialize_mdp_data()
        
        # Dino controller
        self.dino = dino
        
        # current state and action
        self.state = dino.get_state()
        self.action = 0

    def get_reward(self, isCrashed, obsPassed=False):
        """Reward function.
        
        Args:
            'isCrashed' (bool): whether the Game has been failed at the current state
            'obsPassed' (bool): whether an obstacle has been passed
            
        Return:
            'reward' (float): reward earned in the current state
            
        Remarks:
            Losing the game: -100
            Being alive: 0
        """
        if isCrashed:
            reward = -1000
        elif obsPassed:
            reward = +10
        else:
            reward = 0
        
        return reward
        
    def reset(self):
        """Reset the simulation parameters.
        
        Record the last transition.
        Update the approximated MDP parameters.
        Make the strategy more greedy.
        Start a new simulation.
        """    
        # record the last transition information
        self.set_transition() 
        
        # update the approximate MDP with the simulation observations
        self.update_mdp_parameters()
        
        # make the algorithm more greedy
        self.eps += 0.01
        
        # start a new simulation
        self.dino.start()
        
        # reset the state
        self.state = self.dino.get_state()
        
    def choose_action(self):
        """Choose the next action with an Epsilon-Greedy exploration strategy.
        """               
        # epsilon-greedy strategy
        if np.random.rand() < self.eps: 
            # choose greedily the best action
            self.action = self.best_action(self.state)
        else:
            # choose random action
            self.action = (np.random.rand() < 0.5)*1
                        
        if self.action == 0:
            self.dino.run()
        elif self.action == 1:
            self.dino.jump()
        elif self.action == 2:
            self.dino.duck()
            
    def best_action(self, state):
        """Choose the next action (0, 1 or 2) that is optimal according to your current 'mdp_data'. 
        When there is no optimal action, return 0 has "do nothing" is more frequent.
        
        Args:
            'state' (dict): current state of the Dino
            
        Return:
            'action' (int, 0 or 1): optimal action in the current state according to the approximate MDP
        """
        # get the index of the closest discretized state
        s = self.get_closest_state_idx(state)
        
        # value function if taking each action in the current state 
        score_nothing = self.mdp_data['transition_probs'][s, 0, :].dot(self.mdp_data['value'])
        score_jump = self.mdp_data['transition_probs'][s, 1, :].dot(self.mdp_data['value'])
        
        # DUCK ACTION NOT USED: CAN BEAT GAME WITHOUT DUCKING
        #score_duck = self.mdp_data['transition_probs'][s, 2, :].dot(self.mdp_data['value']) 

        # best action in the current state
        action = (score_jump > score_nothing)*1
        
        return action
        
    def get_closest_state_idx(self, state, isFail=False):
        """Get the index of the closest discretized state.
        
        Args:
            'state' (dict): the current state of the Dino
            'isFail' (bool): whether the Game is failed
            
        Return:
            'ind' (int): index of the closest discretized state
            
        Remarks:
            The state of the Dino is defined by: the time to the next obstacle (dt), the height of the dino (y), and if the obstacle is a Pterodactyl, its flight level.
            State 0 is a FAIL state ; State 1 is a NO_OBSTACLE state.
        """
        # discretized state
        dt_s, dy_s, dy_pter_s = self.mdp_data["state_discretization"]
                
        if not state: # no obstacle created yet
            return 1
        
        if state['type'] == "PTERODACTYL":
            i = np.argmin(abs(dy_pter_s - state['config']))
        else:
            i = dy_pter_s.size
        
        # closest discretized state indices
        j = np.argmin(abs(dt_s - state['dt']))
        k = np.argmin(abs(dy_s - state['y']))
        
        return (not isFail)*(i*dt_s.size*dy_s.size + j*dy_s.size + k + 2)
        
    def initialize_mdp_data(self):
        """Save a attributes 'mdp_data' that contains all the parameters defining the approximate MDP.
        
        Parameters:
            'num_states' (int): the number of discretized states.
                    num_states = (1 + n_pter_levels ) * n_t * n_y + 2
        
        Initialization scheme:
            - Value function array initialized to 0
            - Transition probability initialized uniformly: p(x'|x,a) = 1/num_states 
            - State rewards initialized to 0
        """
        
        num_states = (1 + 1*len(PTERODACTYL_HEIGHTS) )*self.args.n_t*self.args.n_y + 2
        
        # state discretization
        dt_s = np.linspace(0, self.args.max_dt, self.args.n_t)
        dy_s = np.linspace(0, self.args.max_y, self.args.n_y)
        dy_pter_s = np.array(PTERODACTYL_HEIGHTS).astype(float)

        # mdp parameters initialization
        transition_counts = np.zeros((num_states, 2, num_states))
        transition_probs = np.ones((num_states, 2, num_states)) / num_states
        reward_counts = np.zeros((num_states, 2))
        reward = np.zeros(num_states)
        value = np.zeros(num_states)

        self.mdp_data = {
            'num_states': num_states,
            'state_discretization': [dt_s, dy_s, dy_pter_s],
            'transition_counts': transition_counts,
            'transition_probs': transition_probs,
            'reward_counts': reward_counts,
            'reward': reward,
            'value': value
        }
        
    def set_transition(self):
        """Update the approximate MDP with the given transition.
        """
        # whether the Game has been failed at the new state
        isCrashed = self.dino.is_crashed()
        # get the new state
        new_state = self.dino.get_state()
        # whether an obstacle has been passed
        obsPassed = new_state['dx'] > self.state['dx']
        # get the previous state reward
        reward = self.get_reward(isCrashed, obsPassed)
        # store the given transition
        self.update_mdp_counts(self.state, self.action, new_state, reward, isCrashed)
        
        # update the current state
        self.state = new_state
        
    def update_mdp_counts(self, state, action, new_state, reward, isCrashed):
        """Update the transition counts and reward counts based on the given transition.
        
        Record for all the simulations:
            - the number of times `state, action, new_state` occurs ;
            - the rewards accumulated for every `new_state`.
        
        Args:
            'state' (np.array, [y, dx, dy]): previous state of the Bird
            'action' (int, 0 or 1): last action performed
            'new_state' (np.array, [y, dx, dy]): new state after performing the action in the previous state
            'reward' (float): reward observed in the previous state
        """
        # get the index of the closest discretized previous and new states
        s = self.get_closest_state_idx(state, False)
        new_s = self.get_closest_state_idx(new_state, isCrashed)
                
        # update the transition and the reward counts
        self.mdp_data['transition_counts'][s, action, new_s] += 1
        self.mdp_data['reward_counts'][new_s, 0] += reward
        self.mdp_data['reward_counts'][new_s, 1] += 1

    def update_mdp_parameters(self):
        """Update the estimated MDP parameters (transition and reward functions) at the end of a simulation.
        Perform value iteration using the new estimated model for the MDP.

        Remarks:
            Only observed transitions are updated.
            Only states with observed rewards are updated.
        """
        temp = self.mdp_data['transition_probs'].copy()
        # update the transition function
        total_num_transitions = np.sum(self.mdp_data['transition_counts'], axis=-1)
        visited_state_action_pairs = total_num_transitions > 0
        self.mdp_data['transition_probs'][visited_state_action_pairs] = self.mdp_data['transition_counts'][visited_state_action_pairs] / total_num_transitions[visited_state_action_pairs, np.newaxis]

        # update the reward function
        visited_states = self.mdp_data['reward_counts'][:, 1] > 0
        self.mdp_data['reward'][visited_states] = self.mdp_data['reward_counts'][visited_states, 0] / self.mdp_data['reward_counts'][visited_states, 1]

        # update the value function through Value Iteration
        while True:           
            # Q(_,a) for the different actions
            value_nojump = np.dot(self.mdp_data['transition_probs'][:,0,:], self.mdp_data['value'])
            value_jump = np.dot(self.mdp_data['transition_probs'][:,1,:], self.mdp_data['value'])

            # Bellman update
            new_value = self.mdp_data['reward'] + self.gamma * np.maximum(value_nojump, value_jump)
            
            # difference with previous value function
            max_diff = np.max(np.abs(new_value - self.mdp_data['value']))

            self.mdp_data['value'] = new_value
            
            # check for convergence
            if max_diff < self.tolerance:
                break
