class Move():
    """Move object

    Variables:
        startRow(int), endRow(int), startCol(int), endCol(int), pieceMoved(str), pieceCaptured(str)
    """

    ranksToRows = {'1': 7,'2': 6,'3': 5,'4': 4,'5': 3,'6': 2,'7': 1,'8': 0}
    rowstoRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEmpassantMove=False, isCastleKingSide=False, isCastleQueenSide=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]        

        #pawn promotion Flag
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        
        #enpassant
        self.isEnpassantMove = isEmpassantMove

        #get captured piece if isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = board[self.startRow][self.endCol]

        #castle flags
        self.isCastleKingSide = isCastleKingSide
        self.isCastleQueenSide = isCastleQueenSide

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol 
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def __str__(self):
        return f" Chess Notation: ({self.getChessNotation()}) --> Start Square: ({self.startRow},{self.startCol}), End Square: ({self.endRow},{self.endCol}), pieceMoved: ({self.pieceMoved}), PieceCaptured: ({self.pieceCaptured}), isEnpassantMove: ({self.isEnpassantMove}), isPawnPromotion: ({self.isPawnPromotion}), isCastleKingSide({self.isCastleKingSide}), isCastleQuennSide: ({self.isCastleQueenSide})"
        

    def getChessNotation(self):
        """Returns chess notation

        Returns:
            String: move in chess notation
        """
        #return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
        #TO-DO: Add check, checkmate, end of game, draw offer and disambiguating moves

        # castling notation
        if self.isCastleKingSide:
            return 'O-O'
        
        if self.isCastleQueenSide:
            return 'O-O-O'
        
        #if not a capture
        if self.pieceCaptured == '--':
            if self.pieceMoved[1] == 'P': #if pawn moves
                ans =  self.getRankFile(self.endRow, self.endCol)

            else: #if other piece moves
                ans =  self.pieceMoved[1] + self.getRankFile(self.endRow, self.endCol) 
        #if a capture
        else:
            if self.pieceMoved[1] == 'P': #if pawn captures (enpassant capture)
                ans =  self.getRankFile(self.startRow,self.startCol)[0] + 'x' + self.getRankFile(self.endRow, self.endCol)

            else: #if other piece captures
                ans = self.pieceMoved[1] + 'x' + self.getRankFile(self.endRow, self.endCol) 
        
        if self.isPawnPromotion:
            ans = ans + 'Q' #ONLY PROMOTES TO QUEEN -- IF PLAYER CAN CHOOSE WE NEED TO ADJUST THIS

        return ans

    def getRankFile(self, r, c):
        """Helper funcion to getChessNotation

        Args:
            r(int): row number
            c(int): col number

        Returns:
            String: Row and Col in Chess Notation
        """
        return self.colsToFiles[c] + self.rowstoRanks[r]