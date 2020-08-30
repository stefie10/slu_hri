from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as na
from qt_utils import Counter
import math2d
counter = Counter()

COL_SENTENCE_IDX = counter.pp()
COL_SUBJECT = counter.pp()
COL_SENTENCE = counter.pp()
COL_CORRECT = counter.pp()
COL_STRICT_CORRECT = counter.pp()
COL_SLOCS = counter.pp()
COL_CORRECT_ELOCS = counter.pp()
COL_ACTUAL_ELOCS = counter.pp()


class Entry:
    def __init__(self, i, run_output,m4du):
        self.i = i
        self.correct = run_output["correct"][i]
        self.sentence = run_output["sentences"][i]
        self.subject = str(run_output["subjects"][i])
        
        self.startLabel, self.endLabel = [x.strip() for x in run_output['regions'][i].split('to')]

        topohash = run_output["region_to_topology"]
        self.iSlocTopo = topohash[self.startLabel][0]
        self.iCorrectElocTopo = topohash[self.endLabel][0]
        
        self.iCorrectSlocs = m4du.vpts_for_topo(self.iSlocTopo)
        self.iCorrectElocs = m4du.vpts_for_topo(self.iCorrectElocTopo)

        elocs = [path[-1] if path != None else None for path in run_output["path"][i]]
        self.iActualElocs = [m4du.vpt_to_num[vp] if vp != None else None for vp in elocs]

        slocs = [path[0] if path != None else None for path in run_output["path"][i]]
        self.iActualSlocs = [m4du.vpt_to_num[vp] if vp != None else None for vp in slocs]

        self.paths = run_output["path"][i]
        print "path", self.paths

        self.probabilities = run_output["probability"][i]

    @property
    def any_correct(self):
        return any(self.correct)

    @property
    def strict_correct(self):
        return self.correct[na.argmax(self.probabilities)]

def loadData(run_output, m4du):
    data = []
    for i, correct in enumerate(run_output['correct']):
        if(run_output["sentences"][i] == None):
            continue
        
        e = Entry (i, run_output, m4du)
        data.append(e)
        if e.any_correct:
            print e.startLabel, e.sentence

    lengths = []
    subject_to_lengths = {}
    for e in data:

        for path in e.paths:
            if path == None:
                continue
            path_xy = []
            for point in path:
                print "point", point
                topo_st,  ang = point.split("_")
                x, y = m4du.tmap_locs[float(topo_st)]
                path_xy.append((x, y))
            path_length = math2d.length(path_xy)
            lengths.append(path_length)
            subject_to_lengths.setdefault(e.subject, [])
            subject_to_lengths[e.subject].append(path_length)

    print "average length", na.mean(lengths)
    for subject in sorted(subject_to_lengths.keys()):
        print subject, na.mean(subject_to_lengths[subject])
    return data


class Model(QAbstractTableModel):
    def __init__(self, view, m4du, run_output):
        QAbstractTableModel.__init__(self)
        self.m4du = m4du
        self._data = loadData(run_output, self.m4du)
        self.view = view
        self.view.setModel(self)
        self.view.setColumnWidth(COL_SENTENCE,300)
        self.view.setColumnWidth(COL_SENTENCE_IDX, 35)
        self.view.setColumnWidth(COL_CORRECT, 60)
        self.view.setColumnWidth(COL_STRICT_CORRECT, 60)
        self.view.setColumnWidth(COL_CORRECT_ELOCS, 160)
        self.view.setColumnWidth(COL_ACTUAL_ELOCS, 160)
        self.view.setColumnWidth(COL_SLOCS, 160)
    def columnCount(self, parent=None):
        return counter.cnt
    def rowCount(self, parent=None):
        return len(self._data)

    def selectedData(self):
        return self.get(self.view.currentIndex().row())


    def get(self, viewIdx):
        return self._data[viewIdx]

    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()

        e = self.get(idx.row())

        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_SENTENCE:
            return QVariant(e.sentence)
        elif col == COL_SENTENCE_IDX:
            return QVariant(e.i)
        elif col == COL_CORRECT:
            return QVariant(e.any_correct)
        elif col == COL_STRICT_CORRECT:
            return QVariant(e.strict_correct)
        elif col == COL_SLOCS:
            return QVariant(`e.iCorrectSlocs`)
        elif col == COL_CORRECT_ELOCS:
            return QVariant(`e.iCorrectElocs`)
        elif col == COL_ACTUAL_ELOCS:
            return QVariant(`e.iActualElocs`)
        elif col == COL_SUBJECT:
            return QVariant(`e.subject`)        
        else:
            raise ValueError("Unxpected index", idx)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == COL_SENTENCE:
                return QVariant("sentence")
            elif col == COL_SENTENCE_IDX:
                return QVariant("idx")
            elif col == COL_CORRECT:
                return QVariant("correct")
            elif col == COL_STRICT_CORRECT:
                return QVariant("strict correct")
            elif col == COL_SLOCS:
                return QVariant("slocs")
            elif col == COL_CORRECT_ELOCS:
                return QVariant("correct elocs")
            elif col == COL_ACTUAL_ELOCS:
                return QVariant("actual elocs")
            elif col == COL_SUBJECT:
                return QVariant("subject")            
            else:
                raise ValueError("Unxpected index", col)
        else:
            return QVariant()

    def sort(self, col, order):
        if col == COL_SENTENCE_IDX:
            self._data.sort(key=lambda e: e.i)
        elif col == COL_SENTENCE:
            self._data.sort(key=lambda e: `e.sentence`)
        elif col == COL_SUBJECT:
            self._data.sort(key=lambda e: `e.subject`)  
        elif col == COL_CORRECT:
            self._data.sort(key=lambda e: e.any_correct)
        elif col == COL_CORRECT_ELOCS:
            self._data.sort(key=lambda e: `e.iCorrectElocs`)
        elif col == COL_SLOCS:
            self._data.sort(key=lambda e: `e.iCorrectSlocs`)
            
        elif col == COL_ACTUAL_ELOCS:
            self._data.sort(key=lambda e: `e.iActualSlocs`)
        else:
            self._data.sort(key=lambda e: e.i)

        if order == Qt.DescendingOrder:
            self._data.reverse()
            
        self.reset()
