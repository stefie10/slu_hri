from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sdcAnnotator
from routeDirectionCorpusReader import readSession
import basewindow
import chunkerAnnotator_ui
import instructionTableModel
import sys



class MainWindow(chunkerAnnotator_ui.Ui_MainWindow, QMainWindow):
    def __init__(self, fname):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.sdcAnnotator = sdcAnnotator.MainWindow()
        self.sdcAnnotator.show()

        self.connect(self.actionSave, SIGNAL("triggered()"), self.save)

        self.activeData = None
        #self.sessions = readSession(fname, "dlaude")
        self.sessions = readSession(fname, "stefie10-d1-hierarchical")
        #self.sessions = readSession(fname, "tkollar")
        #self.sessions = readSession(fname, "regexp_chunker")
        #self.sessions = readSession(fname, "crf_chunker")
        self.setWindowTitle(self.sessions.annotationSource)
        self.instructionModel = instructionTableModel.Model(self.instructionTable,
                                                            self.sessions)
        self.instructionTable.verticalHeader().hide()
        self.instructionTable.horizontalHeader().hide()
        self.instructionTable.horizontalHeader().setStretchLastSection(True)

        self.connect(self.instructionTable.selectionModel(), 
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectInstruction)

        self.instructionTable.selectRow(0)


    def save(self):
        print "saving"
        for session in self.sessions:
            session.saveAnnotations()


    def startSelection(self):
        self.selectionStart = self.instructionEdit.textCursor().position()

    def endSelection(self):
        if not (self.selectionStart is None):
            selectionEnd = self.instructionEdit.textCursor().position()
            
            # moving the cursor doesn't work for some reason. 
            # it selects the text but then hides the cursor. 
            
            #cursor = self.instructionEdit.textCursor()
            #cursor.setPosition(self.selectionStart)
            #cursor.setPosition(selectionEnd, QTextCursor.KeepAnchor)
            #cursor.setPosition(selectionEnd)
            #self.instructionEdit.setTextCursor(cursor)

            for i in range(0, selectionEnd - self.selectionStart):
                self.instructionEdit.moveCursor(QTextCursor.Left)
            for i in range(0, selectionEnd - self.selectionStart):
                self.instructionEdit.moveCursor(QTextCursor.Right, 
                                                QTextCursor.KeepAnchor)


        
    def makeMoveAction(self, shortcut, moveType):
        def moveMethod():
            self.instructionEdit.moveCursor(moveType)
        self.makeAction(shortcut, moveMethod)
    def makeAction(self, shortcut, method):
        action = QAction(self)
        self.addAction(action)
        action.setShortcut(shortcut)
        self.connect(action, SIGNAL("triggered()"), method)
        return action
        
        


    def selectInstruction(self):
        if self.activeData != None:
            activeSession, activeInstructionIdx = self.activeData
            
            activeSession.routeAnnotations[activeInstructionIdx] = self.sdcAnnotator.annotations
        
        
        session, instructionIdx, instruction = \
            self.instructionModel.selectedData()
        annotations = session.routeAnnotations[instructionIdx]
        self.sdcAnnotator.setData(instruction, annotations)
        self.activeData = session, instructionIdx

if __name__ == "__main__":
    app = basewindow.makeApp()
    fname = "data/Direction understanding subjects Floor 1 (Final).ods"
    #fname = "data/Direction understanding subjects Floor 8 (Final).ods"
    wnd = MainWindow(fname)
    wnd.show()
    retval = app.exec_()
    sys.exit(retval)      


