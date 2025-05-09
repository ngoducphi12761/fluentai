import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical

class PPOAgent(nn.Module):
    def __init__(self, state_dim, action_dim, lr=0.0003, gamma=0.99, eps_clip=0.2):
        super(PPOAgent, self).__init__()
        self.gamma = gamma
        self.eps_clip = eps_clip

        self.actor = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Softmax(dim=-1)
        )

        self.critic = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=lr)

    def forward(self, state):
        action_probs = self.actor(state)
        state_value = self.critic(state)
        return action_probs, state_value

    def select_action(self, state):
        state = torch.FloatTensor(state)
        action_probs, _ = self.forward(state)
        dist = Categorical(action_probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)
