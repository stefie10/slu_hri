from PyQt4.QtCore import *
from PyQt4.QtGui import *
from environ_vars import TKLIB_HOME

from chunkerAnnotator.exporter import toprettyxml_fixed
from chunkerAnnotator import sdcAnnotator
import dialogAnnotator_ui
import basewindow
import dialogModel
import turnModel
import reader
from reader import readDialogs


class MainWindow(dialogAnnotator_ui.Ui_MainWindow, QMainWindow):
    def __init__(self, fname):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.dialogs = []

        self.sdcAnnotator = sdcAnnotator.MainWindow()
        self.sdcAnnotator.show()

        
        self.dialogModel = dialogModel.Model(self.dialogTable)

        self.turnModel = turnModel.Model(self.turnTable)



        self.connect(self.dialogTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectDialog)


        self.connect(self.turnTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectTurn)

        self.connect(self.actionSave,
                     SIGNAL("triggered()"),
                     self.save)

        self.connect(self.actionOpen,
                     SIGNAL("triggered()"),
                     self.openFile)

        self.connect(self.actionLoadFromOds,
                     SIGNAL("triggered()"),
                     self.loadFromOds)        
        
        
        self.turn = None


    def selectDialog(self):
        dialog = self.dialogModel.selectedData()
        self.turnModel.load(dialog.turns)
        self.turnTable.selectRow(0)


        
    def selectTurn(self):
        if self.turn != None:
            self.turn.setSdcs(self.sdcAnnotator.annotations)
            
        self.turn = self.turnModel.selectedData()
        self.sdcAnnotator.setData(self.turn.utterance, self.turn.sdcs)

    def loadFromOds(self):
        dialogs = reader.read("%s/data/matthias/transcriptions.ods" % TKLIB_HOME)
        self.load(dialogs)

        
    def load(self, dialogs):
        self.dialogs = dialogs
        self.dialogModel.load(self.dialogs)
        self.dialogTable.selectRow(0)

    def openFile(self, fname=None):
        if fname == None:
            raise ValueError("implement dialog")
        self.load(readDialogs(fname))
        
    def save(self):
        if self.turn != None:
            self.turn.setSdcs(self.sdcAnnotator.annotations)
        
        from xml.dom.minidom import Document
        
        doc = Document()
        dialogsXml = doc.createElement("dialogs")

        for d in self.dialogs:
            dialogXml = doc.createElement("dialog")
            dialogXml.setAttribute("id", str(d.id))

            for t in d.turns:
                turnXml = doc.createElement("turn")
                utteranceXml = doc.createElement("utterance")
                utteranceXml.appendChild(doc.createTextNode(t.utterance))
                turnXml.appendChild(utteranceXml)

                speakerXml = doc.createElement("speaker")
                speakerXml.appendChild(doc.createTextNode(t.speaker))
                turnXml.appendChild(speakerXml)

                startXml = doc.createElement("start")
                startXml.appendChild(doc.createTextNode(str(t.start)))
                turnXml.appendChild(startXml)

                endXml = doc.createElement("end")
                endXml.appendChild(doc.createTextNode(str(t.end)))
                turnXml.appendChild(endXml)

                durationXml = doc.createElement("duration")
                durationXml.appendChild(doc.createTextNode(str(t.duration)))
                turnXml.appendChild(durationXml)                 

                sdcsXml = doc.createElement("sdcs")
                for sdc in t.sdcs:
                    sdcsXml.appendChild(sdc.toXml(doc))
                turnXml.appendChild(sdcsXml)

                dialogXml.appendChild(turnXml)
            
            dialogsXml.appendChild(dialogXml)

        doc.appendChild(dialogsXml)
        outfile = open("out.xml", "w")
        outfile.write(toprettyxml_fixed(doc))
        outfile.close()

def main():
    app = basewindow.makeApp()
    fname = "data/matthias/transcriptions.xls"
    wnd = MainWindow(fname)

    wnd.openFile("out.xml")
    wnd.show()
    retval = app.exec_()

if __name__ == "__main__":
    main()
