from ChessEngine import *
import random
pieceScore = {"K" : 0, "Q" : 10, "R" : 5, "B" : 3, "N" : 3, "p" : 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
	return validMoves[random.randint(0, len(validMoves) - 1)]

def findGreedyMove(gs, validMoves):
	turnMultiplier = 1 if gs.whiteToMove else -1
	opponentMinMaxScore = CHECKMATE
	bestPlayerMove = None
	random.shuffle(validMoves)
	for playerMove in validMoves :
		gs.makeMove(playerMove)
		opponentMoves = gs.getValidMoves()
		opponentMaxScore = -CHECKMATE
		for opponentMove in opponentMoves: 
			gs.makeMove(opponentMove)
			if(gs.checkMate):
				score = -turnMultiplier * CHECKMATE
			elif(gs.staleMate):
				score = STALEMATE
			else:
				score = -turnMultiplier * scoreMaterial(gs.board)
			if(score > opponentMaxScore):
				opponentMaxScore = score
			gs.undoMove()
		if(opponentMinMaxScore > opponentMaxScore):
			opponentMinMaxScore = opponentMaxScore
			bestPlayerMove = playerMove
		gs.undoMove()
	return bestPlayerMove

def scoreMaterial(board):
	score = 0
	for r in board:
		for sq in r:
			if(sq[0] == 'w'):
				score += pieceScore[sq[1]]
			elif(sq[0] == 'b'):
				score -= pieceScore[sq[1]]
	return score