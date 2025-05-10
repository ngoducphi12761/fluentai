import torch
import numpy as np
from agent import PPOAgent
from environment import FluentAIEnv

# Initialize environment and agent
env = FluentAIEnv()
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n
agent = PPOAgent(state_dim, action_dim)

num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        action, log_prob = agent.select_action(state)
        next_state, reward, done, _ = env.step(action)

        # Calculate advantage (A2C approach)
        _, state_value = agent(state)
        _, next_state_value = agent(next_state)
        advantage = reward + agent.gamma * next_state_value.item() - state_value.item()

        # Optimize model
        agent.optimizer.zero_grad()
        loss = -log_prob * advantage  # Policy gradient loss
        loss.backward()
        agent.optimizer.step()

        state = next_state
        total_reward += reward

    print(f"Episode {episode + 1}: Total Reward = {total_reward}")
