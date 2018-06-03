
class MoveWithPoint():
    def __init__(self, move, point):
        self.figureMove = move
        self.movePoint = point

    def getFigureMove(self):
        return self.figureMove

    def getMovePoint(self):
        return self.movePoint

    def getFigureMoveAndPoint(self):
        return (self.figureMove, self.movePoint)
