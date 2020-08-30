from PyQt4.QtCore import *
from PyQt4.QtGui import *
import cPickle
import du.gui.modelBrowser
import resultsBrowser_ui
import resultsTableModel
import sentenceResultsTableModel
import pathOverlay
import basewindow
import os


class MainWindow(QMainWindow, resultsBrowser_ui.Ui_MainWindow):
    def __init__(self, m4du, run_output):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.m4du = m4du
        self.run_output = run_output

        self.resultsModel = resultsTableModel.Model(self.resultsTable, self.m4du, self.run_output)
        self.sentenceResultsModel = sentenceResultsTableModel.Model(self.sentenceResultsTable, self.m4du)

        self.connect(self.resultsTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectResult)
        self.connect(self.sentenceResultsTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectSentenceResult)

        self.browser = du.gui.modelBrowser.MainWindow(self.m4du, run_output['corpus_fname'])
        self.browser.show()

        self.pathOverlay = pathOverlay.MainWindow(self.m4du)
        self.pathOverlay.show()

        self.resultsTable.selectRow(0)

    def selectResult(self):
        e = self.resultsModel.selectedData()
        self.sentenceResultsModel.setData(e)
        self.sentenceResultsTable.selectRow(0)

        results = set()
        for idx in self.resultsTable.selectedIndexes():
            print "idices", idx.row()
            e = self.resultsModel.get(idx.row())
            results.add(e)
        self.pathOverlay.plotPaths(list(results))
            

    def selectSentenceResult(self):
        self.browser.loadResult(self.sentenceResultsModel.selectedData())


def main(argv):
    print "loading model"
    model_file = argv[1]
    output_file = argv[2]
    m4du = cPickle.load(open(model_file, 'r'))

    print "initializing"
    m4du.initialize()
    print "tags"
    #tf = tag_file(argv[2], argv[3])

    ofile = cPickle.load(open(output_file, 'r'))

    app = basewindow.makeApp()
    wnd = MainWindow(m4du, ofile)
    wnd.setWindowTitle("Model %s, output %s" % (os.path.basename(model_file), os.path.basename(output_file)))

    wnd.browser.setWindowTitle(model_file)
            
    wnd.show()
    retval = app.exec_()


if __name__=="__main__":
    import sys
    main(sys.argv)

