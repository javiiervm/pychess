class Position:
    __slots__ = ('x', 'y')  # Limit attributes

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPos(self):
        return Position(self.getX(), self.getY())

    def printPos(self):
        return f"[{self.getX()}, {self.getY()}]"
