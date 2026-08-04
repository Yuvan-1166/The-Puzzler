import random

import numpy as np
from tqdm import tqdm

from environment.game_env import GameEnv


class BaseLineAI:

    def __init__(self):
        self.env = GameEnv(jar_path="../2048/target/2048-1.0-SNAPSHOT.jar")
        self.moves = ["W", "A", "S", "D"]
        self.scores = []
        self.max_tile = []

    def random_agent(self, n_game=100):
        
        for _ in tqdm(range(n_game)):
            board = self.env.reset()
            game_over = False
            total_score = 0
            while not game_over:
                move = random.choice(self.moves)
                board, reward, game_over = self.env.step(move)
                total_score += reward

            self.scores.append(total_score)
            self.max_tile.append(np.max(board))
        self.env.quit()

        print(f"Random Agent's Performance for {n_game} games")
        
        print(f"Average Score: {np.mean(self.scores)}\nMax Score: {np.max(self.scores)}\nMin Score: {np.min(self.scores)}")

        tiles, count = np.unique(self.max_tile, return_counts=True)
        tile_count = dict(zip(tiles, count))
        print(f"Max Tile Frequency {tile_count}")

if __name__ == '__main__':
    agent = BaseLineAI()

    agent.random_agent(1000)

