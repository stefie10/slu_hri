from PyQt4.QtCore import *
from PyQt4.QtGui import *


from qt_utils import Counter

class Model(QAbstractTableModel):

    counter = Counter()
    COL_NAME = counter.pp()
    COL_VALUE = counter.pp()

    def __init__(self, view):
        QAbstractTableModel.__init__(self)

        self._data = []
        self.view = view
        self.view.setModel(self)
        self.view.setColumnWidth(self.COL_NAME, 300)
    def setClassifier(self, classifier):
        self.classifier = classifier
        self._data = self.classifier.engine.features
        self.reset()
        
    def columnCount(self, parent=None):
        return self.counter.cnt
    def rowCount(self, parent=None):
        return len(self._data)
    
    def get(self, viewIdx):
        return self._data[viewIdx]

    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        e = self.get(idx.row())
        if self.classifier.has_data:
            value = self.classifier.features[e]
        else:
            value = None

        if role != Qt.DisplayRole:
            return QVariant()            

        if col == self.COL_NAME:
            return QVariant(e)
        if col == self.COL_VALUE:
            return QVariant(value)
        else:
            raise ValueError("Bad column: " + `col`)
        
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == self.COL_NAME:
                return QVariant("Name")
            elif col == self.COL_VALUE:
                return QVariant("Value")
            else:
                raise ValueError("Bad id: " + `col`)
        else:
            return QVariant()

    def selectedData(self):
        return self.get(self.view.currentIndex().row())
        
    
