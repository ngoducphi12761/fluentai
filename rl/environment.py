import gymnasium as gym
from gymnasium import spaces
import numpy as np

class CFDSimEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(3)  # 0=k-epsilon, 1=k-omega, 2=LES
        self.observation_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.random.rand(4)
        info = {}
        return self.state, info

    def step(self, action):
        reward = np.random.choice([1, -1])  # Placeholder reward
        terminated = True
        truncated = False
        info = {}
        return self.state, reward, terminated, truncated, info