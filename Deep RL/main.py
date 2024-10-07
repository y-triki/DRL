# main.py
from sarsa_agent import SARSAAgent
from environments import TicTacToe

env = TicTacToe()
agent = SARSAAgent(env)
agent.train(episodes=1000)

# Test agent
state = env.reset()
done = False
while not done:
    action = agent.select_action(state)
    state, reward, done = env.step(action)
    print(f"Action: {action}, Reward: {reward}")
