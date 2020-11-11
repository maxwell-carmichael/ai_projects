# Maxwell Carmichael, 10/10/2020, Modified from CS76 Material

import chess
import math
import random

class AlphaBetaAI():
    def __init__(self):
        self.depth = 5 # Constant
        self.nodes_visited = 0 # will reset after each move.

        self.random_factor = 0.1 # the percent chance that an as-good move overrides some other move to prevent cycles.
        random.seed(17) # for replicability. i like the number 17.

        # choose the best move given a board
    def choose_move(self, board):
        # if it's white's turn, call max. if it's black's turn, call min.
        if board.turn:
            util_action = self.max_value(board, -math.inf, math.inf, 0)
        else:
            util_action = self.min_value(board, -math.inf, math.inf, 0)

        move = util_action[1]
        print("Move Utility: " + str(util_action[0]))
        print("Maximum Depth: " + str(self.depth))
        print("Nodes visited: " + str(self.nodes_visited))
        self.nodes_visited = 0
        print("AlphaBetaAI recommending move " + str(move))

        return move

        # white move. returns a (utility, move) pair
    def max_value(self, board, alpha, beta, depth):
        self.nodes_visited += 1

        if self.cutoff_test(board, depth):
            return (self.material_value_heuristic(board, depth), None)

        v = -math.inf
        util_action = None # the (utility, move) pair to return

        # get the highest immediate utilities first, so descending.
        piece_map = board.piece_map()
        moves = sorted(board.legal_moves, key = lambda x : self.material_sort_helper(board, piece_map, x))
        # moves = board.legal_moves

        for move in moves:
            board.push(move) # make the move

            move_util_action = self.min_value(board, alpha, beta, depth + 1)
            if move_util_action[0] > v: # finding maximum utility we can get...
                v = move_util_action[0]
                util_action = (v, move)
                alpha = max(alpha, v)

            # to prevent loops (always choosing same move), make there be an override possibility for our v
            elif move_util_action[0] == v and random.choices([True, False], cum_weights = [self.random_factor, 1]):
                util_action = (v, move)

            board.pop() # unmake the move

            # if black has no more interest in the path...
            if v >= beta:
                return util_action

        return util_action

        # black to move. returns a (utility, move) pair
    def min_value(self, board, alpha, beta, depth):
        self.nodes_visited += 1

        if self.cutoff_test(board, depth):
            return (self.material_value_heuristic(board, depth), None)

        v = math.inf
        util_action = None # the (utility, move) pair to return

        # lowest immediate utilities first, so ascending
        piece_map = board.piece_map()
        moves = sorted(board.legal_moves, key = lambda x : self.material_sort_helper(board, piece_map, x))

        for move in moves:
            board.push(move) # make the move

            move_util_action = self.max_value(board, alpha, beta, depth + 1)
            if move_util_action[0] < v: # finding minimum utility we can get...
                v = move_util_action[0]
                util_action = (v, move)
                beta = min(beta, v)

            # to prevent loops (always choosing same move), make there be an override possibility for our v
            elif move_util_action[0] == v and random.choices([True, False], cum_weights = [self.random_factor, 1]):
                util_action = (v, move)

            board.pop() # unmake the move

            # if white has no more interest in the path...
            if v <= alpha:
                return util_action

        return util_action

        # stop iterating if the game is over or if depth limit is reached
    def cutoff_test(self, board, depth):
        return board.is_game_over() or self.depth == depth

    def material_value_heuristic(self, board, depth):
        # win. prioritize checkmates that are sooner.
        if board.is_checkmate():
            # white's turn, so black just checkmated
            if board.turn:
                return -10000 + depth
            # black's turn, so white just checkmated
            else:
                return 10000 - depth

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
            if board.turn: # white
                heuristic -= 0.5
            else:
                heuristic += 0.5

        return heuristic

        # Sort helper function. Prioritizes moves which take more valuable pieces.
    def material_sort_helper(self, board, piece_map, move):
        if move.to_square in piece_map:
            piece = piece_map[move.to_square]

            if piece.piece_type == 2:  # bishop same score as knight
                return -3
            else:
                return -piece.piece_type

        else:
            return 0


if __name__ == '__main__':
    print("Take queen test")
    board = chess.Board()

    board.remove_piece_at(chess.parse_square("d2"))
    board.set_piece_at(chess.parse_square("d4"), chess.Piece(1, True))
    board.remove_piece_at(chess.parse_square("d8"))
    board.set_piece_at(chess.parse_square("e5"), chess.Piece(5, False))
    print("")
    print(board)
    # board.set_piece_at(0, chess.Piece(6, True)) # white king

    ai = AlphaBetaAI()
    moves = board.legal_moves
    print(moves)
    moves = sorted(moves, key = lambda x : ai.material_sort_helper(board, x), reverse=True)
    print(moves)
    print(ai.choose_move(board))

