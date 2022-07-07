import PossibleMoves

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
                        self.getPawnMoves(r, c, moves, turn)
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

    def getPawnMoves(self, r, c, moves, turn):
        if turn == 'w':
            _moves = []
            _moves = PossibleMoves.getWhitePawnPossibleMoves(r, c, _moves, self.board)
            
            for _move in _moves:
                move = Move((r, c), _move, self.board)
                moves.append(move)
            
            return moves

        elif turn == 'b':
            _moves = []
            _moves = PossibleMoves.getBlackPawnPossibleMoves(r, c, _moves, self.board)
            
            for _move in _moves:
                move = Move((r, c), _move, self.board)
                moves.append(move)
            
            return moves      

    def getRookMoves(self, r, c, moves):
        _moves = []
        _moves = PossibleMoves.getRookPossibleMoves(r, c, _moves)
         
        for _move in _moves:
            move = Move((r, c), _move, self.board)
            moves.append(move)
        
        return moves

    def getBishopMoves(self, r, c, moves):
        _moves = []
        _moves = PossibleMoves.getBishopPossibleMoves(r, c, _moves)
         
        for _move in _moves:
            move = Move((r, c), _move, self.board)
            moves.append(move)
        
        return moves

    def getQueenMoves(self, r, c, moves):
        _moves = []
        _moves = PossibleMoves.getBishopPossibleMoves(r, c, _moves)
        _moves = PossibleMoves.getRookPossibleMoves(r, c, _moves)

        for _move in _moves:
            move = Move((r, c), _move, self.board)
            moves.append(move)
        
        return moves

    def getKingMoves(self, r, c, moves):
        _moves = []
        _moves = PossibleMoves.getKingPossibleMoves(r, c, _moves)
         
        for _move in _moves:
            move = Move((r, c), _move, self.board)
            moves.append(move)
        
        return moves

    def getKnightMoves(self, r, c, moves):
        _moves = []
        _moves = PossibleMoves.getKnightPossibleMoves(r, c, _moves)
         
        for _move in _moves:
            move = Move((r, c), _move, self.board)
            moves.append(move)
        
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