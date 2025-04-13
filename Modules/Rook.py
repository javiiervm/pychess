import Piece as p
import Position as pos

# ========= [Rook] ========= #

class Rook(p.Piece):
    def __init__(self, white):
        super().__init__("Rook", "♜" if not white else "♖", white)
        self.castling = True

    def possibleMoves(self, board, position):
        # List of the possible squares the pawn can move to
        possibles = []

        # A Rook can move to any square in horizontal
        for i in range(1, 8):
                squareToCheck = board.findSquare(pos.Position(position.getX(), position.getY() + i))
                if squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY():
                    break
                if self.inBoard(squareToCheck):
                    if not squareToCheck.hasPiece():
                        possibles.append(squareToCheck)
                    else:
                        if self.isWhite() != squareToCheck.getPiece().isWhite():
                            possibles.append(squareToCheck)
                            break
                        else:
                            break
                else:
                    break
        for i in range(1, 8):
                squareToCheck = board.findSquare(pos.Position(position.getX(), position.getY() - i))
                if squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY():
                    break
                if self.inBoard(squareToCheck):
                    if not squareToCheck.hasPiece():
                        possibles.append(squareToCheck)
                    else:
                        if self.isWhite() != squareToCheck.getPiece().isWhite():
                            possibles.append(squareToCheck)
                            break
                        else:
                            break
                else:
                    break
        for i in range(1, 8):
                squareToCheck = board.findSquare(pos.Position(position.getX() + i, position.getY()))
                if squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY():
                    break
                if self.inBoard(squareToCheck):
                    if not squareToCheck.hasPiece():
                        possibles.append(squareToCheck)
                    else:
                        if self.isWhite() != squareToCheck.getPiece().isWhite():
                            possibles.append(squareToCheck)
                            break
                        else:
                            break
                else:
                    break
        for i in range(1, 8):
                squareToCheck = board.findSquare(pos.Position(position.getX() - i, position.getY()))
                if squareToCheck.getPosition().getX() == position.getX() and squareToCheck.getPosition().getY() == position.getY():
                    break
                if self.inBoard(squareToCheck):
                    if not squareToCheck.hasPiece():
                        possibles.append(squareToCheck)
                    else:
                        if self.isWhite() != squareToCheck.getPiece().isWhite():
                            possibles.append(squareToCheck)
                            break
                        else:
                            break
                else:
                    break

        return possibles

    def disableCastling(self):
        self.castling = False

    def getCastling(self):
        return self.castling