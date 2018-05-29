from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from BoardField import BoardField
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.etree import ElementTree as ET
from xml.dom import minidom
import os.path


import re

from xml.dom.minidom import Document
import sys

class ChessView(QGraphicsView):
    boardWidht = 8
    boardHeight = 8
    boardOffset = 20
    fieldWidht = 60
    fieldHeight = 60
    pathToXML = "gameRecord 0.xml"

    def __init__(self):
        QGraphicsView.__init__(self)

        # SIZES OF THE BOARD VIEW
        self.viewHeight = self.boardHeight * self.fieldHeight + 3 * self.boardOffset
        self.viewWidht = self.boardWidht * self.fieldWidht + 3 * self.boardOffset
        self.setFixedHeight(self.viewHeight )
        self.setFixedWidth(self.viewWidht )

        # SCENE AND ALL VISUAL THINGS
        self.scene = QGraphicsScene(0 , 0 , self.viewWidht - self.boardOffset, self.viewHeight - self.boardOffset)
        self.setScene(self.scene)
        self.generateBoard()
        self.addingGameBoardToScene()
        self.printBoard()
        self.debugPrint()

        # MOVE MANAGE
        self.moveFigure = [(-1,-1),(-1,-1)]
        self.playerRound = "white"
        self.readyToMoveFigure = False
        self.possibleMoves = []
        self.replayMode = False
        self.readedXML = None
        self.indexOfReplayNode = 0
        # CREATING NEW XML FILE THERE WE WILL SAVE THE DATA
        self.createXmlFile()

# --------------- Generating game ---------------------
    def resetTheGame(self):
        self.generateBoard()
        self.addingGameBoardToScene()

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

    def translateCordinatesIntoPositionInBoardArray(self, cordinates):
        xPos = cordinates[0]
        yPos = cordinates[1]
        return ( 7 - yPos)*self.boardWidht + xPos

    def getClickedFigurePosition(self):
        return(self.moveFigure)

    def debugPrint(self):
        print("\nDEBUG", end = "")
        for i in range(self.boardWidht):
            print("")
            for j in range(self.boardHeight):
                self.gameBoard[i*self.boardWidht + j].printXiFIsFigure()
        print("\nDEBUG")

    def addingGameBoardToScene(self):
        for i in range(self.boardWidht):
            for j in range(self.boardHeight):
                self.scene.addItem(self.gameBoard[i*self.boardWidht + j])


# --------------- Making move --------------------------------------
    def makeFigureMove(self, move):
        self.moveFigure = move
        print(self.moveFigure)
        self.gameBoard[0].moveTheFigureToPlace()

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

# --------------- Replay Mode on ---------------------------------
    def turnReplayMode(self):
        self.resetTheGame()
        self.replayMode = True
        self.readXmlFile()

    def getReplayMode(self):
        return self.replayMode

# -------------- XML File saving ------------------------
    def saveMoveToXml(self):
        tree = ET.parse(self.pathToXML)
        root = tree.getroot()
        child = ET.SubElement(root, "shift")
        moveToSave = str(self.moveFigure[0][0]) + "," + str(self.moveFigure[0][1]) + "," + str(self.moveFigure[1][0]) + "," + str(self.moveFigure[1][1])
        child.text = moveToSave
        tree.write(self.pathToXML)
        print(self.prettify(root))
        self.saveXmlAsPretty(root)

    def prettify(self, elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def saveXmlAsPretty(self, root):
        out = ET.tostring(root)
        dom = minidom.parseString(out)
        xmlFile = open("./gamePrettyRecords.xml", 'w')
        xmlFile.write(dom.toprettyxml())

# ---------------- creating xml file -----------------------------------
    def createXmlFile(self):
        trunk = Element('game')
        print(self.prettify(trunk))
        tree = ET.ElementTree(trunk)
        while(os.path.isfile(self.pathToXML)):
            newpathToXMLFile = self.getNumberToCreateNewXMLFile(self.pathToXML)
            self.pathToXML = newpathToXMLFile
        tree.write(self.pathToXML)

    def getNumberToCreateNewXMLFile(self, pathToXML):
        string = pathToXML
        numberOfFile = re.findall('\d+',string)
        indexOfNumber = string.find(numberOfFile[0])
        numberOfFile = numberOfFile[0]
        newNumberOfFile = int(numberOfFile) + 1
        newPathString = list(string)
        newPathString[indexOfNumber : indexOfNumber + len(numberOfFile)] = str(newNumberOfFile)
        newPathString = ''.join(newPathString)
        return newPathString

# --------------- Click next move from replay -----------------
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_R:
            if self.replayMode == True:
                try:
                    replayMove = self.getMoveFromXML()
                    replayMove = replayMove.split(',')
                    move = list(map(int, replayMove))
                    move = [(move[0], move[1]), (move[2],move[3])]
                    self.moveFigure = move
                    self.makeFigureMove(self.moveFigure)
                except:
                    pass
    def getMoveFromXML(self):
        try:
            actualMoveToReplay = self.readedXML[self.indexOfReplayNode].text
            self.indexOfReplayNode += 1
        except:
            actualMoveToReplay = None
            pass
        return actualMoveToReplay

    def readXmlFile(self):
        tree = ET.parse('gamePrettyRecords.xml')
        self.readedXML = tree.getroot()
