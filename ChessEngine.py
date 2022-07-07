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
    
    def makeMove(self, move):
        """Makes a move

        Args:
            move (instance of Move class): player move to be performed
        """
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
    
    def undoMove(self):
        """Undo the last move in the moveLog variable of the game object
        """
        if len(self.moveLog) > 0: 
            move = self.moveLog.pop()
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.whiteToMove = not self.whiteToMove

    # a ser implementado
    def getValidMoves(self):
        return self.getAllPossibleMoves()

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
                if self.board[r-1][c] == '--':
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if self.inRange(r - 2, c):
                        if self.board[r - 2][c][0] == '-' and r == 6:
                            moves.append(Move((r, c), (r - 2, c), self.board))
            if self.inRange(r -1, c - 1):
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if self.inRange(r - 1, c + 1):
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.inRange(r+1,c):
                if self.board[r+1][c] == '--':
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if self.inRange(r+2,c):
                        if self.board[r + 2][c][0] == '-' and r == 1:
                            moves.append(Move((r, c), (r + 2, c), self.board))
            if self.inRange(r + 1, c - 1):
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if self.inRange(r + 1, c + 1):
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))            

        return moves

    def getRookMoves(self, r, c, moves):
        steps = [(1,0),(-1,0),(0,1),(0,-1)]
        for step in steps:
            j, k = step
            i = 1
            while True:
                #going down
                if self.inRange(r+i*j,c+i*k): #check if not below board
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
                #going down
                if self.inRange(r+i*j,c+i*k): #check if not below board
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

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol 
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

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