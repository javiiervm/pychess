import Piece as p
import Position as pos

# ========= [Pawn] ========= #

class Pawn(p.Piece):
    def __init__(self, white):
        super().__init__("Pawn", "♟" if not white else "♙", white)

    def possibleMoves(self, board, position):
        # List of the possible squares the pawn can move to
        possibles = []

        # Iterate over the board to check for available squares to move to
        if self.isWhite():
            # A pawn can move to the square in front of it
            squareToCheck = board.findSquare(pos.Position(position.getX() - 1, position.getY()))
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                #else:
                #    if self.isWhite() != squareToCheck.getPiece().isWhite():
                #        possibles.append(squareToCheck)

            # If it's the pawn first move, it can move two squares
            if self.getMoves() == 0:
                squareToCheck = board.findSquare(pos.Position(position.getX() - 2, position.getY()))
                squareToCheckAnterior = board.findSquare(pos.Position(position.getX() - 1, position.getY()))
                if self.inBoard(squareToCheck) and self.inBoard(squareToCheckAnterior):
                    if not squareToCheck.hasPiece() and not squareToCheckAnterior.hasPiece():
                        possibles.append(squareToCheck)

            # A pawn can eat diagonally on its left
            squareToCheck = board.findSquare(pos.Position(position.getX() - 1, position.getY() - 1))
            if self.inBoard(squareToCheck):
                if squareToCheck.hasPiece() and self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

            # A pawn can eat diagonally on its right
            squareToCheck = board.findSquare(pos.Position(position.getX() - 1, position.getY() + 1))
            if self.inBoard(squareToCheck):
                if squareToCheck.hasPiece() and self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)
        else:
            # A pawn can move to the square in front of it
            squareToCheck = board.findSquare(pos.Position(position.getX() + 1, position.getY()))
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                #else:
                #    if self.isWhite() != squareToCheck.getPiece().isWhite():
                #        possibles.append(squareToCheck)

            # If it's the pawn first move, it can move two squares
            if self.getMoves() == 0:
                squareToCheck = board.findSquare(pos.Position(position.getX() + 2, position.getY()))
                squareToCheckAnterior = board.findSquare(pos.Position(position.getX() + 1, position.getY()))
                if self.inBoard(squareToCheck) and self.inBoard(squareToCheckAnterior):
                    if not squareToCheck.hasPiece() and not squareToCheckAnterior.hasPiece():
                        possibles.append(squareToCheck)

            # A pawn can eat diagonally on its left
            squareToCheck = board.findSquare(pos.Position(position.getX() + 1, position.getY() - 1))
            if self.inBoard(squareToCheck):
                if squareToCheck.hasPiece() and self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

            # A pawn can eat diagonally on its right
            squareToCheck = board.findSquare(pos.Position(position.getX() + 1, position.getY() + 1))
            if self.inBoard(squareToCheck):
                if squareToCheck.hasPiece() and self.isWhite() != squareToCheck.getPiece().isWhite():
                    possibles.append(squareToCheck)

        return possibles

    def isValidMove(self):
        return None