from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter

counter = Counter()
COL_NAME = counter.pp()
COL_SCORE = counter.pp()


class Entry:
    def __init__(self, engine, geometry):
        self.engine = engine
        self.geometry = geometry
        self.cls, self.probabilities, self.ex = engine.classify(**geometry)
        

    @property
    def p_true(self):
        return self.probabilities["True"]

                   


class Model(QAbstractTableModel):
    def __init__(self, view, engineMap):
        QAbstractTableModel.__init__(self)
        self.engineNames = sorted(engineMap.keys())
        self.engineMap = engineMap
        self._data = []

        self.view = view
        self.view.setModel(self)

        
    def columnCount(self, parent=None):
        return counter.cnt        

    def rowCount(self, parent=None):
        return len(self._data)

    def setGeometry(self, geometry):
        self._data = [Entry(self.engineMap[name], geometry) for name in 
                      self.engineNames]
        self._data.sort(key=lambda e: e.p_true, reverse=True)
        self.reset()
    def get(self, idx):
        return self._data[idx]

    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        e = self.get(idx.row())
        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_NAME:
            return QVariant(e.engine.name())
        elif col == COL_SCORE:
            return QVariant("%.3f" % e.p_true)
        else:
            raise ValueError("Bad id: %s" % col)

    def sort(self, col, order):
        if col == COL_SCORE:
            self._data.sort(key=lambda e: e.p_true)
        elif col == COL_NAME:
            self._data.sort(key=lambda e: e.engine.name())


        if order == Qt.DescendingOrder:
            self._data.reverse()
        self.reset()
            
