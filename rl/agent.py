# fluentai/rl/agent.py
from stable_baselines3 import PPO
from rl.environment import CFDSimEnv
from rl.config import RL_MODEL_PATH

def train_agent():
    env = CFDSimEnv()
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    model.save(RL_MODEL_PATH)
