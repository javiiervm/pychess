from abc import ABC, abstractmethod

# ========================== [ABSTRACT PIECE CLASS] ========================== #

class Piece(ABC):
    __slots__ = ('name', 'icon', 'white', 'moves')  # Limit attributes

    def __init__(self, name, icon, white):
        self.name = name
        self.icon = icon
        self.white = white
        self.moves = 0

    def getName(self):
        return self.name

    def getIcon(self):
        return self.icon

    def isWhite(self):
        return self.white

    def getMoves(self):
        return self.moves

    def printData(self):
        return f"{"White" if self.isWhite() else "Black"} {self.getName()} ({self.getIcon()})"

    def addMove(self):
        self.moves = self.moves + 1

    def inBoard(self, squareToCheck):
        if not ((squareToCheck.getPosition().getX() < 0 or squareToCheck.getPosition().getX() > 7) and (squareToCheck.getPosition().getY() < 0 or squareToCheck.getPosition().getY() > 7)):
            return True
        return False

    @abstractmethod
    def possibleMoves(self, board, position):
        pass
