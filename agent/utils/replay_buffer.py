import random
from collections import deque

import torch


class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.memory = deque(maxlen=capacity)
        
    def push(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def sample(self, batch_size, device):
        batch = random.sample(self.memory, batch_size)
        
        states, actions, rewards, next_states, dones = zip(*batch)
        
        state_batch = torch.cat(states).to(device)
        next_state_batch = torch.cat(next_states).to(device)
        
        action_batch = torch.tensor(actions, dtype=torch.long).to(device)
        reward_batch = torch.tensor(rewards, dtype=torch.float32).to(device)
        done_batch = torch.tensor(dones, dtype=torch.float32).to(device)
        
        return state_batch, action_batch, reward_batch, next_state_batch, done_batch
        
    def __len__(self):
        return len(self.memory)
