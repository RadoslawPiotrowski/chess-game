from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from BoardField import BoardField

class ChessView(QGraphicsView):
    boardWidht = 8
    boardHeight = 8
    boardOffset = 20
    fieldWidht = 60
    fieldHeight = 60
    def __init__(self):
        QGraphicsView.__init__(self)

        # SIZES OF THE BOARD VIEW

        self.viewHeight = self.boardHeight * self.fieldHeight + 3 * self.boardOffset
        self.viewWidht = self.boardWidht * self.fieldWidht + 3 * self.boardOffset
        self.setFixedHeight(self.viewHeight )
        self.setFixedWidth(self.viewWidht )

        # SCENE AND ALL VISUAL THINGS

        self.scene = QGraphicsScene(0 , 0 , self.viewWidht - self.boardOffset, self.viewHeight - self.boardOffset)
        # self.view = QGraphicsView(self.scene)
        self.setScene(self.scene)
        self.generateBoard()
        self.addingGameBoardToScene()
        self.printBoard()

        # MOVE MANAGE

        self.moveFigure = [(-1,-1),(-1,-1)]
        self.playerRound = "white"
        self.figureChosen = False
        self.possibleMoves = []

    def highlightPossibleFieldMoves(self):
        for position in self.possibleMoves:
            arrayPosition = self.translateCordinatesIntoPositionInBoardArray(position)
            self.gameBoard[arrayPosition].setHighlightPossibleMoveFields()
            self.gameBoard[arrayPosition].updateSelf()

    def notHighlightAllFields(self):
        for i in range(self.boardWidht):
            for j in range(self.boardHeight):
                if self.gameBoard[i*self.boardWidht + j].getHighlightField():
                    self.gameBoard[i*self.boardWidht + j].highlightField = False
                    self.gameBoard[i*self.boardWidht + j].updateSelf()

    def translateCordinatesIntoPositionInBoardArray(self, cordinates):
        xPos = cordinates[0]
        yPos = cordinates[1]
        return ( 7 - yPos)*self.boardWidht + xPos

    def getClickedFigurePosition(self):
        return(self.moveFigure)

    def addingGameBoardToScene(self):
        for i in range(self.boardWidht):
            for j in range(self.boardHeight):
                self.scene.addItem(self.gameBoard[i*self.boardWidht + j])

    def generateBoard(self):
        self.gameBoard = []
        for i in range(self.boardWidht):
            for j in range(self.boardHeight):
                color = self.generateColorOfField(i,j)
                self.gameBoard.append(BoardField(j * self.fieldWidht + self.boardOffset,
                                                 i * self.fieldHeight + self.boardOffset,
                                                 color,
                                                 self.fieldWidht,
                                                 self.boardOffset,
                                                 None,
                                                 self))

    def generateColorOfField(self, xindex, yindex):
        if (xindex + yindex) % 2 == 0:
            color = QColor(255, 255, 255)
        else:
            color = QColor(150, 150, 150)
        return color

    def printBoard(self):
        for i in range(self.boardWidht):
            print("")
            for j in range(self.boardHeight):
                print(self.gameBoard[i*self.boardWidht + j].getBoardPostion(), end = " ")
                print(self.gameBoard[i*self.boardWidht + j].getFieldPosition(), end = " ")
