from PyQt5.QtWidgets import QGraphicsItem
import copy

class Figure():
    def __init__(self, figureColor, boardPostion):
        self.figureColor = figureColor
        self.boardPosition = boardPostion

    def translateFieldPositionIntoPositionInBoardArray(self):
        xPos = ord(self.boardPosition[0]) - 65
        yPos = ord(self.boardPosition[1]) - 49
        return(xPos,yPos)

    #cordinates = (x,y)
    def translateCordinatesIntoPositionInBoardArray(self, cordinates):
        xPos = cordinates[0]
        yPos = cordinates[1]
        return ( 7 - yPos)*8 + xPos
    #positionInBoardArray = positionInGameBoardList
    def translatePositionInBoardArrayIntoCordinates(self, positionInBoardArray):
        xPos = positionInBoardArray % 8
        yPos = 7 - (positionInBoardArray // 8)
        return([xPos, yPos])

    def getFigureColor(self):
        return self.figureColor

    def getFigureBoardPosition(self):
        return self.boardPosition



    def checkIfIsFree(self, fieldPosition , gameBoard):
        takenFields = self.getTakenFields(gameBoard)
        if fieldPosition in takenFields:
            fieldIsFree = False
        else:
            fieldIsFree = True
        return fieldIsFree

    def getTakenFields(self, gameBoard):
        occupiedField = []
        for i in range(8):
            for j in range(8):
                position = i*8 + j
                if gameBoard[position].figureChild != None:
                    position = self.translatePositionInBoardArrayIntoCordinates(position)
                    occupiedField.append(position)
        return occupiedField

    def checkIfEnemy(self, fieldPos, gameBoard):
        enemyOnField = False
        if not self.checkIfIsFree(fieldPos,gameBoard):
            if not self.isAllyOnField(fieldPos, gameBoard):
                enemyOnField = True
        return enemyOnField

    def isBoardField(self, fieldPos):
        isField = True
        if fieldPos[0] < 0 or fieldPos[0] > 7:
            isField = False
        elif fieldPos[1] < 0 or fieldPos[1] > 7:
            isField = False
        return isField

    # fieldPos [x,y]
    def getVerticalAndHorizontalFigureMoves(self, fieldPos, gameBoard):
        attackingAboveFields = self.setVerticalFieldsForMovePossibility(fieldPos, gameBoard, 1)       # checking above
        attackingBelowFields = self.setVerticalFieldsForMovePossibility(fieldPos, gameBoard, -1)
        attackingRightFields = self.setHorizontalFieldsForMovePossibility(fieldPos, gameBoard, 1)
        attackingLeftFields = self.setHorizontalFieldsForMovePossibility(fieldPos, gameBoard, -1)
        return (attackingAboveFields + attackingBelowFields + attackingLeftFields + attackingRightFields)

    def getDiagonalFigureMoves(self, fieldPos, gameBoard):
        attackingUpperLeftDiagonal = self.setDiagonalFieldsForMovePossibility(fieldPos, gameBoard, ([-1,1]))
        attackingUpperRightDiagonal = self.setDiagonalFieldsForMovePossibility(fieldPos, gameBoard, ([1,1]))
        attackingBottomLeftDiagonal = self.setDiagonalFieldsForMovePossibility(fieldPos, gameBoard, ([-1,-1]))
        attackingBottomRightDiagonal = self.setDiagonalFieldsForMovePossibility(fieldPos, gameBoard, ([1,-1]))
        return(attackingBottomLeftDiagonal + attackingBottomRightDiagonal + attackingUpperLeftDiagonal + attackingUpperRightDiagonal)

    def getKnightFieldsForMovePossibility(self, fieldPos, gameBoard):
        fieldPossibleToMove = []
        allKnightAvaibleMoves = [[2,1],[2,-1],[1,2],[1,-2],[-1,2],[-1,-2],[-2,1],[-2,-1]]
        for knightMove in allKnightAvaibleMoves:
            print(knightMove)
            fieldToCheck = copy.copy(fieldPos)
            fieldToCheck[0] += knightMove[0]
            fieldToCheck[1] += knightMove[1]
            if self.isInBoardAndHaveNoFigure(fieldToCheck, gameBoard):
                fieldPossibleToMove.append(fieldToCheck)
            elif self.isInBoardAndEnemyOnField(fieldToCheck, gameBoard):
                fieldPossibleToMove.append(fieldToCheck)
            else:
                pass
        return fieldPossibleToMove
    # fieldPos [x,y], direction is int 1(right) or -1(left)
    def setVerticalFieldsForMovePossibility(self, fieldPos, gameBoard, direction):
        fieldPossibleToMove = []
        fieldToCheck = copy.copy(fieldPos)
        fieldToCheck[1] += direction
        while(self.isInBoardAndHaveNoFigure(fieldToCheck, gameBoard)):
            fieldPossibleToMove.append(copy.copy(fieldToCheck))
            fieldToCheck[1] += direction
        if self.isInBoardAndEnemyOnField(fieldToCheck, gameBoard):
            fieldPossibleToMove.append(fieldToCheck)
        else:
            pass
        return fieldPossibleToMove

    def setHorizontalFieldsForMovePossibility(self, fieldPos, gameBoard, direction):
        fieldPossibleToMove = []
        fieldToCheck = copy.copy(fieldPos)
        fieldToCheck[0] += direction
        while(self.isInBoardAndHaveNoFigure(fieldToCheck, gameBoard)):
            fieldPossibleToMove.append(copy.copy(fieldToCheck))
            fieldToCheck[0] += direction
        if self.isInBoardAndEnemyOnField(fieldToCheck, gameBoard):
            fieldPossibleToMove.append(fieldToCheck)
        else:
            pass
        return fieldPossibleToMove

    # fieldPos [x,y], direction is list [a,b] a -> left(-1)/right(1), b -> down(-1),up(1)
    def setDiagonalFieldsForMovePossibility(self, fieldPos, gameBoard, direction):
        fieldPossibleToMove = []
        fieldToCheck = copy.copy(fieldPos)
        fieldToCheck[0] += direction[0]
        fieldToCheck[1] += direction[1]
        while(self.isInBoardAndHaveNoFigure(fieldToCheck, gameBoard)):
            fieldPossibleToMove.append(copy.copy(fieldToCheck))
            fieldToCheck[0] += direction[0]
            fieldToCheck[1] += direction[1]
        if self.isInBoardAndEnemyOnField(fieldToCheck, gameBoard):
            fieldPossibleToMove.append(fieldToCheck)
        else:
            pass
        return fieldPossibleToMove

    def getAllLineralDirections(self,fieldPos, gameBoard):
        verticalAndHorizontalMoves = self.getVerticalAndHorizontalFigureMoves(fieldPos,gameBoard)
        diagonalMoves = self.getDiagonalFigureMoves(fieldPos, gameBoard)
        return (verticalAndHorizontalMoves + diagonalMoves)

    def isCordinatesCorrect(self, fieldPosition):
        fieldExists = True
        if fieldPosition[0] < 0 or fieldPosition[1] < 0 or 7 < fieldPosition[0] or 7 < fieldPosition[1]:
            fieldExists = False
        return fieldExists

    def isInBoardAndHaveNoFigure(self, fieldPosition, gameBoard):
        isPossibleToAdd = False
        idxOfField = self.translateCordinatesIntoPositionInBoardArray(fieldPosition)
        if(self.isCordinatesCorrect(fieldPosition) and (gameBoard[idxOfField].isHavingFigure() == False)):
            isPossibleToAdd = True
        return isPossibleToAdd

    def isAllyOnField(self, fieldPosition, gameBoard):
        arrayPosition = self.translateCordinatesIntoPositionInBoardArray(fieldPosition)
        if gameBoard[arrayPosition].getFigureColor() == self.getFigureColor():
            allyOnField = True
        else:
            allyOnField = False
        return allyOnField

    #we already know there is figure on this field
    def isInBoardAndEnemyOnField(self, fieldPos, gameBoard):
        isEnemyOnField = False
        if (self.isCordinatesCorrect(fieldPos) == True and self.isAllyOnField(fieldPos, gameBoard) == False):
            isEnemyOnField = True
        return isEnemyOnField




class Pawn(Figure):
    def __init__(self,figureColor, boardPostion):
        super().__init__(figureColor = figureColor, boardPostion = boardPostion)
        self.firstMoveDone = False
        self.movePosibilities = None
        self.attackFields = None

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard):
        self.setMovePosibilities(gameBoard)

    def checkIfFirstMoveDone(self):
        if self.figureColor == "white":
            if self.boardPosition[1] == "2":
                self.firstMoveDone = False
            else: self.firstMoveDone = True
        elif self.figureColor == "black":
            if self.boardPosition[1] == "7":
                self.firstMoveDone = False
            else: self.firstMoveDone = True

    def setAttackFields(self):
        xPos, yPos = self.translateFieldPositionIntoPositionInBoardArray()
        attackFields = []
        if self.figureColor == "white":
            if xPos == 0:
                attackFields.append([xPos + 1, yPos + 1])
            elif xPos == 7:
                attackFields.append([xPos - 1, yPos + 1])
            else:
                attackFields.append([xPos + 1, yPos + 1])
                attackFields.append([xPos - 1, yPos + 1])
        elif self.figureColor == "black":
            if xPos == 0:
                attackFields.append([xPos + 1, yPos - 1])
            elif xPos == 7:
                attackFields.append([xPos - 1, yPos - 1])
            else:
                attackFields.append([xPos + 1, yPos - 1])
                attackFields.append([xPos - 1, yPos - 1])
        self.attackFields = attackFields

    def setMovePosibilities(self, gameBoard):
        xPos, yPos = self.translateFieldPositionIntoPositionInBoardArray()
        movePosibility = []
        self.setAttackFields()
        self.checkIfFirstMoveDone()
        if self.figureColor == "white":
            if yPos < 7:
                for atackField in self.attackFields:
                    if self.checkIfEnemy(atackField, gameBoard):
                        movePosibility.append(atackField)
                if self.checkIfIsFree([xPos,yPos +1],gameBoard):
                    movePosibility.append([xPos,yPos + 1])
            if not self.firstMoveDone:
                if self.checkIfIsFree([xPos,yPos +2],gameBoard):
                    movePosibility.append([xPos,yPos + 2])
        elif self.figureColor == "black":
            if yPos > 0:
                for atackField in self.attackFields:
                    if self.checkIfEnemy(atackField, gameBoard):
                        movePosibility.append(atackField)
                if self.checkIfIsFree([xPos,yPos -1],gameBoard):
                    movePosibility.append([xPos,yPos - 1])
            if not self.firstMoveDone:
                if self.checkIfIsFree([xPos,yPos -2],gameBoard):
                    movePosibility.append([xPos,yPos - 2])
        self.movePosibilities = movePosibility
        return movePosibility

    def getPath(self):
        figurePath = None
        if self.figureColor == "white":
            figurePath = "./Figure/White/pawn.png"
        elif self.figureColor == "black":
            figurePath = "./Figure/Black/pawn.png"
        return figurePath

class King(Figure):
    def __init__(self,figureColor, boardPostion):
        super().__init__(figureColor = figureColor, boardPostion = boardPostion)
        self.firstMoveDone = False
        self.movePosibilities = None
        self.attackFields = None
        self.ischecked = False

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard):
        self.setMovePosibilities(gameBoard)

    def checkIfFirstMoveDone(self):
        pass

    def setAttackFields(self):
        xPos, yPos = self.translateFieldPositionIntoPositionInBoardArray()
        attackFields = []
        yCheckingField = yPos + 2
        for i in range (3):
            xCheckingField = xPos - 2
            yCheckingField -= 1
            for j in range (3):
                xCheckingField += 1
                if self.isBoardField((xCheckingField, yCheckingField)):
                    attackFields.append([xCheckingField, yCheckingField])
        self.attackFields = attackFields

    def setMovePosibilities(self, gameBoard):
        movePosibility = []
        self.setAttackFields()
        for atackingField in self.attackFields:
            if self.checkIfIsFree(atackingField,gameBoard):
                movePosibility.append(atackingField)
            else:
                if not self.isAllyOnField((atackingField), gameBoard):
                    movePosibility.append(atackingField)
        self.movePosibilities = movePosibility

    def getPath(self):
        figurePath = None
        if self.figureColor == "white":
            figurePath = "./Figure/White/king.png"
        elif self.figureColor == "black":
            figurePath = "./Figure/Black/king.png"
        return figurePath

class Queen(Figure):
    def __init__(self,figureColor, boardPostion):
        super().__init__(figureColor = figureColor, boardPostion = boardPostion)
        self.movePosibilities = None
        self.attackFields = None

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard):
        self.setMovePosibilities(gameBoard)

    def setAttackFields(self, gameBoard):
        xPos, yPos = self.translateFieldPositionIntoPositionInBoardArray()
        attackFields = self.getAllLineralDirections([xPos, yPos], gameBoard)
        self.attackFields = attackFields
        return attackFields

    def setMovePosibilities(self, gameBoard):
        movePosibility = self.setAttackFields(gameBoard)
        self.movePosibilities = movePosibility

    def getPath(self):
        figurePath = None
        if self.figureColor == "white":
            figurePath = "./Figure/White/queen.png"
        elif self.figureColor == "black":
            figurePath = "./Figure/Black/queen.png"
        return figurePath

class Knight(Figure):
    def __init__(self,figureColor, boardPostion):
        super().__init__(figureColor = figureColor, boardPostion = boardPostion)
        self.firstMoveDone = False
        self.movePosibilities = None
        self.attackFields = None

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard):
        self.setMovePosibilities(gameBoard)

    def setAttackFields(self, gameBoard):
        xPos, yPos = self.translateFieldPositionIntoPositionInBoardArray()
        attackFields = self.getKnightFieldsForMovePossibility([xPos, yPos], gameBoard)
        self.attackFields = attackFields
        return attackFields

    def setMovePosibilities(self, gameBoard):
        movePosibility = self.setAttackFields(gameBoard)
        self.movePosibilities = movePosibility

    def getPath(self):
        figurePath = None
        if self.figureColor == "white":
            figurePath = "./Figure/White/knight.png"
        elif self.figureColor == "black":
            figurePath = "./Figure/Black/knight.png"
        return figurePath

class Rook(Figure):
    def __init__(self,figureColor, boardPostion):
        super().__init__(figureColor = figureColor, boardPostion = boardPostion)
        self.firstMoveDone = False
        self.movePosibilities = None
        self.attackFields = None

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard):
        self.setMovePosibilities(gameBoard)

    def setAttackFields(self, gameBoard):
        xPos, yPos = self.translateFieldPositionIntoPositionInBoardArray()
        attackFields = self.getVerticalAndHorizontalFigureMoves([xPos, yPos], gameBoard)
        self.attackFields = attackFields
        return attackFields

    def setMovePosibilities(self, gameBoard):
        movePosibility = self.setAttackFields(gameBoard)
        self.movePosibilities = movePosibility

    def getPath(self):
        figurePath = None
        if self.figureColor == "white":
            figurePath = "./Figure/White/rook.png"
        elif self.figureColor == "black":
            figurePath = "./Figure/Black/rook.png"
        return figurePath

class Bishop(Figure):
    def __init__(self,figureColor, boardPostion):
        super().__init__(figureColor = figureColor, boardPostion = boardPostion)
        self.firstMoveDone = False
        self.movePosibilities = None
        self.attackFields = None

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard):
        self.setMovePosibilities(gameBoard)

    def setAttackFields(self, gameBoard):
        xPos, yPos = self.translateFieldPositionIntoPositionInBoardArray()
        attackFields = self.getDiagonalFigureMoves([xPos, yPos], gameBoard)
        self.attackFields = attackFields
        return attackFields

    def setMovePosibilities(self, gameBoard):
        movePosibility = self.setAttackFields(gameBoard)
        self.movePosibilities = movePosibility

    def getPath(self):
        figurePath = None
        if self.figureColor == "white":
            figurePath = "./Figure/White/bishop.png"
        elif self.figureColor == "black":
            figurePath = "./Figure/Black/bishop.png"
        return figurePath
