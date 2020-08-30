from PyQt4.QtGui import *
from PyQt4.QtCore import *
import explorationBrowser_ui
import sys
import time
import cPickle
import basewindow
from tag_util import tag_file
from du.eval_util import model_evaluator
from logfile_util import logfile_du

from qt_utils import Counter
counter = Counter()

COL_INDEX = counter.pp()
COL_SDC = counter.pp()


class Model(QAbstractTableModel):
    def __init__(self, view, me):
        QAbstractTableModel.__init__(self)
        self.sdcs = []

        self.view = view
        self.view.setModel(self)
        self.me = me
        self.skel_map = self.me.get_skeleton_map()

    def columnCount(self, parent=None):
        return counter.cnt
    def rowCount(self, parent=None):
        return len(self.sdcs)
    
    def set_data(self, res):
        self.path, self.probs, self.sdcs_eval, self.sdcs, self.frontiers, self.frontiers_all, self.front_allowed = res
        self.reset()

    def selectedIndex(self):
        return self.get(self.view.currentIndex().row())

    def get(self, i):
        X, Y = self.skel_map.compute_path(path[0:2,i], path[0:2,i+1])
        ther, theim_str, odom = lf.get_readings([X[i], Y[i], curr_orient+sf*rotation])
        myim = lf.get_image(theim_str)
        return [X, Y], myim
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        i = idx.row()
        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_INDEX:
            return QVariant(idx.row())
        elif col == COL_SDC:
            return QVariant("%s %s %s" % (self.sdcs_eval[i]['verb'], self.sdcs_eval[i]['sr'], self.sdcs_eval[i]['landmark']))
        else:
            raise ValueError()

class MainWindow(QMainWindow, explorationBrowser_ui.Ui_MainWindow):
    def __init__(self, modelEvaluator, sentence, start_region, lf):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.lf = lf
        self.resultModel = Model(self.resultTable)
        
        self.modelEvaluator = modelEvaluator
        res = self.modelEvaluator.evaluate_sentence_explore(sentence, start_region=start_region)

        self.resultModel.set_data(res)
        
        

        self.connect(self.resultTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectSdc)

    def selectSdc(self):
        idx = self.resultModel.selectedIndex()
        i = idx.row()
        paths, image_fname = self.resultModel.get(idx.row)
        print image_fname


def main():
    argv = sys.argv
    start = time.time()
    laser_fname = argv[1]
    image_dir = argv[2]
    model_fname = argv[3]
    region_fname = argv[4]
    map_fname = argv[5]


    lf = logfile_du(laser_fname, image_dir)
    
    m4du = cPickle.load(open(model_fname, 'r'))
    end = time.time()

    m4du.initialize()
    print "tags"
    gtruth_tf = tag_file(region_fname, map_fname)
    me = model_evaluator(m4du, gtruth_tf, "d8")

    app = basewindow.makeApp()
    sentence = '''Go through the double doors and past the
        lobby.  Go into a lounge with some couches. Enjoy the nice
        view.  Go past the spiral staircase.  Continue towards the
        hallway with the cubby holes.  But don't go down that
        hallway. Instead take a right into the kitchen.'''

    sentence = "Go through the double doors and past the lobby."
    wnd = MainWindow(me, sentence, "R9", lf)
    wnd.setWindowTitle(model_fname)
    wnd.show()    

    retval = app.exec_()        
if __name__=="__main__":
    main()


