# random_agent.py
import numpy as np

class RandomAgent:
    def __init__(self, environment):
        self.env = environment
    
    def select_action(self, state):
        """ Select a random action from available actions. """
        actions = self.env.available_actions()
        action_index = np.random.choice(len(actions))
        return actions[action_index]

# Example usage:
# env = TicTacToe()
# agent = RandomAgent(env)
# state = env.reset()
# action = agent.select_action(state)
