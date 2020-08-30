from PyQt4.QtCore import *
from PyQt4.QtGui import *
from routeDirectionCorpusReader import Standoff, Annotation, \
    makeNullTextStandoff, TextStandoff
import annotationTableModel
import basewindow
import sdcAnnotator_ui
import sys



class MainWindow(sdcAnnotator_ui.Ui_MainWindow, QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.setWindowTitle("SDC Annotator")
        

        self.annotationModel = annotationTableModel.Model(self.annotationTable)
        self.annotationTable.horizontalHeader().hide()
        self.annotationTable.verticalHeader().hide()
        self.annotationTable.horizontalHeader().setStretchLastSection(True)

        

        self.connect(self.annotationTable.selectionModel(), 
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectAnnotation)
        

        actions = []
        actions.append(self.makeMoveAction("Ctrl+B", QTextCursor.Left))
        actions.append(self.makeMoveAction("Ctrl+F", QTextCursor.Right))
        actions.append(self.makeMoveAction("Ctrl+P", QTextCursor.Up))
        actions.append(self.makeMoveAction("Ctrl+N", QTextCursor.Down))
        actions.append(self.makeMoveAction("Ctrl+E", QTextCursor.EndOfLine))
        actions.append(self.makeMoveAction("Ctrl+A", QTextCursor.StartOfLine))

        #actions.append(self.makeMoveAction("Alt+W", QTextCursor.StartOfLine))

        
        self.makeAction("Ctrl+ ", self.startSelection)
        self.makeAction("Alt+W", self.endSelection)

        self.makeAction("N", self.newAnnotation)
        self.makeAction("C", self.clear)
        self.makeAction("U", self.updateAnnotation)
        self.makeAction("D", self.deleteAnnotation)


        self.annotationMap = {}
        self.buttonMap = {"verb":self.verbButton, 
                          "spatialRelation":self.spatialRelationButton, 
                          "landmark":self.landmarkButton,
                          "landmark2":self.landmark2Button,
                          "figure":self.figureButton,
                          }
        self.labelMap = {"verb":self.verbLabel,
                         "spatialRelation":self.spatialRelationLabel,
                         "landmark":self.landmarkLabel,
                         "landmark2":self.landmark2Label,
                         "figure":self.figureLabel,
                         }


        for key in Annotation.keys:
            self.annotationMap[key] = None
            def makeUpdateFunction(gui, key):
                def updateFunction():
                    range = self.getTextSelection()
                    standoff = TextStandoff(self.text, range)
                    gui.annotationMap[key] = standoff
                    gui.labelMap[key].setText(standoff.text)
                return updateFunction
            self.connect(self.buttonMap[key], SIGNAL("clicked()"), 
                         makeUpdateFunction(self, key))
            
        range = self.getTextSelection()
        #self.verb = Standoff(session, instructionIdx, range)
        #self.verbLabel.setText(self.verb.text)
        #self.connect(self.verbButton, SIGNAL("clicked()"), self.updateVerb)
        #self.connect(self.spatialRelationButton, SIGNAL("clicked()"), 
        #             self.updateSpatialRelation)
        #self.connect(self.landmarkButton, SIGNAL("clicked()"), 
        #             self.updateLandmark)


        self.selectionStart = None

        



    def getTextSelection(self):
        cursor = self.instructionEdit.textCursor()
        return cursor.selectionStart(), cursor.selectionEnd()

    def updateSpatialRelation(self):
        session, instructionIdx, instruction = self.instructionModel.selectedData()
        range = self.getTextSelection()
        self.spatialRelation = Standoff(session, instructionIdx, range)
        self.spatialRelationLabel.setText(self.spatialRelation.text)

        
    def newAnnotation(self):
        self.annotationModel.addAnnotation(Annotation(**self.annotationMap))
        self.clear()

    def deleteAnnotation(self):
        annotationIdx = self.annotationModel.view.currentIndex().row()
        self.annotationModel.deleteAnnotation(annotationIdx)
        self.annotationModel.reset()


        
    def updateAnnotation(self):
        print "Updating annotation"
        annotation = self.annotationModel.selectedData()
        for key in Annotation.keys:
            annotation.annotationMap[key] = self.annotationMap[key]
        self.annotationModel.reset()



    def clear(self):
        for key, value in self.labelMap.iteritems():
            value.setText("")
            self.annotationMap[key] = makeNullTextStandoff(self.text)
        
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
        
        





    def setData(self, text, annotations):
        self.text = text
        self.instructionEdit.document().setPlainText(text)
        self.annotationModel.setAnnotations(annotations)            
        self.clear()


    def selectAnnotation(self):
        cursor = QTextCursor(self.instructionEdit.document())
        format = QTextCharFormat()
        cursor.setPosition(0)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        format.setBackground(QBrush(Qt.white))
        cursor.setCharFormat(format)

        print "selecting annotation"
        annotation = self.annotationModel.selectedData()
        start, end = annotation.spatialRelation.range
        cursor = self.instructionEdit.textCursor()
        here = cursor.position()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        colors = [Qt.magenta, Qt.green, Qt.cyan, Qt.yellow, QColor(100, 255, 100)]
        assert len(colors) >= len(Annotation.keys)
        
        for key, color in zip(Annotation.keys, colors):
            self.annotationMap[key] = annotation[key]
            field = self.annotationMap[key]
            self.labelMap[key].setText(field.text)

            cursor = QTextCursor(self.instructionEdit.document())
            cursor.setPosition(field.range[0])
            cursor.setPosition(field.range[-1], QTextCursor.KeepAnchor)
            format = QTextCharFormat()
            format.setBackground(QBrush(color))
            cursor.setCharFormat(format)
            
        #cursor.setPosition(here)
        #self.instructionEdit.setTextCursor(cursor)

    @property
    def annotations(self):
        return self.annotationModel._data      

        
        

if __name__ == "__main__":
    app = basewindow.makeApp()
    #fname = "data/Direction understanding subjects Floor 1 (Final).ods"
    fname = "data/Direction understanding subjects Floor 8 (Final).ods"
    wnd = MainWindow(fname)
    wnd.show()
    retval = app.exec_()
    sys.exit(retval)      


