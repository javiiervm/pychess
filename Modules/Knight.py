import Piece as p
import Position as pos

# ========= [Knight] ========= #

class Knight(p.Piece):
    def __init__(self, white):
        super().__init__("Knight", "♞" if not white else "♘", white)

    def possibleMoves(self, board, position):
        # List of the possible squares the pawn can move to
        possibles = []

        # Iterate over the board to check for available squares to move to
        squareToCheck = board.findSquare(pos.Position(position.getX() - 2, position.getY() - 1))
        if not (squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY()):
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                else:
                    if self.isWhite() != squareToCheck.getPiece().isWhite():
                        possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() - 2, position.getY() + 1))
        if not (squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY()):
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                else:
                    if self.isWhite() != squareToCheck.getPiece().isWhite():
                        possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() + 2, position.getY() - 1))
        if not (squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY()):
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                else:
                    if self.isWhite() != squareToCheck.getPiece().isWhite():
                        possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() + 2, position.getY() + 1))
        if not (squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY()):
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                else:
                    if self.isWhite() != squareToCheck.getPiece().isWhite():
                        possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() - 1, position.getY() + 2))
        if not (squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY()):
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                else:
                    if self.isWhite() != squareToCheck.getPiece().isWhite():
                        possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() + 1, position.getY() + 2))
        if not (squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY()):
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                else:
                    if self.isWhite() != squareToCheck.getPiece().isWhite():
                        possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() - 1, position.getY() - 2))
        if not (squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY()):
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                else:
                    if self.isWhite() != squareToCheck.getPiece().isWhite():
                        possibles.append(squareToCheck)

        squareToCheck = board.findSquare(pos.Position(position.getX() + 1, position.getY() - 2))
        if not (squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY()):
            if self.inBoard(squareToCheck):
                if not squareToCheck.hasPiece():
                    possibles.append(squareToCheck)
                else:
                    if self.isWhite() != squareToCheck.getPiece().isWhite():
                        possibles.append(squareToCheck)

        return possibles