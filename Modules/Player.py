class Player:
    __slots__ = ('name', 'white', 'piecesLeft', 'isCheck', 'isCheckMate')  # Limit attributes

    def __init__(self, name, white):
        self.name = name
        self.white = white
        self.piecesLeft = 16
        self.isCheck = False
        self.isCheckMate = False

    def getName(self):
        return self.name

    def isWhite(self):
        return self.white

    def getColor(self):
        return "White" if self.isWhite() else "Black"

    def getPiecesLeft(self):
        return self.piecesLeft

    def subsPiece(self):
        if self.getPiecesLeft() > 0:
            self.piecesLeft = self.getPiecesLeft() - 1

    def getCheck(self):
        return self.isCheck

    def getCheckMate(self):
        return self.isCheckMate

    def setCheckMate(self):
        self.isCheckMate = True

    def switchCheck(self):
        var = self.getCheck()
        self.isCheck = not var

    def turnMessage(self):
        return f"{self.getColor()} king turn!"

    def winMessage(self):
        return f"{self.getColor()} king {self.getName()} wins!"
