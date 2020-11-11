# Maxwell Carmichael, 10/10/2020, Modified from CS76 Material
# pip3 install python-chess

# Code for testing the algorithm, and playing the AI. 
# To make a move, type from-square and to-square in console, no space. ex: e2e4 could be an opening move for white.

import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
from IterativeAI import IterativeAI


import sys


player1 = HumanPlayer()
player2 = AlphaBetaAI()
# player2 = MinimaxAI()
# player2 = IterativeAI(AlphaBetaAI(), 20)
# player2 = IterativeAI(MinimaxAI(), 20)

game = ChessGame(player1, player2)

# function that significantly simplifies the start board
def open_board(game):
    board = game.board
    board.clear()
    white_king = chess.Piece(6, True)
    black_king = chess.Piece(6, False)
    board.set_piece_at(chess.parse_square("a1"), white_king)
    board.set_piece_at(chess.parse_square("h8"), black_king)

    white_queen = chess.Piece(5, True)
    black_queen = chess.Piece(5, False)
    white_knight = chess.Piece(2, True)
    black_knight = chess.Piece(2, False)
    board.set_piece_at(chess.parse_square("b1"), white_queen)
    board.set_piece_at(chess.parse_square("g8"), black_queen)
    board.set_piece_at(chess.parse_square("b2"), white_knight)
    board.set_piece_at(chess.parse_square("g7"), black_knight)

    white_bishop = chess.Piece(3, True)
    black_bishop = chess.Piece(3, False)
    board.set_piece_at(chess.parse_square("a2"), white_bishop)
    board.set_piece_at(chess.parse_square("h7"), black_bishop)

# black's turn, black can absolutely win in 3 turns
def black_checkmate(game):
    board = game.board
    board.clear()
    board.turn = False

    white_pawn1 = chess.Piece(1, True)
    white_pawn2 = chess.Piece(1, True)
    white_knight = chess.Piece(2, True)
    white_king = chess.Piece(6, True)
    black_king = chess.Piece(6, False)
    black_rook = chess.Piece(4, False)

    board.set_piece_at(chess.parse_square("a2"), white_pawn1)
    board.set_piece_at(chess.parse_square("b2"), white_pawn2)
    board.set_piece_at(chess.parse_square("a1"), white_king)
    board.set_piece_at(chess.parse_square("b3"), white_knight)
    board.set_piece_at(chess.parse_square("h8"), black_king)
    board.set_piece_at(chess.parse_square("h7"), black_rook)


# open_board(game)
# black_checkmate(game)
# e2e4

while not game.is_game_over():
    print(game)
    game.make_move()

#print(hash(str(game.board)))
