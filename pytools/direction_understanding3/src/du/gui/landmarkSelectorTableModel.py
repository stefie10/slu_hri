from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter
counter = Counter()

COL_INDEX = counter.pp()
COL_NAME = counter.pp()
COL_LOCATION = counter.pp()

class Entry:
    def __init__(self, m4du, i):
        self.i = i
        self.name = m4du.obj_names[i]
        self.location = m4du.obj_locations[0][i], m4du.obj_locations[1][i]


class Model(QAbstractTableModel):
    def __init__(self, view, m4du):
        QAbstractTableModel.__init__(self)

        self.m4du = m4du

        self._data = [Entry(m4du, i) for i in range(len(self.m4du.obj_names))]

        self.view = view
        self.view.setModel(self)
        self.view.selectAll()
    def selectedIndexes(self):
        return set([self.get(idx.row()).i for idx in self.view.selectedIndexes()])

    def selectIndexes(self, indexes):
        model_to_view = {}
        for i, e in enumerate(self._data):
            model_to_view[e.i] = i
        self.view.clearSelection()
        for idx in indexes:
            viewIdx = model_to_view[idx]
            self.view.selectRow(viewIdx)
            
                          

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
        if col == COL_NAME:
            return QVariant(e.name)
        elif col == COL_LOCATION:
            return QVariant("%.2f, %.2f" % tuple(e.location))
        elif col == COL_INDEX:
            return QVariant("%d" % e.i)
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_NAME:
                return QVariant("Name")
            elif section == COL_LOCATION:
                return QVariant("Location")
            elif section == COL_INDEX:
                return QVariant("i")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()

    def sort(self, col, order):


        if col == COL_NAME:
            self._data.sort(key=lambda e: e.name)
        elif col == COL_LOCATION:
            self._data.sort(key=lambda e: `e.location`)
        elif col == COL_INDEX:
            self._data.sort(key=lambda e: e.i)


        if order == Qt.DescendingOrder:
            self._data.reverse()
            
        self.reset()
            
        
