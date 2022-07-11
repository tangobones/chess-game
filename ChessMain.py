import pygame
from Game import Game
from Move import Move
import ChessAI

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    """Generates dictionary where keys are pieces in 'bR' format and values are png files 
    """
    pieces = ['bR','bN','bB','bQ','bK','bP','wR','wN','wB','wQ','wK','wP']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load(f'resources/{piece}.png')

def main():
    """Main program loop and initialization protocols
    """

    # initialization 
    pygame.init() 
    loadImages()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    gs = Game()
    validMoves = gs.getValidMoves()
    
    moveMade = False # flag variable for when a move is made
    
    running = True
    animation = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True #If human is playing white this must be true if AI is playing this needs to be false
    playerTwo = False #same as above but for black
    
    # main game loop with all event listners and function calls
    while running: 
        isHumanTurn = ((gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo))        
        # event listner
        for e in pygame.event.get():
            
            # quits the game when windown is closed
            if e.type == pygame.QUIT:
                running = False
            
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver and isHumanTurn:
                    location = pygame.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col): # clicking on the same piece twice undo the click
                        sqSelected = ()
                        playerClicks = []
                    else:              
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                        if gs.board[playerClicks[0][0]][playerClicks[0][1]] == "--": # checks if the first click is and empty position
                            sqSelected = ()
                            playerClicks = []    
                    if len(playerClicks) == 2: # perform move if two clicks already logged
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                if animation: animateMove(validMoves[i], screen, gs, clock)
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
                
                #AI move finder logic
                if not gameOver and not isHumanTurn:
                    AIMove = ChessAI.findBestMoveMinMax(gs, validMoves)
                    if AIMove is None:
                        AIMove = ChessAI.findRandomMove(validMoves)
                    gs.makeMove(AIMove)
                    if animation: animateMove(AIMove, screen, gs, clock)
                    moveMade = True
                    
                
                #updated validMoves if move is made
                if moveMade:
                    
                    #Prints moveLog for debugging
                    print("Move Log: ")
                    for i in range(len(gs.moveLog)):
                        print(gs.moveLog[i])   

                    validMoves = gs.getValidMoves()
                    moveMade = False

            # keyboard handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z: #press z to undo a move
                    gs.undoMove()
                    moveMade = True
                    gameOver = False
                if e.key == pygame.K_a: #press a to toggle animation effects
                    animation = not animation
                if e.key == pygame.K_r: #press r to reset the board
                    gs = Game()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    gameOver = False

        # draws new game state
        drawGameState(screen, gs, playerClicks, validMoves)
        
        # checks for checkmate or stalemate
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Game Ended: Black wins by checkmate")
            else:
                drawText(screen, "Game Ended: White wins by checkmate")
        if gs.staleMate:
            gameOver = True
            drawText(screen, "Game Ended: Stalemate")

        # ticks and updates screen
        clock.tick(MAX_FPS)
        pygame.display.flip()

def drawGameState(screen, gs, playerClicks, validMoves):
    """Draws game state to the screen

    Args:
        screen (pygame screen object): pygame screen
        gs (object instance of Game class): current game being played
        playerClicks (list of tuples): list of current player clicks (maximum of two clicks, startSq and endSq)
    """
    drawBoard(screen)

    #draw highlights
    if len(playerClicks) > 0:
        highlightSelectedPiece(screen, playerClicks)    
        highlightPossibleMoves(screen, playerClicks, validMoves)
    
    if len(gs.moveLog)>0:
        hightlightLastMove(screen, gs)

    drawPieces(screen, gs.board)

def hightlightLastMove(screen, gs):
    color = pygame.Color('lightblue')
    lastMove = gs.moveLog[-1]
    padding = 5
    s = pygame.Surface((SQ_SIZE - padding * 2, SQ_SIZE - padding * 2))
    s.set_alpha(100)
    s.fill(color)
    screen.blit(s, (lastMove.endCol*SQ_SIZE + padding, lastMove.endRow*SQ_SIZE + padding))

def highlightPossibleMoves(screen, playerClicks, validMoves):
    startSq = playerClicks[0]
    possibleMoves = []
    possibleMoves = piecePossibleMoves(startSq, validMoves)

    if playerClicks[0] in possibleMoves:
        possibleMoves.remove(playerClicks[0])

    for move in possibleMoves:
        color = pygame.Color('light green')
        r, c = move
        padding = 5 # adds padding to the selected piece valid moves
        s = pygame.Surface((SQ_SIZE - padding * 2, SQ_SIZE - padding * 2))
        s.set_alpha(100)
        s.fill(color)
        screen.blit(s, (c*SQ_SIZE + padding, r*SQ_SIZE + padding))

def piecePossibleMoves(startSq, validMoves):
    possibleMovesSq = []
    pieceRow, pieceCol = startSq

    for move in validMoves:
        if move.startRow == pieceRow and move.startCol == pieceCol:
            square = (move.endRow, move.endCol)
            possibleMovesSq.append(square)
    return possibleMovesSq

def highlightSelectedPiece(screen, playerClicks):
    if len(playerClicks) == 1:
        color = pygame.Color('light yellow')
        r = playerClicks[0][0]
        c = playerClicks[0][1]
        padding = 5 # adds padding to the selected piece
        s = pygame.Surface((SQ_SIZE - padding * 2, SQ_SIZE - padding * 2))
        s.set_alpha(150)
        s.fill(color)
        screen.blit(s, (c*SQ_SIZE + padding, r*SQ_SIZE + padding))

def drawBoard(screen):
    """Draws the board to the screen

    Args:
        screen (pygame screen object): pygame screen
    """
    global colors
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen,color,pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    """Draw pieces to the screen

    Args:
        screen (pygame screen object): pygame screen
        board (list of list): current board
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, gs, clock):

    # ADD ANIMATION FOR THE ROOK IN CASE OF A CASTLE MOVE

    board = gs.board
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frame to move 1 square of animation
    frameCount = (abs(dR)+abs(dC))*framesPerSquare


    
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        
        #erase piece moved from ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pygame.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, endSquare)
        
        #highlights the move during animation
        hightlightLastMove(screen, gs)
        
        #draw captured piece onto rectagle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
        #updates the screen
        pygame.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = pygame.font.SysFont('Helvetica', 20, True, False)
    textObject = font.render(text, 0, pygame.Color('pink'))
    textLocation = pygame.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    
    screen.blit(textObject, textLocation)
    textObject = font.render(text,0,pygame.Color('red'))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == '__main__':
    main()
    


