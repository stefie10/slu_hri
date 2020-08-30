from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter

counter = Counter()
COL_NAME = counter.pp()
COL_VALUE = counter.pp()

class Entry:
    def __init__(self, example, name):
        self.example = example
        self.name = name
        
    @property
    def value(self):
        return self.example[self.name]
    
    @property
    def drawCommands(self):
        drawMap = self.example["drawMap"].value
        if self.name in drawMap:
            return self.example["drawMap"].value[self.name]
        else:
            return []
    
        
class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self._data = []
        self.view = view
        self.view.setModel(self)

        
    def loadData(self, example):
        self._data = []
        
        for feature in example.domain:
            print feature.name
            self._data.append(Entry(example, feature.name))
            
        self._data.sort(key=lambda e: e.name)
        self.reset()
        

    def columnCount(self, parent):
        return counter.cnt

    def rowCount(self, parent):
        return len(self._data)

    def get(self, i):
        return self._data[i]
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        e = self.get(idx.row())
        
        if role != Qt.DisplayRole:
            return QVariant()         
        
        if col == COL_NAME:
            return QVariant("%s" % e.name)
        elif col == COL_VALUE:
            return QVariant("%s" % e.value)        
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_NAME:
                return QVariant("Name")
            elif section == COL_VALUE:
                return QVariant("p_true")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()
                         
    def selectedData(self):
        if self.view.currentIndex().row() == -1:
            return None
        else:
            return self.get(self.view.currentIndex().row())


