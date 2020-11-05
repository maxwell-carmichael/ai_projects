# Maxwell Carmichael, 10/10/2020, Modified from CS76 Material

import chess
import math
import random

class MinimaxAI():
    def __init__(self):
        self.depth = 3 # Constant
        self.nodes_visited = 0 # will reset after each move.

        self.random_factor = 0.1 # the percent chance that an as-good move overrides some other move to prevent cycles.
        random.seed(17) # for replicability. i like the number 17.

        # choose best move given a board
    def choose_move(self, board):
        # if it's white's turn, call max. if it's black's turn, call min.
        if board.turn:
            util_action = self.max_value(board, 0)
        else:
            util_action = self.min_value(board, 0)

        move = util_action[1] # action
        print("Move Utility: " + str(util_action[0])) # utility
        print("Maximum Depth: " + str(self.depth))
        print("Nodes visited: " + str(self.nodes_visited))
        self.nodes_visited = 0 # reset
        print("MinimaxAI recommending move " + str(move))

        return move

        # white move. returns a (utility, move) pair
    def max_value(self, board, depth):
        self.nodes_visited += 1 # increment

        if self.cutoff_test(board, depth):
            return (self.material_value_heuristic(board), None)

        v = -math.inf
        util_action = None # the (utility, move) pair to return

        for move in board.legal_moves:
            board.push(move) # make the move

            move_util_action = self.min_value(board, depth + 1)
            if move_util_action[0] > v: # finding maximum utility we can get...
                v = move_util_action[0]
                util_action = (v, move)

            # to prevent loops (always choosing same move), make there be an override possibility for our v
            elif move_util_action[0] == v and random.choices([True, False], cum_weights = [self.random_factor, 1]):
                util_action = (v, move)

            board.pop() # unmake the move

        return util_action

        # black to move. returns a (utility, move) pair
    def min_value(self, board, depth):
        self.nodes_visited += 1

        if self.cutoff_test(board, depth):
            return (self.material_value_heuristic(board), None)

        v = math.inf
        util_action = None # the (utility, move) pair to return

        for move in board.legal_moves:
            board.push(move) # make the move

            move_util_action = self.max_value(board, depth + 1)
            if move_util_action[0] < v: # finding minimum utility we can get...
                v = move_util_action[0]
                util_action = (v, move)

            # to prevent loops (always choosing same move), make there be an override possibility for our v
            elif move_util_action[0] == v and random.choices([True, False], cum_weights = [self.random_factor, 1]):
                util_action = (v, move)

            board.pop() # unmake the move

        return util_action

        # stop iterating if the game is over or if depth limit is reached
    def cutoff_test(self, board, depth):
        return board.is_game_over() or self.depth == depth

    def material_value_heuristic(self, board):
        # win
        if board.is_checkmate():
            # white's turn, so black just checkmated
            if board.turn:
                return -10000
            # black's turn, so white just checkmated
            else:
                return 10000

        # stalemate, insufficient material, etc.
        if board.is_game_over():
            return 0

        # heuristic at depth limit
        map = board.piece_map()
        heuristic = 0 # this heuristic will be for white player

        # loops through all the pieces and adds them to the heuristic
        for square in map:
            piece = map[square]

            val = 0
            if piece.piece_type == 1: # pawn
                val = 1
            elif piece.piece_type == 2 or piece.piece_type == 3: # knight, bishop
                val = 3
            elif piece.piece_type == 4: # rook
                val = 5
            elif piece.piece_type == 5: # queen
                val = 9

            if piece.color: # white
                heuristic += val
            else:
                heuristic -= val

        # considers whether a player puts the other in check
        if board.is_check():
            if board.turn: # white in check
                heuristic -= 0.5
            else:
                heuristic += 0.5

        return heuristic

if __name__ == '__main__':
    # print("Take queen test")
    # board = chess.Board()
    # print(board)
    # board.remove_piece_at(chess.parse_square("d2"))
    # board.set_piece_at(chess.parse_square("d4"), chess.Piece(1, True))
    # board.remove_piece_at(chess.parse_square("d8"))
    # board.set_piece_at(chess.parse_square("e5"), chess.Piece(5, False))
    # print(board)
    # # board.set_piece_at(0, chess.Piece(6, True)) # white king
    #
    # ai = MinimaxAI()
    # print(ai.choose_move(board))

    # random test:
    random.seed(17)

    n = 20
    while n > 0:
        n-=1
        print(random.choices([0,1], cum_weights = [0.1, 1]))
    print("Done!")

        # print(board.piece_map())
