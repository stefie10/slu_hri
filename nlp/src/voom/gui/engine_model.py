from PyQt4.QtCore import *
from PyQt4.QtGui import *


from qt_utils import Counter

class Model(QAbstractTableModel):

    counter = Counter()
    COL_NAME = counter.pp()

    def __init__(self, view, classifiers):
        QAbstractTableModel.__init__(self)

        self._data = list(classifiers)
        self._data.sort(key=lambda x: x.engine.name)
        
        self.view = view
        self.view.setModel(self)


    def columnCount(self, parent=None):
        return self.counter.cnt
    def rowCount(self, parent=None):
        return len(self._data)
    
    def idxForName(self, name):
        for i, c in enumerate(self._data):
            if c.engine.name == name:
                return i
        raise ValueError("No entry for " + `name` + " in " + `self._data`)
    def get(self, viewIdx):
        return self._data[viewIdx]

    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        e = self.get(idx.row())

        if role != Qt.DisplayRole:
            return QVariant()            

        if col == self.COL_NAME:
            return QVariant(e.engine.name)
        else:
            raise ValueError("Bad column: " + `col`)
        
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == self.COL_NAME:
                return QVariant("Name")
            else:
                raise ValueError("Bad id: " + `col`)
        else:
            return QVariant()

    def selectedData(self):
        return self.get(self.view.currentIndex().row())
        
