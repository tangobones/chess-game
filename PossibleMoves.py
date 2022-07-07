from ChessMain import DIMENSION

def getRookPossibleMoves(pieceRow, pieceCol, possibleMovesSq):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if r == pieceRow or c == pieceCol:
                possibleMovesSq.append((r,c))
    return possibleMovesSq

def getKnightPossibleMoves(pieceRow, pieceCol, possibleMovesSq):
    if inRange(pieceRow+1,pieceCol+2):
        possibleMovesSq.append((pieceRow+1,pieceCol+2))
    if inRange(pieceRow+1,pieceCol-2):
        possibleMovesSq.append((pieceRow+1,pieceCol-2))
    if inRange(pieceRow-1,pieceCol+2):
        possibleMovesSq.append((pieceRow-1,pieceCol+2))
    if inRange(pieceRow-1,pieceCol-2):
        possibleMovesSq.append((pieceRow-1,pieceCol-2))
    if inRange(pieceRow+2,pieceCol+1):
        possibleMovesSq.append((pieceRow+2,pieceCol+1))
    if inRange(pieceRow+2,pieceCol-1):
        possibleMovesSq.append((pieceRow+2,pieceCol-1))
    if inRange(pieceRow-2,pieceCol+1):
        possibleMovesSq.append((pieceRow-2,pieceCol+1))
    if inRange(pieceRow-2,pieceCol-1):
        possibleMovesSq.append((pieceRow-2,pieceCol-1))
    return possibleMovesSq

def getBishopPossibleMoves(pieceRow, pieceCol, possibleMovesSq):
    for i in range(1,DIMENSION):
        if inRange(pieceRow+i, pieceCol+i):
            possibleMovesSq.append((pieceRow + i, pieceCol + i))
        if inRange(pieceRow-i, pieceCol-i):
            possibleMovesSq.append((pieceRow - i, pieceCol - i))
        if inRange(pieceRow+i, pieceCol-i):
            possibleMovesSq.append((pieceRow + i, pieceCol - i))
        if inRange(pieceRow-i, pieceCol+i):
            possibleMovesSq.append((pieceRow - i, pieceCol + i))
    return possibleMovesSq    

def getKingPossibleMoves(pieceRow, pieceCol, possibleMovesSq):
    for i in range(-1,2):
        for j in range(-1,2):
            if inRange(pieceRow + i,pieceCol + j):
                possibleMovesSq.append((pieceRow + i, pieceCol + j))
    return possibleMovesSq

def getWhitePawnPossibleMoves(pieceRow, pieceCol, possibleMovesSq, board):
    if pieceRow == 6:
        possibleMovesSq.append((pieceRow - 2, pieceCol))
    possibleMovesSq.append((pieceRow - 1, pieceCol))

    if inRange(pieceRow - 1, pieceCol + 1):
        if board[pieceRow - 1][pieceCol + 1][0] == 'b':
            possibleMovesSq.append((pieceRow - 1, pieceCol + 1))

    if inRange(pieceRow - 1, pieceCol - 1):
        if board[pieceRow - 1][pieceCol - 1][0] == 'b':
            possibleMovesSq.append((pieceRow - 1, pieceCol - 1))

    return possibleMovesSq

def getBlackPawnPossibleMoves(pieceRow, pieceCol, possibleMovesSq, board):
    if pieceRow == 1:
        possibleMovesSq.append((pieceRow + 2, pieceCol))
    if inRange(pieceRow + 1, pieceCol):
        possibleMovesSq.append((pieceRow + 1, pieceCol))

    if inRange(pieceRow + 1, pieceCol + 1):
        if board[pieceRow + 1][pieceCol + 1][0] == 'w':
            possibleMovesSq.append((pieceRow + 1, pieceCol + 1))

    if inRange(pieceRow + 1, pieceCol - 1):
        if board[pieceRow + 1][pieceCol - 1][0] == 'w' and inRange(pieceRow + 1, pieceCol - 1):
            possibleMovesSq.append((pieceRow + 1, pieceCol - 1))

    return possibleMovesSq

def inRange(row, col):
    return row >= 0  and row < DIMENSION and col >= 0 and col < DIMENSION