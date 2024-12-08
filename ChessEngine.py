class GameState():
	def __init__(self):
		self.board = 	[["bR","bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
						["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
						["--", "--", "--", "--", "--", "--", "--", "--"],
						["--", "--", "--", "--", "--", "--", "--", "--"],
						["--", "--", "--", "--", "--", "--", "--", "--"],
						["--", "--", "--", "--", "--", "--", "--", "--"],
						["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
						["wR","wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
		self.whiteToMove = True
		self.moveLog = []

		self.moveFunctions = {'p' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves, 'B' : self.getBishopMoves}

		self.whiteKingLocation = (7, 4)
		self.blackKingLocation = (0, 4)
		self.checkMate = False
		self.staleMate = False
	
	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = "--"
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.moveLog.append(move)
		self.whiteToMove = not self.whiteToMove
		if(move.pieceMoved == 'wK'):
			self.whiteKingLocation = (move.endRow, move.endCol)
		elif(move.pieceMoved == 'bK'):
			self.blackKingLocation = (move.endRow, move.endCol)
	
	def undoMove(self):
		if(len(self.moveLog) != 0):
			move = self.moveLog.pop()
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.whiteToMove = not self.whiteToMove
			if(move.pieceMoved == 'wK'):
				self.whiteKingLocation = (move.startRow, move.startCol)
			elif(move.pieceMoved == 'bK'):
				self.blackKingLocation = (move.startRow, move.startCol)

	def getValidMoves(self):
		# 1) Generate all possible moves 
		moves = self.getAllPossibleMoves()
		# 2) For each move, make the move
		for i in range(len(moves) - 1, -1, -1):
			self.makeMove(moves[i])
		# 3) Generate all opponent's moves 
		# 4) For each of your opponent's moves, see it they attack the king 
			self.whiteToMove = not self.whiteToMove
			if(self.inCheck()):
				moves.remove(moves[i])
			self.whiteToMove = not self.whiteToMove
			self.undoMove()
		# 5) If they do attack your king, not a valid move 
		if(len(moves) == 0):
			#either checkmate or stalemate
			if(self.inCheck()):
				self.checkMate = True
			else:
				self.StaleMate = True
		else:
			self.checkMate = False
			self.StaleMate = False
		return moves
	
	def inCheck(self):
		if(self.whiteToMove):
			return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
		else:
			return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

	def squareUnderAttack(self, r, c):
		self.whiteToMove = not self.whiteToMove
		oppMoves = self.getAllPossibleMoves()
		self.whiteToMove = not self.whiteToMove
		for move in oppMoves:
			if(move.endRow == r and move.endCol == c):
				return True
		return False

	def getAllPossibleMoves(self):
		moves = []
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				turn = self.board[r][c][0]
				if((turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove)):
					piece = self.board[r][c][1]
					self.moveFunctions[piece](r, c, moves)

		return moves

	def getPawnMoves(self, r, c, moves):
		if(self.whiteToMove):
			if(self.board[r - 1][c] == "--"):
				moves.append(Move((r, c), (r - 1, c), self.board))
			if(r == 6 and self.board[r - 2][c] == "--" and self.board[r - 1][c] == "--"):
				moves.append(Move((r, c), (r - 2, c), self.board))
		
			if(c - 1 >= 0):
				if(self.board[r - 1][c - 1][0] == 'b'):
					moves.append(Move((r, c), (r - 1, c - 1), self.board))
			
			if(c + 1 <= 7):
				if(self.board[r - 1][c + 1][0] == 'b'):
					moves.append(Move((r, c), (r - 1, c + 1), self.board))
		else:
			if(self.board[r + 1][c] == "--"):
				moves.append(Move((r, c), (r + 1, c), self.board))
			if(r == 1 and self.board[r + 2][c] == "--" and self.board[r + 1][c] == "--"):
				moves.append(Move((r, c), (r + 2, c), self.board))
		
			if(c - 1 >= 0):
				if(self.board[r + 1][c - 1][0] == 'w'):
					moves.append(Move((r, c), (r + 1, c - 1), self.board))
			
			if(c + 1 <= 7):
				if(self.board[r + 1][c + 1][0] == 'w'):
					moves.append(Move((r, c), (r + 1, c + 1), self.board))


	def getRookMoves(self, r, c, moves):
		directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
		enemy_color = 'b' if self.whiteToMove else 'w'

		for dr, dc in directions:
			for i in range(1, 8): 
				end_row, end_col = r + dr * i, c + dc * i
				if 0 <= end_row < 8 and 0 <= end_col < 8: 
					end_piece = self.board[end_row][end_col]
					if end_piece == "--":
						moves.append(Move((r, c), (end_row, end_col), self.board))
					elif end_piece[0] == enemy_color: 
						moves.append(Move((r, c), (end_row, end_col), self.board))
						break 
					else: 
						break
				else:
					break


	def getKnightMoves(self, r, c, moves):
		knight_moves = [
			(-2, -1), (-2, 1), (-1, -2), (-1, 2),
			(1, -2), (1, 2), (2, -1), (2, 1)
		]
		enemy_color = 'b' if self.whiteToMove else 'w'

		for dr, dc in knight_moves:
			end_row, end_col = r + dr, c + dc
			if 0 <= end_row < 8 and 0 <= end_col < 8:
				end_piece = self.board[end_row][end_col]
				if end_piece == "--" or end_piece[0] == enemy_color:
					moves.append(Move((r, c), (end_row, end_col), self.board))


	def getBishopMoves(self, r, c, moves):
		directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 
		enemy_color = 'b' if self.whiteToMove else 'w'

		for dr, dc in directions:
			for i in range(1, 8):
				end_row, end_col = r + dr * i, c + dc * i
				if 0 <= end_row < 8 and 0 <= end_col < 8:
					end_piece = self.board[end_row][end_col]
					if end_piece == "--": 
						moves.append(Move((r, c), (end_row, end_col), self.board))
					elif end_piece[0] == enemy_color:
						moves.append(Move((r, c), (end_row, end_col), self.board))
						break
					else:
						break
				else:
					break


	def getQueenMoves(self, r, c, moves):
		directions = [
			(-1, 0), (1, 0), (0, -1), (0, 1),
			(-1, -1), (-1, 1), (1, -1), (1, 1)
		]
		enemy_color = 'b' if self.whiteToMove else 'w'

		for dr, dc in directions:
			for i in range(1, 8):
				end_row, end_col = r + dr * i, c + dc * i
				if 0 <= end_row < 8 and 0 <= end_col < 8:
					end_piece = self.board[end_row][end_col]
					if end_piece == "--":
						moves.append(Move((r, c), (end_row, end_col), self.board))
					elif end_piece[0] == enemy_color:
						moves.append(Move((r, c), (end_row, end_col), self.board))
						break
					else:
						break
				else:
					break 


	def getKingMoves(self, r, c, moves):
		king_moves = [
			(-1, -1), (-1, 0), (-1, 1),
			(0, -1),          (0, 1),
			(1, -1), (1, 0), (1, 1)
		]
		enemy_color = 'b' if self.whiteToMove else 'w'

		for dr, dc in king_moves:
			end_row, end_col = r + dr, c + dc
			if 0 <= end_row < 8 and 0 <= end_col < 8:
				end_piece = self.board[end_row][end_col]
				if end_piece == "--" or end_piece[0] == enemy_color:
					moves.append(Move((r, c), (end_row, end_col), self.board))

class Move():
	ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
	rowsToRanks = {v : k for k, v in ranksToRows.items()}
	filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
	colsToFiles = {v : k for k, v in filesToCols.items()}

	def __init__(self, startSq, endSq, board):
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[self.startRow][self.startCol]
		self.pieceCaptured = board[self.endRow][self.endCol]
		self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
	
	def __eq__(self, other):
		if(isinstance(other, Move)):
			return self.moveID == other.moveID
		return False

	def getChessNotation(self):
		return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

	def getRankFile(self, r, c):
		return self.colsToFiles[c] + self.rowsToRanks[r]