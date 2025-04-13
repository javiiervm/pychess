import Square as s
import Position as p
import PieceFactory as f

class Board:
    __slots__ = 'squares'  # Limit attributes

    def __init__(self):
        # Initialize 8x8 matrix of None
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.initializeBoard()
        
    def initializeBoard(self):
        for row in range(8):
            for column in range(8):
                if (row == 0 or row == 7) and (column == 0 or column == 7):
                    self.squares[row][column] = s.Square(p.Position(row, column), f.createPiece("Rook", row == 7))
                # Place Knights
                elif (row == 0 or row == 7) and (column == 1 or column == 6):
                    self.squares[row][column] = s.Square(p.Position(row, column), f.createPiece("Knight", row == 7))
                # Place Bishops
                elif (row == 0 or row == 7) and (column == 2 or column == 5):
                    self.squares[row][column] = s.Square(p.Position(row, column), f.createPiece("Bishop", row == 7))
                # Place Queens
                elif (row == 0 and column == 3) or (row == 7 and column == 3):
                    self.squares[row][column] = s.Square(p.Position(row, column), f.createPiece("Queen", row == 7))
                # Place Kings
                elif (row == 0 and column == 4) or (row == 7 and column == 4):
                    self.squares[row][column] = s.Square(p.Position(row, column), f.createPiece("King", row == 7))
                # Place Pawns
                elif row == 1 or row == 6:
                    self.squares[row][column] = s.Square(p.Position(row, column), f.createPiece("Pawn", row == 6))
                # Empty Squares
                else:
                    self.squares[row][column] = s.Square(p.Position(row, column), None)

    def getSquares(self):
        return self.squares

    def getPlayerSquares(self, white):
        squares = []
        for row in range(8):
            for column in range(8):
                if self.squares[row][column].hasPiece() and self.squares[row][column].getPiece().isWhite() == white:
                    squares.append(self.squares[row][column])
        return squares

    def findSquare(self, position):
        if position.getX() < 0 or position.getX() > 7 or position.getY() < 0 or position.getY() > 7:
            return s.Square(p.Position(-1, -1), None)
        return self.squares[position.getX()][position.getY()]

    def printSquareInfo(self, position):
        square = self.findSquare(position)
        print(f"SQUARE {square.getPosition().printPos()} -> {self.getSquareIcon(square)}")

    def getSquareIcon(self, square):
        return " " if not square.hasPiece() else square.getPiece().getIcon()

    def printBoard(self):
        print("  ",end="")
        for i in range(8):
            print(f"{i}",end= " ")
        print("")
        for row in range(8):
            print(f"{row}", end= " ")
            for column in range(8):
                print(f"{self.getSquareIcon(self.squares[row][column])}",end=" ")
            print("")
        print("\n")

    def movePiece(self, origin, destiny):
        pieceToMove = origin.getPiece()
        self.squares[origin.getPosition().getX()][origin.getPosition().getY()].removePiece()
        self.squares[destiny.getPosition().getX()][destiny.getPosition().getY()].changePiece(f.createPiece(pieceToMove.getName(), pieceToMove.isWhite()))
