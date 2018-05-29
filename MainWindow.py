from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor,QIcon
from PyQt5.QtWidgets import QWidget,QLineEdit, QFrame, QSplitter, QMessageBox,QVBoxLayout,QHBoxLayout, QGraphicsScene, QGraphicsView, QApplication, QPushButton, QGraphicsItem, QGraphicsPixmapItem
from PyQt5.QtCore import Qt
from ChessView import ChessView
from pynput.keyboard import Key, Listener

import sys

class MainWindow(QWidget):
    def __init__(self,widthX,HeightY, title):
        QWidget.__init__(self)
        self.windowSetup(widthX, HeightY, title)
        self.addButtonsAndLineEdit()
        self.setSceneAndView()
        self.windowArrangement()
        self.show()

    def windowArrangement(self):

        verticalBoxWithButtons = QVBoxLayout()
        buttonSplitter = QSplitter(Qt.Vertical)
        buttonSplitter.setFrameShape(QFrame.StyledPanel)
        buttonSplitter.addWidget(self.startButton)
        buttonSplitter.addWidget(self.endButton)
        buttonSplitter.addWidget(self.resetButton)
        buttonSplitter.addWidget(self.replayButton)
        buttonSplitter.addWidget(self.clientButton)
        buttonSplitter.addWidget(self.serwerButton)
        verticalBoxWithButtons.addWidget(buttonSplitter)

        verticalBoxWithScene = QVBoxLayout()
        verticalBoxWithScene.addWidget(self.view, alignment= Qt.AlignCenter)
        verticalBoxWithScene.addWidget(self.inputLineEdit)

        horizontalBoxWithAll = QHBoxLayout()
        horizontalBoxWithAll.addLayout(verticalBoxWithScene)
        horizontalBoxWithAll.addLayout(verticalBoxWithButtons)

        self.setLayout(horizontalBoxWithAll)

    def addButtonsAndLineEdit(self):

        self.startButton = QPushButton("START GAME")
        self.startButton.clicked.connect(self.startGame)

        self.endButton = QPushButton("END GAME")
        self.endButton.clicked.connect(self.endGame)

        self.resetButton = QPushButton("RESET GAME")
        self.resetButton.clicked.connect(self.resetGame)

        self.replayButton = QPushButton("REPLAY GAME")
        self.replayButton.clicked.connect(self.turnReplayON)

        self.clientButton = QPushButton("CLIENT")
        self.clientButton.clicked.connect(self.runClient)

        self.serwerButton = QPushButton("SERWER")
        self.serwerButton.clicked.connect(self.runSerwer)

        self.inputLineEdit = QLineEdit(self)

    def runClient(self):
        pass

    def runSerwer(self):
        pass

    def startGame(self):
        pass

    def turnReplayON(self):
        self.view.turnReplayMode()

    def endGame(self):
        pass

    def resetGame(self):
        self.view.resetTheGame()



    def setSceneAndView(self):
        self.view = ChessView()
        # self.scene = QGraphicsScene(self)
        # self.scene.setSceneRect(0, 0 , 480.0, 480.0)
        # self.view = QGraphicsView(self.scene, self)

    def windowSetup(self, widthX, HeightX, title):
        self.resize(widthX,HeightX)
        self.setWindowTitle(title)
        self.setWindowToCenter()
        self.setWindowIcon(QIcon("./Figure/icon.png"))

    def setWindowToCenter(self):
        positioning = self.frameGeometry()
        centralPosition= QtWidgets.QDesktopWidget().availableGeometry().center()
        positioning.moveCenter(centralPosition)
        self.move(positioning.topLeft())

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Exit Program', "Are you sure to quit chess?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()




if __name__=="__main__":
    app = QApplication(sys.argv)
    firstScene = MainWindow(700, 600, "Chess")
    sys.exit(app.exec_())
