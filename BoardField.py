from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtCore
from Figures import *
from PyQt5.QtGui import QPixmap
from enum import Enum

class FiguresPoints(Enum):
    Pawn = 1
    Knight = 3
    Bishop = 3
    Rook = 5
    Queen = 9
    King = 20

class BoardField(QGraphicsItem):
    def __init__(self, xPosition, yPosition, color = None, squareSize = None, boardOffset = None, figureChild = None, parent = None):
        super(QGraphicsItem, self).__init__()
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.fieldColor = color
        self.squareSize = squareSize
        self.fieldPoint = 0
        self.boardOffset = boardOffset
        self.figureChild = figureChild
        self.gameHandler = parent
        self.highlightField = False
        self.pressed = False
        self.rectF = QtCore.QRectF(self.xPosition, self.yPosition, self.squareSize, self.squareSize)
        self.boardPosition = self.setBoardPosition()
        self.addFiguresToBoard()

    def __del__(self):
        print ('died')

    def getFieldPoint(self):
        return self.fieldPoint

    def updateFieldPoint(self):
        if self.figureChild != None:
            points = self.getPointForField(type(self.figureChild).__name__)
            self.fieldPoint = points
        else:
            self.fieldPoint = 0

    def getPointForField(self, figureName):
        point = FiguresPoints[figureName].value
        return point

    def getHighlightField(self):
        return self.highlightField

    def addFiguresToBoard(self):
        self.addWhiteFigures()
        self.addBlackFigures()

    def addWhiteFigures(self):
        if self.fieldNumber == "2":
            self.addPawn("white")
            pass
        elif self.boardPosition == "D1":
            self.addQueen("white")
        elif self.boardPosition == "E1":
            self.addKing("white")
        elif self.boardPosition == "A1" or self.boardPosition == "H1":
            self.addRook("white")
        elif self.boardPosition == "B1" or self.boardPosition == "G1":
            self.addKnight("white")
        elif self.boardPosition == "C1" or self.boardPosition == "F1":
            self.addBishop("white")

    def addBlackFigures(self):
        if self.fieldNumber == "7":
            self.addPawn("black")
            pass
        elif self.boardPosition == "D8":
            self.addQueen("black")
        elif self.boardPosition == "E8":
            self.addKing("black")
        elif self.boardPosition == "A8" or self.boardPosition == "H8":
            self.addRook("black")
        elif self.boardPosition == "B8" or self.boardPosition == "G8":
            self.addKnight("black")
        elif self.boardPosition == "C8" or self.boardPosition == "F8":
            self.addBishop("black")

    def addKnight(self, color):
        self.figureChild = Knight(color, self.boardPosition)

    def addKing(self, color):
        self.figureChild = King(color, self.boardPosition)

    def addQueen(self, color):
        self.figureChild = Queen(color, self.boardPosition)

    def addBishop(self, color):
        self.figureChild = Bishop(color, self.boardPosition)

    def addRook(self, color):
        self.figureChild = Rook(color, self.boardPosition)

    def addPawn(self, color):
        self.figureChild = Pawn(color, self.boardPosition)

    def boundingRect(self):
        return self.rectF

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        if self.gameHandler.getReplayMode() == False and self.gameHandler.itIsPlayerMove() == True:
            if self.isItPlayersFigure() and self.gameHandler.readyToMoveFigure == False:
                self.chooseMovingFigure()
            elif self.isItPlayersFigure() and self.gameHandler.readyToMoveFigure == True:            #kliknięta inna nasza figura
                self.changeMovingFigure()
            elif self.isItPlayersFigure() == False and self.gameHandler.readyToMoveFigure == True:                                             #kliknięte odpowiednie pole
                self.gameHandler.readyToMoveFigure = False
                self.saveTheSourceMove()
                if self.moveIsValid():
                    self.chooseMovingDestination()
                else:
                    self.gameHandler.readyToMoveFigure = True
                    print("NIE WŁAŚCIWY RUCH")
        # self.gameHandler.debugPrint()
        self.update()

    def chooseMovingDestination(self):
        self.changeRound()
        self.moveTheFigureToPlace()
        self.gameHandler.refreshPlayerPossibleMoves()
        self.gameHandler.saveMoveToXml()
        self.resetFigureMoveArray()
        self.gameHandler.notHighlightAllFields()

        #added staff
        self.gameHandler.debugPrint()
        self.gameHandler.setAvaibleMovesWithPoints(self.gameHandler.getAllTheMovesWithPoints())

    def changeMovingFigure(self):
        self.gameHandler.notHighlightAllFields()
        self.chooseMovingFigure()

    def chooseMovingFigure(self):
        self.gameHandler.readyToMoveFigure = True
        self.saveTheSourceMove()
        self.figureChild.refreshFigureMovePosibilities(self.gameHandler.gameBoard)
        self.gameHandler.possibleMoves = self.figureChild.getMovePosibilities()
        self.gameHandler.highlightPossibleFieldMoves()

    def saveTheSourceMove(self):
        source = self.translateFieldPositionIntoCordinates()
        if self.gameHandler.readyToMoveFigure == True:
            self.gameHandler.moveFigure[0] = source
        elif self.gameHandler.readyToMoveFigure == False:
            self.gameHandler.moveFigure[1] = source

    def isHavingFigure(self):
        figureOnField = False
        if self.figureChild != None:
            figureOnField = True
        return figureOnField

    def isItPlayersFigure(self):
        playerColor = self.gameHandler.playerRound
        posibleToChose = False
        if self.figureChild != None:
            if playerColor == self.figureChild.getFigureColor():
                posibleToChose = True
            else:
                posibleToChose = False
        return posibleToChose

    def setHighlightPossibleMoveFields(self):
        self.highlightField = True

    def moveIsValid(self):
        validMove = False
        verifiedField = self.gameHandler.moveFigure[1]
        verifiedField = list(verifiedField)
        movingFigure = self.gameHandler.moveFigure[0]
        movingFigure = self.translateCordinatesIntoPositionInBoardArray(movingFigure)
        if verifiedField in self.gameHandler.gameBoard[movingFigure].figureChild.getMovePosibilities():
            validMove = True
        return validMove

    def changeRound(self):
        if self.gameHandler.playerRound == "white":
            self.gameHandler.playerRound = "black"
        elif self.gameHandler.playerRound == "black":
            self.gameHandler.playerRound = "white"


    def moveTheFigureToPlace(self):
        figureMove = self.gameHandler.moveFigure
        initialField = self.translateCordinatesIntoPositionInBoardArray(figureMove[0])
        terminalField = self.translateCordinatesIntoPositionInBoardArray(figureMove[1])
        self.gameHandler.gameBoard[terminalField].figureChild = self.gameHandler.gameBoard[initialField].figureChild
        self.gameHandler.gameBoard[terminalField].updateFigurePosition()
        self.gameHandler.gameBoard[initialField].figureChild = None
        self.gameHandler.gameBoard[terminalField].figureChild.refreshFigureMovePosibilities(self.gameHandler.gameBoard)
        self.gameHandler.gameBoard[initialField].updateSelf()
        self.gameHandler.gameBoard[terminalField].updateSelf()

    def translateCordinatesIntoPositionInBoardArray(self, cordinates):
        xPos = cordinates[0]
        yPos = cordinates[1]
        return ( 7 - yPos)*self.gameHandler.boardWidht + xPos

    def resetFigureMoveArray(self):
        self.gameHandler.moveFigure = [(-1,-1),(-1,-1)]

    def checkIfNotTheSameColor(self, figureMove):
        terminalField = self.translateCordinatesIntoPositionInBoardArray(figureMove[1])
        if self.gameHandler.gameBoard[terminalField].figureChild != None:
            if self.gameHandler.gameBoard[terminalField].figureChild.getFigureColor() != self.gameHandler.playerRound:
                possibilityOfMove = True
            else:
                possibilityOfMove = False
        else:
            possibilityOfMove = True
        return possibilityOfMove

    def setBoardPosition(self):
        self.boardSize = 8 * self.squareSize + 2 * self.boardOffset
        self.fieldLetter = chr((self.xPosition) // self.squareSize + 65)
        self.fieldNumber = str((self.boardSize - self.yPosition) // self.squareSize)
        fieldCode = self.fieldLetter + self.fieldNumber
        return fieldCode

    def translateFieldPositionIntoCordinates(self):
        xPos = self.xPosition // self.squareSize
        yPos = (self.boardSize - self.squareSize - self.yPosition) // self.squareSize
        return(xPos, yPos)

    def getBoardPosition(self):
        return self.boardPosition

    def getFigureColor(self):
        return self.figureChild.getFigureColor()

    def getFieldPosition(self):
        return (self.xPosition , self.yPosition)

    def paint(self, painter, QStyleOptionGraphicsItem, widget = None):
        if self.highlightField:
            painter.fillRect(self.xPosition, self.yPosition,self.squareSize,self.squareSize, self.fieldColor.darker(130))
        else:
            painter.fillRect(self.xPosition, self.yPosition,self.squareSize,self.squareSize, self.fieldColor)
        if self.figureChild != None:
            try:
                icon = QPixmap(self.figureChild.getPath())
                painter.drawPixmap(self.xPosition, self.yPosition,self.squareSize,self.squareSize,icon)
            except:
                pass
        if(self.pressed):
            painter.fillRect(self.xPosition, self.yPosition,self.squareSize,self.squareSize, QtCore.Qt.black)

    def updateSelf(self):
        self.updateFieldPoint()
        self.update()

    def updateFigurePosition(self):
        if self.figureChild.getFigureBoardPosition() != self.boardPosition:
            self.figureChild.boardPosition = self.boardPosition

    def printXiFIsFigure(self):
        if self.figureChild == None:
            print(" ", end= " ")
        else:
            print("X", end= " ")
