from copy import deepcopy

class ChessGame:
    __slots__ = ('board', 'whiteKing', 'blackKing', 'round', 'checkMate')  # Limit attributes

    def __init__(self, board, player1, player2):
        self.board = board
        self.whiteKing = player1
        self.blackKing = player2
        self.round = 1
        self.checkMate = False

    def getBoard(self):
        return deepcopy(self.board)

    def getWhiteKing(self):
        return self.whiteKing

    def getBlackKing(self):
        return self.blackKing

    def getRound(self):
        return self.round

    def addRound(self):
        self.round = self.getRound() + 1

    def getCheckMate(self):
        return self.checkMate

    def checkForCheckMate(self):
        if self.whiteKing.getCheckMate() or self.blackKing.getCheckMate():
            return True
        return False

    def setCheckMate(self, white):
        if white:
            self.whiteKing.setCheckMate()
        else:
            self.blackKing.setCheckMate()

    def getPlayerTurn(self):
        if self.getRound() % 2 == 0:    # Si la ronda actual es par significa que le toca al rey negro
            return self.getBlackKing()
        return self.getWhiteKing()      # Si la ronda actual es impar entonces le toca al rey blanco

    def checkForCheck(self, white):
        king = None     # Cuadrado en el que se encuentra el rey del color pasado por parámetro
        danger = []     # Lista de posiciones (piezas) que suponen un peligro (jaque)
        menacePieces = []   # Lista con las piezas que amenazan al rey
        squareList = self.board.getSquares()
        for row in squareList:
            for square in row:
                if square.hasPiece() and square.getPiece().getName() == "King" and square.getPiece().isWhite() == white:
                    king = square
                    break
        #print(f"{"White" if white else "Black"} king located in {king.getPosition().printPos()}")
        for row in squareList:
            for square in row:
                if square.hasPiece() and square.getPiece().isWhite() != white:
                    possibleMoveList = square.getPiece().possibleMoves(self.getBoard(), square.getPosition())
                    for move in possibleMoveList:
                        #print(f"{square.getPiece().printData()} {square.getPosition().printPos()} -> {move.getPosition().printPos()}")
                        if move.getPosition().getX() == king.getPosition().getX() and move.getPosition().getY() == king.getPosition().getY():
                            danger.append(move.getPosition())
                            menacePieces.append(square.getPosition())
                            #print("Added item to danger zone")
        #print(f"Danger detected: {len(danger)}")
        if len(danger) > 0:
            return True, danger, menacePieces
        return False, [], []

    def findKing(self, white):
        king = None
        for row in self.getBoard().getSquares():
            for square in row:
                if square.hasPiece() and square.getPiece().getName() == "King" and square.getPiece().isWhite() == white:
                    king = square
        return king
