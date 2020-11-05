# Maxwell Carmichael, 10/10/2020

import time
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI

class IterativeAI:
    def __init__(self, ai, time):
        self.AI = ai
        self.maximum_time = time # seconds

    def choose_move(self, board):
        # Figured out how to do this on Andrew Clark's answer on stack exchange
        timeout = time.time() + self.maximum_time # in reality this won't suffice. I actually have to stop choose_move during its call.
        best_move = None # the move to return

        self.AI.depth = 0

        while True:
            if time.time() > timeout:
                return best_move

            self.AI.depth += 1

            print("Iteration with depth: " + str(self.AI.depth))
            move = self.AI.choose_move(board)
            best_move = move



if __name__ == '__main__':
    ai = IterativeAI(MinimaxAI(), 10)
    ai.choose_move()
