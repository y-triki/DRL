# sarsa_agent.py
import numpy as np
from random_agent import RandomAgent

class SARSAAgent:
    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}  # Q-values for state-action pairs
    
    def get_q_value(self, state, action):
        return self.q_table.get((tuple(state), tuple(action)), 0.0)
    
    def update_q_value(self, state, action, new_q):
        self.q_table[(tuple(state), tuple(action))] = new_q
    
    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return RandomAgent(self.env).select_action(state)  # Exploration
        else:
            actions = self.env.available_actions()
            q_values = [self.get_q_value(state, a) for a in actions]
            return actions[np.argmax(q_values)]  # Exploitation
    
    def train(self, episodes):
        for _ in range(episodes):
            state = self.env.reset()
            action = self.select_action(state)
            done = False
            
            while not done:
                next_state, reward, done = self.env.step(action)
                next_action = self.select_action(next_state)
                q_value = self.get_q_value(state, action)
                next_q_value = self.get_q_value(next_state, next_action)
                td_target = reward + self.gamma * next_q_value
                new_q_value = q_value + self.alpha * (td_target - q_value)
                self.update_q_value(state, action, new_q_value)
                
                state = next_state
                action = next_action
