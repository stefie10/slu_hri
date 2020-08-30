import matplotlib
matplotlib.use("Qt4Agg")

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from chunkerAnnotator import sdcAnnotator
from voom import verbs
from voom.gui import recorder
from voom.gui.assignments.assignmentData import Assignment 
import assignmentModel
import assignment_ui
import tag_util



class MainWindow(QMainWindow, assignment_ui.Ui_MainWindow):
    def __init__(self, tagFile, skeleton, isEditable):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.tagFile = tagFile
        self.skeleton = skeleton    
        self.entry = None
        
        self.recorder = recorder.MainWindow(tagFile, skeleton)
        self.recorder.show()
        
        self.assignmentModel = assignmentModel.Model(verbs.verbMap,
                                                     self.assignmentTable, 
                                                     isEditable=isEditable)
        
        self.sdcAnnotator = sdcAnnotator.MainWindow()
        self.sdcAnnotator.show()
        

        self.fname = ""
        self.connect(self.actionOpen,
                     SIGNAL("triggered()"),
                     self.open)
        
        
        
        self.connect(self.actionSave,
                     SIGNAL("triggered()"),
                     self.save)

        self.connect(self.assignmentTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectAssignment)

        self.assignmentTable.selectRow(0)
        
        self.sdcTag = "stefie10"

    def open(self, fname):
        self.fname = fname
        assignment = Assignment.load(fname, self.tagFile, self.skeleton)
        self.load(assignment)
    
    def load(self, assignment):
        self.assignment = assignment
        self.assignmentModel.loadData(self.assignment)
        #self.assignmentTable.selectRow(28)
        self.assignmentTable.selectRow(0)
        
    def save(self):
        self.copySdcs()
        print "fname", self.fname
        fname = QFileDialog.getSaveFileName(self, "Save File", self.fname)
        print "after", fname, fname.__class__
        if fname != "":
            self.fname = fname
            self.assignment.save(self.fname)
        
        
    def copySdcs(self):
        if self.entry != None:
            self.entry.setSdcs(self.sdcTag, self.sdcAnnotator.annotations)
    def selectAssignment(self):
        
        self.copySdcs()
        
        self.entry = self.assignmentModel.selectedData()
        self.recorder.recordAssignment(self.entry)
        self.sdcAnnotator.setData(self.entry.command, self.entry.sdcs(self.sdcTag))
        

def main():
    
    
    from sys import argv
    import cPickle
    import basewindow
    app = basewindow.makeApp()
    
    map_fn = argv[1]
    gtruth_tag_fn = argv[2]
    cluster_fn = argv[3]
    assignment_fn = argv[4]
    tagFile = tag_util.tag_file(gtruth_tag_fn, map_fn)
    tagFile.get_map()
    tagFile.get_tag_names()

    skeleton = cPickle.load(open(cluster_fn, 'r'))

    wnd = MainWindow(tagFile, skeleton, isEditable=True)
    wnd.show()
    wnd.open(assignment_fn)
    
    #vae = VerbAssignmentEntry.load("vae1.yaml", tagFile, skeleton)
    
    
    #wnd.recorder.recordAssignment(vae)

    retval = app.exec_()
if __name__ == "__main__":
    main()
