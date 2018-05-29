from PyQt5.QtWidgets import QGraphicsItem

class Figure():
    def __init__(self, figureColor, boardPostion):
        self.figureColor = figureColor
        self.boardPosition = boardPostion

    def translateBoardPositionIntoPositionInBoardArray(self):
        xPos = ord(self.boardPosition[0]) - 65
        yPos = ord(self.boardPosition[1]) - 49
        return(xPos,yPos)

    def translateCordinatesIntoPositionInBoardArray(self, cordinates):
        xPos = cordinates[0]
        yPos = cordinates[1]
        return ( 7 - yPos)*8 + xPos

    def getFigureColor(self):
        return self.figureColor

    def getFigureBoardPosition(self):
        return self.boardPosition

    def checkIfAllyOnField(self, fieldPosition, gameBoard):
        if gameBoard == None:
            allyOnField = True
        else:
            arrayPosition = self.translateCordinatesIntoPositionInBoardArray(fieldPosition)
            if gameBoard[arrayPosition].getFigureColor() == self.getFigureColor():
                allyOnField = True
            else:
                allyOnField = False
        return allyOnField

    def checkIfIsFree(self, fieldPosition , gameBoard):
        if gameBoard == None:
            fieldIsFree = True
        else:
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
                    position = self.translateFieldPositionIntoCordinates(position)
                    occupiedField.append(position)
        return occupiedField

    def translateFieldPositionIntoCordinates(self, positionInBoardArray):
        xPos = positionInBoardArray % 8
        yPos = 7 - (positionInBoardArray // 8)
        return([xPos, yPos])

    def checkIfEnemy(self, fieldPos, gameBoard):
        enemyOnField = False
        if gameBoard == None:
            enemyOnField = False
        else:
            if not self.checkIfIsFree(fieldPos,gameBoard):
                if not self.checkIfAllyOnField(fieldPos,gameBoard):
                    enemyOnField = True
        return enemyOnField

    def isBoardField(self, fieldPos):
        isField = True
        if fieldPos[0] < 0 or fieldPos[0] > 7:
            isField = False
        elif fieldPos[1] < 0 or fieldPos[1] > 7:
            isField = False
        return isField

    def checkVerticalFigureAttackFields(self, fieldPos, gameBoard):
        attackingVerticalFields = []
        upFieldsToCheck = 7 - fieldPos[1]
        yPos = fieldPos[1]
        for i in range(upFieldsToCheck):
            yPos += 1
            if self.checkIfIsFree((fieldPos[0], yPos), gameBoard):
                # print( " SPRAWDZAM ", end = " ")
                # print( fieldPos[0],yPos)
                attackingVerticalFields.append([fieldPos[0], yPos])
            # elif not self.checkIfIsFree((fieldPos[0], yPos), gameBoard):
            #     attackingVerticalFields.append([fieldPos[0], yPos])
            #     break
        yPos = fieldPos[1]
        # for j in range (fieldPos[1],0,-1):
        #     yPos -= 1
        #     if self.checkIfIsFree((fieldPos[0], yPos), gameBoard):
        #         attackingVerticalFields.append([fieldPos[0], yPos])
        #     else:
        #         attackingVerticalFields.append([fieldPos[0], yPos])
        #         break


class Pawn(Figure):
    def __init__(self,figureColor, boardPostion):
        super().__init__(figureColor = figureColor, boardPostion = boardPostion)
        self.firstMoveDone = False
        self.movePosibilities = self.setMovePosibilities()
        self.attackFields = self.setAttackFields()

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard = None):
        self.setMovePosibilities(gameBoard)
        # print(self.getMovePosibilities())

    def checkIfFirstMoveDone(self):
        # print("TU WBILEM")
        # print(self.boardPosition)
        if self.figureColor == "white":
            if self.boardPosition[1] == "2":
                self.firstMoveDone = False
            else: self.firstMoveDone = True
        elif self.figureColor == "black":
            if self.boardPosition[1] == "7":
                self.firstMoveDone = False
            else: self.firstMoveDone = True
        # print(self.firstMoveDone)

    def setAttackFields(self):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
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
        return attackFields

    def setMovePosibilities(self, gameBoard = None):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
        movePosibility = []
        # print("TUTAJ")
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
        self.movePosibilities = self.setMovePosibilities()
        self.attackFields = self.setAttackFields()
        self.ischecked = False

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard = None):
        self.setMovePosibilities(gameBoard)

    def checkIfFirstMoveDone(self):
        pass

    def setAttackFields(self):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
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
        return attackFields

    def setMovePosibilities(self, gameBoard = None):
        movePosibility = []
        self.setAttackFields()
        for atackingField in self.attackFields:
            if self.checkIfIsFree(atackingField,gameBoard):
                movePosibility.append(atackingField)
            else:
                if not self.checkIfAllyOnField((atackingField), gameBoard):
                    movePosibility.append(atackingField)
        self.movePosibilities = movePosibility
        return movePosibility

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
        self.movePosibilities = self.setMovePosibilities()
        self.attackFields = []

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard = None):
        self.setMovePosibilities(gameBoard)
        print(self.getMovePosibilities())

    def setAttackFields(self, gameBoard):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
        attackFields = []
        print("ATACK POSIBILITIS")
        self.checkVerticalFigureAttackFields((xPos,yPos),gameBoard)
        self.attackFields = attackFields
        return attackFields

    def setMovePosibilities(self, gameBoard = None):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
        movePosibility = []
        print("MOVE POSIBILITIS")
        self.setAttackFields(gameBoard)
        self.movePosibilities = movePosibility
        return movePosibility

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
        self.movePosibilities = self.setMovePosibilities()
        self.attackFields = self.setAttackFields()

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard = None):
        self.setMovePosibilities(gameBoard)
        print(self.getMovePosibilities())

    def checkIfFirstMoveDone(self):
        print("TU WBILEM")
        print(self.boardPosition)
        if self.figureColor == "white":
            if self.boardPosition[1] == "2":
                self.firstMoveDone = False
            else: self.firstMoveDone = True
        elif self.figureColor == "black":
            if self.boardPosition[1] == "7":
                self.firstMoveDone = False
            else: self.firstMoveDone = True
        print(self.firstMoveDone)

    def setAttackFields(self):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
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
        return attackFields

    def setMovePosibilities(self, gameBoard = None):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
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
            figurePath = "./Figure/White/knight.png"
        elif self.figureColor == "black":
            figurePath = "./Figure/Black/knight.png"
        return figurePath

class Rook(Figure):
    def __init__(self,figureColor, boardPostion):
        super().__init__(figureColor = figureColor, boardPostion = boardPostion)
        self.firstMoveDone = False
        self.movePosibilities = self.setMovePosibilities()
        self.attackFields = self.setAttackFields()

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard = None):
        self.setMovePosibilities(gameBoard)
        print(self.getMovePosibilities())

    def checkIfFirstMoveDone(self):
        print(self.boardPosition)
        if self.figureColor == "white":
            if self.boardPosition[1] == "2":
                self.firstMoveDone = False
            else: self.firstMoveDone = True
        elif self.figureColor == "black":
            if self.boardPosition[1] == "7":
                self.firstMoveDone = False
            else: self.firstMoveDone = True
        print(self.firstMoveDone)

    def setAttackFields(self):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
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
        return attackFields

    def setMovePosibilities(self, gameBoard = None):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
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
            figurePath = "./Figure/White/rook.png"
        elif self.figureColor == "black":
            figurePath = "./Figure/Black/rook.png"
        return figurePath

class Bishop(Figure):
    def __init__(self,figureColor, boardPostion):
        super().__init__(figureColor = figureColor, boardPostion = boardPostion)
        self.firstMoveDone = False
        self.movePosibilities = self.setMovePosibilities()
        self.attackFields = self.setAttackFields()

    def getattackFields(self):
        return self.attackFields

    def getMovePosibilities(self):
        return self.movePosibilities

    def refreshFigureMovePosibilities(self, gameBoard = None):
        self.setMovePosibilities(gameBoard)
        print(self.getMovePosibilities())

    def checkIfFirstMoveDone(self):
        print(self.boardPosition)
        if self.figureColor == "white":
            if self.boardPosition[1] == "2":
                self.firstMoveDone = False
            else: self.firstMoveDone = True
        elif self.figureColor == "black":
            if self.boardPosition[1] == "7":
                self.firstMoveDone = False
            else: self.firstMoveDone = True
        print(self.firstMoveDone)

    def setAttackFields(self):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
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
        return attackFields

    def setMovePosibilities(self, gameBoard = None):
        xPos, yPos = self.translateBoardPositionIntoPositionInBoardArray()
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
            figurePath = "./Figure/White/bishop.png"
        elif self.figureColor == "black":
            figurePath = "./Figure/Black/bishop.png"
        return figurePath
