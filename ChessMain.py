from ChessEngine import *
import pygame as p # type: ignore
from ChessAI import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
	pieces = ["bR","bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bp", "wp", "wR","wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
	for piece in pieces:
		IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
	p.init()
	screen = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	screen.fill(p.Color("white"))
	gs = GameState()
	validMoves = gs.getValidMoves()
	playerOne = True
	playerTwo = False

	moveMade = False
	loadImages()
	running = True
	sqSelected = ()
	playerClicks = []

	while(running):
		# for x in validMoves:
		# 	print(x.startRow, x.startCol, x.endRow, x.endCol)
		# print(gs.enpassantPossibleLog)
		# print(gs.currentCastleRights.bks, gs.currentCastleRights.bqs, gs.currentCastleRights.wks, gs.currentCastleRights.wqs)
		# print("------------------------------------------------------")
		# for x in gs.CastleRightsLog:
		# 	print(x.wks, x.bks, x.wqs, x.bqs)
		# print("------------------------------------------------------")

		humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

		for e in p.event.get():
			if(e.type == p.QUIT):
				running = False
			elif(e.type == p.MOUSEBUTTONDOWN):
				if(humanTurn):
					location = p.mouse.get_pos()
					col = location[0] // SQ_SIZE
					row = location[1] // SQ_SIZE
					if(sqSelected == (row, col)):
						sqSelected = ()
						playerClicks = []
					else:
						sqSelected = (row, col)
						playerClicks.append(sqSelected)
					if(len(playerClicks) == 2):
						move = Move(playerClicks[0], playerClicks[1], gs.board)
						# print(move.getChessNotation())
						for i in range(len(validMoves)):
							if(move == validMoves[i]):
								gs.makeMove(validMoves[i])
								moveMade = True
								sqSelected = ()
								playerClicks = []
						if not moveMade:
							playerClicks = [sqSelected]
			elif(e.type == p.KEYDOWN):
				if(e.key == p.K_z):
					gs.undoMove()
				moveMade = True
		
		if(not humanTurn):
			AIMove = finRandomMove(validMoves)
			gs.makeMove(AIMove)
			moveMade = True

		if(moveMade):
			validMoves = gs.getValidMoves()
			moveMade = False
		drawGameState(screen, gs, validMoves, sqSelected)
		clock.tick(MAX_FPS)
		p.display.flip()

def drawGameState(screen, gs, validMoves, sqSelected):
	drawBoard(screen)
	highlightSquares(screen, gs, validMoves, sqSelected)
	drawPieces(screen, gs.board)

def highlightSquares(screen, gs, validMoves, sqSelected):
	if(sqSelected != ()):
		r, c = sqSelected
		if(gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b')):
			s = p.Surface((SQ_SIZE, SQ_SIZE))
			s.set_alpha(100)
			s.fill(p.Color("blue"))
			screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
			s.fill(p.Color("yellow"))
			for move in validMoves:
				if(move.startRow == r and move.startCol == c):
					screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawBoard(screen):
	colors = [p.Color("white"), p.Color("grey")]
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			color = colors[(r + c) % 2] 
			p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[r][c]
			if(piece != "--"):
				screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
	main()