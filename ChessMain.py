import pygame
from Game import Game
from Move import Move

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
    sqSelected = ()
    playerClicks = []
    
    # main game loop with all event listners and function calls
    while running: 
        # event listner
        for e in pygame.event.get():
            
            # quits the game when windown is closed
            if e.type == pygame.QUIT:
                running = False
            
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
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
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []

                    #Prints moveLog for debugging
                    print("Move Log: ")
                    for i in range(len(gs.moveLog)):
                        print(gs.moveLog[i])   

                    if not moveMade:
                        playerClicks = [sqSelected]
            
            # keyboard handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        # draws new game state
        drawGameState(screen, gs, playerClicks, validMoves)
        
        # checks for checkmate or stalemate
        if gs.checkMate:
            print('CHECKMATE')
        if gs.staleMate:
            print('STALEMATE')

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

    drawPieces(screen, gs.board)

def highlightPossibleMoves(screen, playerClicks, validMoves):
    startSq = playerClicks[0]
    possibleMoves = []
    possibleMoves = piecePossibleMoves(startSq, validMoves)

    if playerClicks[0] in possibleMoves:
        possibleMoves.remove(playerClicks[0])

    for move in possibleMoves:
        color = pygame.Color('light green')
        r, c = move
        padding = 0 # adds padding to the selected piece valid moves
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
        padding = 0 # adds padding to the selected piece
        s = pygame.Surface((SQ_SIZE - padding * 2, SQ_SIZE - padding * 2))
        s.set_alpha(150)
        s.fill(color)
        screen.blit(s, (c*SQ_SIZE + padding, r*SQ_SIZE + padding))

def drawBoard(screen):
    """Draws the board to the screen

    Args:
        screen (pygame screen object): pygame screen
    """
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

if __name__ == '__main__':
    main()
    


