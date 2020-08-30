from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qt_utils import Counter

counter = Counter()

COL_SLOC = counter.pp()
COL_ACTUAL_ELOC = counter.pp()
COL_CORRECT_ELOCS = counter.pp()
COL_CORRECT = counter.pp()
COL_PATH = counter.pp()
COL_PROBABILITY = counter.pp()
COL_DIRECTIONS = counter.pp()


class Entry:
    def __init__(self, run_idx, outputEntry):

        self.run_idx = run_idx
        assert run_idx >= 0
        assert run_idx < 4
        self.sentence = outputEntry.sentence
        self.correct = outputEntry.correct[run_idx]
        self.iCorrectSloc = outputEntry.iCorrectSlocs[run_idx]

        self.iActualEloc = outputEntry.iActualElocs[run_idx]
        self.iCorrectElocs = outputEntry.iCorrectElocs
        self.probability = outputEntry.probabilities[run_idx]
        self.path = outputEntry.paths[run_idx]

        self.directions = outputEntry.sentence
        
class Model(QAbstractTableModel):
    def __init__(self, view, m4du):
        QAbstractTableModel.__init__(self)
        self.m4du = m4du
        self._data = []

        self.view = view
        self.view.setModel(self)
        self.view.setColumnWidth(COL_CORRECT_ELOCS, 160)

        self.view.setColumnWidth(COL_DIRECTIONS, 500)
        self.view.setWordWrap(True)
        QTimer.singleShot(0, self.view.resizeRowsToContents)


    def setEntries(self, lst):
        data = []
        for e in lst:
            for i, correct in enumerate(e.correct):
                data.append(Entry(i, e))
        self._data = data
        self.reset()
                
    def setData(self, e):
        self.setEntries([e])


    def columnCount(self, parent=None):
        return counter.cnt
    def rowCount(self, parent=None):
        return len(self._data)

    def get(self, viewIdx):
        return self._data[viewIdx]

    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()

        e = self.get(idx.row())

        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_SLOC:
            return QVariant(e.iCorrectSloc)
        elif col == COL_CORRECT_ELOCS:
            return QVariant(`e.iCorrectElocs`)
        elif col == COL_ACTUAL_ELOC:
            return QVariant(e.iActualEloc)
        elif col == COL_CORRECT:
            return QVariant(e.correct)
        elif col == COL_DIRECTIONS:
            return QVariant(e.directions)
        elif col == COL_PROBABILITY:
            if e.probability != None:
                return QVariant("%e" % e.probability)
            else:
                return QVariant("None")
        elif col == COL_PATH:
            if e.path != None:
                return QVariant(`[self.m4du.vpt_to_num[vp] for vp in e.path]`)
            else:
                return QVariant("None")
        else:
            raise ValueError("Unxpected index", idx)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == COL_SLOC:
                return QVariant("sloc")
            elif col == COL_CORRECT_ELOCS:
                return QVariant("correct eloc")
            elif col == COL_ACTUAL_ELOC:
                return QVariant("actual eloc")
            elif col == COL_CORRECT:
                return QVariant("correct")
            elif col == COL_PATH:
                return QVariant("path")
            elif col == COL_PROBABILITY:
                return QVariant("probability")
            elif col == COL_DIRECTIONS:
                return QVariant("directions")
            else:
                raise ValueError("Unxpected index", col)
        else:
            return QVariant()

    def selectedData(self):
        return self.get(self.view.currentIndex().row())
