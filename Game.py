from Move import Move
from CastleRights import CastleRights

class Game():
    """Game object

    Variables:
        board(list of lists),whiteToMove(bool),moveLog(list of Move objects)
    """

    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.undoLog = []
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)
        self.checkMate = False
        self.staleMate = False

        #enpassant
        self.enpassantPossible = ()

        #castling
        self.currentCastleRights = CastleRights(True, True, True, True) #current rights
        self.castleRightsLog = [CastleRights(self.currentCastleRights.wks,self.currentCastleRights.bks,
                                            self.currentCastleRights.wqs,self.currentCastleRights.bqs)] #log of rights
    
    def makeMove(self, move):
        """Makes a move

        Args:
            move (instance of Move class): player move to be performed
        """
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        #updates king location
        if move.pieceMoved[1] == 'K':
            if move.pieceMoved[0] == 'w': # updates white king location if white king moved
                self.whiteKingPosition = (move.endRow, move.endCol)
            else: #updates black king location if black king moved
                self.blackKingPosition = (move.endRow, move.endCol)
        
        #updates pawn to Queen if pawn is promoted
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = 'bQ' if self.whiteToMove else 'wQ'

        #enpassant
        if (move.endRow, move.endCol) == self.enpassantPossible:
            self.board[move.startRow][move.endCol] = '--' # capture enpassant
        
        #update enpassantPossible variable
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow+move.endRow)//2,move.endCol)
        else:
            self.enpassantPossible = ()

        #update castle rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastleRights.wks,self.currentCastleRights.bks,
                                                 self.currentCastleRights.wqs,self.currentCastleRights.bqs))

        #perform castle (move rooks)
        if move.isCastleKingSide:
            self.board[move.startRow][5] = self.board[move.startRow][7]
            self.board[move.startRow][7] = '--'
        elif move.isCastleQueenSide:
            self.board[move.startRow][3] = self.board[move.startRow][0]
            self.board[move.startRow][0] = '--'
    
    def undoMove(self):
        """Undo the last move in the moveLog variable of the game object
        """
        if len(self.moveLog) > 0: 
            move = self.moveLog.pop()
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.whiteToMove = not self.whiteToMove

            #update king location
            if move.pieceMoved[1] == 'K':
                if move.pieceMoved[0] == 'w': #white king location to be updated
                    self.whiteKingPosition = (move.startRow, move.startCol)
                else: #black king location to be updated
                    self.blackKingPosition = (move.startRow, move.startCol)
            
            #restore pawn captured on enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                if len(self.moveLog) > 0:
                    lastMove = self.moveLog[-1] #get previous move
                    self.enpassantPossible = ((lastMove.startRow+lastMove.endRow)//2,lastMove.endCol) #restore enpassantPossibleVariable

            #undo castle rights update
            self.castleRightsLog.pop()
            if len(self.castleRightsLog) > 0:
                castleRights = self.castleRightsLog[-1]
                self.currentCastleRights = CastleRights(castleRights.wks,castleRights.bks,castleRights.wqs,castleRights.bqs)

            #undo castle moves (change rooks back)
            if move.isCastleKingSide:
                self.board[move.startRow][7] = self.board[move.startRow][5]
                self.board[move.startRow][5] = '--'
            elif move.isCastleQueenSide:
                self.board[move.startRow][0] = self.board[move.startRow][3]
                self.board[move.startRow][3] = '--'
            
    def updateCastleRights(self, move):
        if move.pieceMoved == 'bK':
            self.currentCastleRights.bks = False
            self.currentCastleRights.bqs = False
        elif move.pieceMoved == 'wK':
            self.currentCastleRights.wks = False
            self.currentCastleRights.wqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastleRights.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastleRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastleRights.bqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastleRights.bks = False

    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastleRights.wks, self.currentCastleRights.bks, self.currentCastleRights.wqs, self.currentCastleRights.bqs)

        #generate possible moves
        moves =  self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingPosition[0],self.whiteKingPosition[1],moves)
        else:
            self.getCastleMoves(self.blackKingPosition[0],self.blackKingPosition[1],moves)

        for move in reversed(moves):
            self.makeMove(move)
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(move)
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0: #checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else: 
                self.staleMate = True
        else: # if we undo a move we need to come back to a not a Mate situation
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastleRights = tempCastleRights
        
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.sqUnderAttack(self.whiteKingPosition[0], self.whiteKingPosition[1])
        else:
            return self.sqUnderAttack(self.blackKingPosition[0], self.blackKingPosition[1])

    def sqUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
        
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        moves = self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves

    def inRange(self, row, col):
        return row >= 0  and row < len(self.board) and col >= 0 and col < len(self.board)
        
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.inRange(r - 1, c): 
                if self.board[r-1][c] ==  '--': #allow move to empty square ahead
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if self.inRange(r - 2, c):
                        if self.board[r - 2][c][0] == '-' and r == 6: #allow move to empty square two ahead if pawn has not moved yet
                            moves.append(Move((r, c), (r - 2, c), self.board))
            if self.inRange(r -1, c - 1): 
                if self.board[r - 1][c - 1][0] == 'b': #allow capture if black on diagonal in front (left)
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEmpassantMove=True))
                
            if self.inRange(r - 1, c + 1): 
                if self.board[r - 1][c + 1][0] == 'b': #allow capture if black on diagonal in front (right)
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEmpassantMove=True))       

        else: #black pawn moving
            if self.inRange(r+1,c):
                if self.board[r+1][c] == '--':
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if self.inRange(r+2,c):
                        if self.board[r + 2][c][0] == '-' and r == 1:
                            moves.append(Move((r, c), (r + 2, c), self.board))
            if self.inRange(r + 1, c - 1):
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEmpassantMove=True))                    
            if self.inRange(r + 1, c + 1):
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))            
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEmpassantMove=True))     
        return moves

    def getRookMoves(self, r, c, moves):
        steps = [(1,0),(-1,0),(0,1),(0,-1)]
        for step in steps:
            j, k = step
            i = 1
            while True:
                if self.inRange(r+i*j,c+i*k): 
                    if self.board[r+i*j][c+i*k] == '--': # if its empty
                        moves.append(Move((r,c),(r+i*j,c+i*k),self.board))
                        i += 1
                    elif (self.board[r+i*j][c+i*k][0] == 'b' and self.board[r][c][0] == 'w'): # if white can capture
                        moves.append(Move((r,c),(r+i*j,c+i*k),self.board))
                        break
                    elif (self.board[r+i*j][c+i*k][0] == 'w' and self.board[r][c][0] == 'b'): # if black can capture
                        moves.append(Move((r,c),(r+i*j,c+i*k),self.board))
                        break                    
                    else: break              
                else: break
        return moves
    
    def getBishopMoves(self, r, c, moves):
        steps = [(1,1),(-1,1),(1,-1),(-1,-1)]
        for step in steps:
            j,k = step
            i = 1
            while True:
                if self.inRange(r+i*j,c+i*k): 
                    if self.board[r+i*j][c+i*k] == '--': # if its empty
                        moves.append(Move((r,c),(r+i*j,c+i*k),self.board))
                        i += 1
                    elif (self.board[r+i*j][c+i*k][0] == 'b' and self.board[r][c][0] == 'w'): # if white can capture
                        moves.append(Move((r,c),(r+i*j,c+i*k),self.board))
                        break
                    elif (self.board[r+i*j][c+i*k][0] == 'w' and self.board[r][c][0] == 'b'): # if black can capture
                        moves.append(Move((r,c),(r+i*j,c+i*k),self.board))
                        break                    
                    else: break              
                else: break
        return moves

    def getQueenMoves(self, r, c, moves):
        moves = self.getRookMoves(r,c,moves)
        moves = self.getBishopMoves(r,c,moves)
        return moves

    def getKingMoves(self, r, c, moves):
        steps = [(-1,-1),(0,1),(-1,1),(1,0),(1,1),(0,-1),(1,-1),(-1,0)]
        for step in steps:
            j, k = step
            if self.inRange(r+j,c+k):
                if self.board[r+j][c+k] == '--':
                    moves.append(Move((r,c),(r+j,c+k),self.board))
                elif self.board[r+j][c+k][0] == 'b' and self.board[r][c][0] == 'w':
                    moves.append(Move((r,c),(r+j,c+k),self.board))
                elif self.board[r+j][c+k][0] == 'w' and self.board[r][c][0] == 'b':
                    moves.append(Move((r,c),(r+j,c+k),self.board)) 
        return moves

    def getCastleMoves(self,r,c,moves):
        if (self.currentCastleRights.wks and r == 7): #white king side castle
            if self.inRange(r,c+2):
                if (not self.sqUnderAttack(r,c+1) and not self.sqUnderAttack(r,c+2) and not self.sqUnderAttack(r,c)):
                    if (self.board[r][c+1] == '--' and self.board[r][c+2] == '--'):
                        moves.append(Move((r,c),(r,c+2),self.board,isCastleKingSide=True))
        if (self.currentCastleRights.wqs and r == 7): #white queen side castle
            if self.inRange(r,c-3):
                if (not self.sqUnderAttack(r,c-1) and not self.sqUnderAttack(r,c-2) and not self.sqUnderAttack(r,c)):
                    if (self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--'):
                        moves.append(Move((r,c),(r,c-2),self.board,isCastleQueenSide=True))
        if (self.currentCastleRights.bks and r == 0): #black king side castle
            if self.inRange(r,c+2):
                if (not self.sqUnderAttack(r,c+1) and not self.sqUnderAttack(r,c+2) and not self.sqUnderAttack(r,c)):
                    if (self.board[r][c+1] == '--' and self.board[r][c+2] == '--'):
                        moves.append(Move((r,c),(r,c+2),self.board,isCastleKingSide=True))
        if (self.currentCastleRights.bqs and r == 0): #black queen side castle
            if self.inRange(r,c-3):
                if (not self.sqUnderAttack(r,c-1) and not self.sqUnderAttack(r,c-2) and not self.sqUnderAttack(r,c)):
                    if (self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--'):
                        moves.append(Move((r,c,),(r,c-2),self.board,isCastleQueenSide=True))
        return moves

    def getKnightMoves(self, r, c, moves):
        steps = [(1,2),(-1,2),(2,1),(-2,1),(1,-2),(-1,-2),(2,-1),(-2,-1)]
        for step in steps:
            j, k = step
            if self.inRange(r+j,c+k):
                if self.board[r+j][c+k] == '--':
                    moves.append(Move((r,c),(r+j,c+k),self.board))
                elif self.board[r+j][c+k][0] == 'b' and self.board[r][c][0] == 'w':
                    moves.append(Move((r,c),(r+j,c+k),self.board))
                elif self.board[r+j][c+k][0] == 'w' and self.board[r][c][0] == 'b':
                    moves.append(Move((r,c),(r+j,c+k),self.board))
        return moves

