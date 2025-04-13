import Piece as p
import Position as pos

# ========= [King] ========= #

class King(p.Piece):
    def __init__(self, white):
        super().__init__("King", "♚" if not white else "♔", white)
        self.castling = True

    def possibleMoves(self, board, position):
        # List of the possible squares the pawn can move to
        possibles = []

        # King can move one square any direction
        squareToCheck = board.findSquare(pos.Position(position.getX() - 1, position.getY() - 1))
        if self.inBoard(squareToCheck):
            if not squareToCheck.hasPiece():
                possibles.append(squareToCheck)
            else:
                if self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() - 1, position.getY()))
        if self.inBoard(squareToCheck):
            if not squareToCheck.hasPiece():
                possibles.append(squareToCheck)
            else:
                if self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() - 1, position.getY() + 1))
        if self.inBoard(squareToCheck):
            if not squareToCheck.hasPiece():
                possibles.append(squareToCheck)
            else:
                if self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX(), position.getY() - 1))
        if self.inBoard(squareToCheck):
            if not squareToCheck.hasPiece():
                possibles.append(squareToCheck)
            else:
                if self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX(), position.getY() + 1))
        if self.inBoard(squareToCheck):
            if not squareToCheck.hasPiece():
                possibles.append(squareToCheck)
            else:
                if self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() + 1, position.getY() - 1))
        if self.inBoard(squareToCheck):
            if not squareToCheck.hasPiece():
                possibles.append(squareToCheck)
            else:
                if self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() + 1, position.getY()))
        if self.inBoard(squareToCheck):
            if not squareToCheck.hasPiece():
                possibles.append(squareToCheck)
            else:
                if self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() + 1, position.getY() + 1))
        if self.inBoard(squareToCheck):
            if not squareToCheck.hasPiece():
                possibles.append(squareToCheck)
            else:
                if self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

        return possibles

    def disableCastling(self):
        self.castling = False

    def getCastling(self):
        return self.castling