import math
import random

import torch
import torch.nn.functional as F
import torch.optim as optim

from environment.game_env import GameEnv
# Assuming you saved your DuelingDQN class in a file named model.py
from model.dueling_dqn import DuelingDQN
from utils.board_to_tensor import board_to_tensor
from utils.replay_buffer import ReplayBuffer

# --- Hyperparameters ---
BATCH_SIZE = 128
GAMMA = 0.99             # Discount factor (how much it cares about future rewards vs immediate)
EPS_START = 1.0          # Starting exploration rate
EPS_END = 0.05           # Final exploration rate
EPS_DECAY = 20000        # How many moves it takes to decay epsilon
TARGET_UPDATE = 1000     # Sync Target Network every 1000 moves
LR = 1e-4                # Learning Rate
MEMORY_SIZE = 100000     # Replay Buffer capacity
NUM_EPISODES = 5000      # Total games to play

# Setup Device (CPU for your Ryzen, automatically swaps to CUDA for the RTX 4050)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training on device: {device}")

# --- Initialization ---
env = GameEnv(jar_path="../2048/target/2048-1.0-SNAPSHOT.jar")
memory = ReplayBuffer(capacity=MEMORY_SIZE)

# Initialize Both Networks
policy_net = DuelingDQN().to(device)
target_net = DuelingDQN().to(device)
target_net.load_state_dict(policy_net.state_dict()) # Clone weights
target_net.eval() # Target network does not train!

optimizer = optim.Adam(policy_net.parameters(), lr=LR)
steps_done = 0

# Map AI output (0,1,2,3) to Java commands
ACTION_MAP = {0: 'W', 1: 'S', 2: 'A', 3: 'D'}

def select_action(state_tensor):
    global steps_done
    # Epsilon decay math
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    
    if random.random() > eps_threshold:
        # EXPLOIT: Use the network
        with torch.no_grad(): # Don't track gradients for picking moves
            # Get Q-values for all 4 moves, pick the index with the highest value
            return policy_net(state_tensor.to(device)).max(1)[1].view(1, 1).item()
    else:
        # EXPLORE: Pick a random move
        return random.randrange(4)

def optimize_model():
    if len(memory) < BATCH_SIZE:
        return # Don't train until buffer is full enough
        
    # Sample a batch from memory
    states, actions, rewards, next_states, dones = memory.sample(BATCH_SIZE, device)
    
    # 1. Calculate Current Q Values
    # policy_net(states) outputs [Batch, 4]. gather() picks the specific action we actually took.
    state_action_values = policy_net(states).gather(1, actions.unsqueeze(1))
    
    # 2. Calculate Target Q Values
    with torch.no_grad():
        # Get max Q value for the next state from the TARGET network
        next_state_values = target_net(next_states).max(1)[0]
        
    # The Bellman Equation: Expected = Reward + (Gamma * Next State Value * (1 - Game Over))
    expected_state_action_values = rewards + (GAMMA * next_state_values * (1 - dones))
    
    # 3. Calculate Loss (Huber Loss is incredibly stable for RL)
    loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))
    
    # 4. Backpropagation
    optimizer.zero_grad()
    loss.backward()
    # Gradient clipping prevents the network from "exploding" mathematically
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()

# --- Main Training Loop ---
for episode in range(NUM_EPISODES):
    board_2d = env.reset()
    state = board_to_tensor(board_2d)
    total_reward = 0
    
    while True:
        # 1. Pick an action
        action_idx = select_action(state)
        java_command = ACTION_MAP[action_idx]
        
        # 2. Execute action in Java
        next_board_2d, reward, done = env.step(java_command)
        total_reward += reward
        next_state = board_to_tensor(next_board_2d)
        
        # 3. Store in Memory
        memory.push(state, action_idx, reward, next_state, done)
        state = next_state
        
        # 4. Train the network one step
        optimize_model()
        
        # 5. Sync Target Network
        if steps_done % TARGET_UPDATE == 0:
            target_net.load_state_dict(policy_net.state_dict())
            
        if done:
            print(f"Episode {episode} | Score: {total_reward} | Epsilon: {EPS_END + (EPS_START - EPS_END) * math.exp(-1. * steps_done / EPS_DECAY):.3f}")
            break

env.quit()
