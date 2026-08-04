import json
import subprocess


class GameEnv:

    def __init__(self, jar_path="../2048/target/2048-1.0-SNAPSHOT.jar"):
        self.process = subprocess.Popen(
            ['java', '-jar', jar_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        board = self.process.stdout.readline().strip()
        self.current_state = json.loads(board)

    def step(self, move):
        command = json.dumps({"move": move})

        self.process.stdin.write(command + '\n')
        self.process.stdin.flush()

        board = self.process.stdout.readline().strip()
        new_state = json.loads(board)

        reward = new_state['score'] - self.current_state['score']

        self.current_state = new_state

        return self.current_state['board'], reward, self.current_state['isGameOver']

    def reset(self):
        command = json.dumps({"move": "r"})

        self.process.stdin.write(command + '\n')
        self.process.stdin.flush()

        board = self.process.stdout.readline().strip()
        self.current_state = json.loads(board)


        return self.current_state['board']

    def quit(self):
        command = json.dumps({"move": "q"})
        
        self.process.stdin.write(command + '\n')
        self.process.stdin.flush()
        self.process.wait()
