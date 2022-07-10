class Game():
    """Game object

    Variables:
        board(list of lists),whiteToMove(bool),moveLog(list of Move objects)
    """

    def __init__(self):
        self.board = [
            ["bR","--","--","--","bK","--","--","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","--","--","--","wK","--","--","wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.undoLog = []
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)

        #mates
        self.checkMate = False
        self.staleMate = False

        #enpassant
        self.enpassantPossible = ()

        #castling
        self.blackKinghasMoved = False
        self.whiteKinghasMoved = False
        self.blackKingSideRookhasMoved = False
        self.blackQueenSideRookhasMoved = False
        self.whiteKingSideRookhasMoved = False
        self.whiteKingSideRokkhasMoved = False

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
                self.whiteKinghasMoved = True
            else: #updates black king location if black king moved
                self.blackKingPosition = (move.endRow, move.endCol)
                self.blackKinghasMoved = True

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

        #castling move the rook
        if (move.pieceMoved[1] == 'K' and (move.endCol - move.startCol) == 2): #King side castling
            if move.pieceMoved[0] == 'b':
                print('king side black castling')
                self.board[0][7] = '--' #removes Rook
                self.board[0][5] = 'bR' #adds Rook back
            elif move.pieceMoved[0] == 'w':
                print('king side white castling')
                self.board[7][7] = '--' #removes Rook
                self.board[7][5] = 'wR' #adds white Rook back
            self.whiteToMove = not self.whiteToMove
        if (move.pieceMoved[1] == 'K' and (move.endCol - move.startCol) == -2): #Queen side castling
            if move.pieceMoved[0] == 'b':
                print('queen side black castling')
                self.board[0][0] = '--' #removes Rook
                self.board[0][3] = 'bR' #adds Rook back
            elif move.pieceMoved[0] == 'w':
                print('queen side white castling')
                self.board[7][0] = '--' #removes Rook
                self.board[7][3] = 'wR' #adds white Rook back   
            self.whiteToMove = not self.whiteToMove         

    

    #undo king movements needs to set kinghasmoved back to false if king has not moved (idea, look at all movelogs to see if king has moved)
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
            
            # restore pawn on the enpassant move
            if move.isEnpassant:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            #restore rook on castling
            if move.isKingSideCastling:
                if move.pieceMoved == 'wK':
                    self.board[7][5] = '--'
                    self.board[7][7] = 'wR'
                if move.pieceMoved == 'bK':
                    self.board[0][5] = '--'
                    self.board[0][7] = 'bR'
            
            if move.isQueenSideCastling:
                if move.pieceMoved == 'wK':
                    self.board[7][3] = '--'
                    self.board[7][0] = 'wR'
                if move.pieceMoved == 'bK':
                    self.board[0][3] = '--'
                    self.board[0][0] = 'bR'

    def getValidMoves(self):
        return self.getAllPossibleMoves() # DELETE THIS LINE TO GET VALID MOVES WORKING AGAIN
        tempEnpassantPossible = self.enpassantPossible
        moves =  self.getAllPossibleMoves()
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
                    print('called')
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEmpassant=True))
                
            if self.inRange(r - 1, c + 1): 
                if self.board[r - 1][c + 1][0] == 'b': #allow capture if black on diagonal in front (right)
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    print('called')
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEmpassant=True))       

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
                    print('called')
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEmpassant=True))                    
            if self.inRange(r + 1, c + 1):
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))            
                elif (r + 1, c + 1) == self.enpassantPossible:
                    print('called')
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEmpassant=True))     
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

        #castling moved flags
        whiteKingMoved = False
        blackKingMoved = False
        kingSideBlackRookMoved = False
        queenSideBlackRookMoved = False
        kingSideWhiteRookMoved = False 
        queenSideWhiteRookMoved = False

        # checks all moves previouly made to see if kings or rooks have moved and update the flags
        for i in range(len(self.moveLog)):
            if self.moveLog[i].pieceMoved == 'wK':
                whiteKingMoved = True
            if self.moveLog[i].pieceMoved == 'bK':
                blackKingMoved = True
            if self.moveLog[i].pieceMoved == 'bR':
                if self.moveLog[i].startCol == 7:
                    kingSideBlackRookMoved = True
                if self.moveLog[i].startCol == 0:
                    queenSideBlackRookMoved = True
            if self.moveLog[i].pieceMoved == 'wR':
                if self.moveLog[i].startCol == 7:
                    kingSideWhiteRookMoved = True
                if self.moveLog[i].startCol == 0:
                    queenSideWhiteRookMoved = True


        #castling checks if not moved and no obstructions (DOES NOT CHECK FOR IN CHECK AND THROUGH CHECK CONDITIONS YET)
        if (not whiteKingMoved and c == 4 and r == 7):
            if (self.board[r][c+1] == '--' and self.board[r][c+2] == '--' and not kingSideWhiteRookMoved):
                moves.append((Move((r,c),(r,c+2), self.board, isKingSideCastling=True)))
            
            if (self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--' and not queenSideWhiteRookMoved):
                moves.append((Move((r,c),(r,c-2), self.board, isQueenSideCastling=True)))       

        if (not blackKingMoved and c == 4) and r == 0:
            if (self.board[r][c+1] == '--' and self.board[r][c+2] == '--' and not kingSideBlackRookMoved):
                moves.append((Move((r,c),(r,c+2), self.board, isKingSideCastling=True)))
            
            if (self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--' and not queenSideBlackRookMoved):
                moves.append((Move((r,c),(r,c-2), self.board, isQueenSideCastling=True)))               

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

class Move():
    """Move object

    Variables:
        startRow(int), endRow(int), startCol(int), endCol(int), pieceMoved(str), pieceCaptured(str)
    """

    ranksToRows = {'1': 7,'2': 6,'3': 5,'4': 4,'5': 3,'6': 2,'7': 1,'8': 0}
    rowstoRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEmpassant=False, isQueenSideCastling=False, isKingSideCastling=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]        

        #pawn promotion Flag
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        
        #enpassant
        self.isEnpassant = isEmpassant

        #get captured piece if isEnpassantMove
        if self.isEnpassant:
            self.pieceCaptured = board[self.startRow][self.endCol]

        #castling
        self.isQueenSideCastling = isQueenSideCastling
        self.isKingSideCastling = isKingSideCastling


        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol 
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def __str__(self):
        return f"    Start Square: ({self.startRow},{self.startCol}), End Square: ({self.endRow},{self.endCol}), pieceMoved: ({self.pieceMoved}), PieceCaptured: ({self.pieceCaptured}), isEnpassantMove: ({self.isEnpassant}), isPawnPromotion: ({self.isPawnPromotion}), isQueenSideCastling: ({self.isQueenSideCastling}), isKingSideCastling: ({self.isKingSideCastling})"
        

    def getChessNotation(self):
        """Returns chess notation

        Returns:
            String: move in chess notation
        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        """Helper funcion to getChessNotation

        Args:
            r(int): row number
            c(int): col number

        Returns:
            String: Row and Col in Chess Notation
        """
        return self.colsToFiles[c] + self.rowstoRanks[r]