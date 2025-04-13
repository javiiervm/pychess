class Square:
    __slots__ = ('position', 'piece')  # Limit attributes

    def __init__(self, position, piece):
        self.position = position
        self.piece = piece

    def getPosition(self):
        return self.position

    def getPiece(self):
        if not self.hasPiece():
            return None
        return self.piece

    def hasPiece(self):
        return False if self.piece is None else True

    def removePiece(self):
        self.piece = None

    def changePiece(self, piece):
        self.removePiece()
        self.piece = piece
        if self.piece.getName() == "Pawn":
            self.piece.addMove()
        elif self.piece.getName() == "Rook" or self.piece.getName() == "King":
            self.piece.disableCastling()