# Maxwell Carmichael, 10/10/2020, Modified from CS76 Material

import chess


class ChessGame:
    def __init__(self, player1, player2):
        self.board = chess.Board()
        self.players = [player1, player2]

    def make_move(self):

        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)

        self.board.push(move)  # Make the move

    def is_game_over(self):
        if self.board.is_game_over():
            print(self.board)
            if self.board.is_checkmate():
                if self.board.turn:
                    print("CHECKMATE! Black wins!")
                else:
                    print("CHECKMATE! White wins!")
            else:
                print("Stalemate.")
            return True

        return False

    def __str__(self):

        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        move_str = "White to move" if self.board.turn else "Black to move"

        return board_str + "\n" + move_str + "\n"
