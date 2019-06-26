# RL-chrome-dino
Reinforcement Learning to train an AI agent to play Dino Run on Chrome.

## RL algorithm

The state is composed of: the time to the next obstacle (dt), the height of the dino (y), and if the obstacle is a Pterodactyl, its flight level.

The AI agent explores its environment with an increasingly greedy Epsilon-Greedy scheme.

At the end of each simulation, it updates its approximation of the underlying Markov Decision Process. The state space is descretized.
Then it solves for the optimal value function via Value Iteration.

The best action in a given state is the one that yields the largest value function in this state.

## Performances

After 100 simulations (successive games), the AI achieves a highscore around: 1500.

However the training is unstable.

## How to let the AI play?

To let the AI agent learn, go at the root of the repository and run: `python train.py`

If you want to load a pretrained agent, add the following flag: `python train.py --load_save True`

You can also save your own agent's state by entering "S" in the command line during the simulation.

## How to customize?

From an idea from BillehBawb, the sprites (for the dino animation and the obstacles) used in the game are customizable. 

If you want to use your own:
- watch BillehBawb [tutorial](https://www.youtube.com/watch?v=jwCXchvJ83w) to see how to create a custom sprite for the game ;
- put the new sprite as a JPG file in the "sprite" directory ;
- update the "dino_sprite" argument in the "args.py" file with the new sprite filename.

You can also modify "args.py" to change the parameters of the simulation:
- the Simulation hyperparameters: by default they are set to their value in the original game ;
- the Reinforcement Learning hyperparameters.

## Requirements

If you want to code in a conda environment, run the following commands in the command line:
```
conda create -n dino pip
conda activate dino
```

To install all the necessary packages, go at the root of the repository and run: `pip install -r requirements.txt`

To deactivate the environment, run: `conda deactivate dino`

## Acknowledgement

The interface between Python and Chrome Javascript is implemented with the Selenium package. 
The starter code comes from Ravi Munde's own attempt at training an AI agent to play Dino Run. 
The code from his project can be found in this [repository](https://github.com/ravi72munde/Chrome-Dino-Reinforcement-Learning).
