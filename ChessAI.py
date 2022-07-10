import random

pieceScores = {'K': 0, 'P' : 1, 'N' : 3, 'B' : 3, 'R' : 5, 'Q' : 10}
CHECKMATE = 10000
STALEMATE = 0


def findRandomMove(validMoves):
    """Random Move AI

    Args:
        validMoves (list of moves): list of all valid moves

    Returns:
        move: chosen random move
    """
    return validMoves[random.randint(0, len(validMoves)-1)]


# iterative min max with depth of 2
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1 
    oppMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        oppMoves = gs.getValidMoves()
        oppMaxScore = -CHECKMATE

        for oppMove in oppMoves:
            gs.makeMove(oppMove)

            if gs.checkMate:
                score = -turnMultiplier * CHECKMATE

            elif gs.staleMate:
                score = STALEMATE

            else:
                score = -turnMultiplier * scoreMaterial(gs.board)

            if score > oppMaxScore:
                oppMaxScore = score

            gs.undoMove()

        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove 
        
        gs.undoMove()
    
    return bestPlayerMove

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] == 'b':
                score -= pieceScores[square[1]]
    
    return score
