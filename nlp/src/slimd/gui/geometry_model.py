from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter

counter = Counter()
COL_NAME = counter.pp()
COL_GEOMETRY = counter.pp() 


class Entry:
    def __init__(self, name, geometry):
        self.name = name
        self.geometry = geometry
class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self._data = []
        self.view = view
        self.view.setModel(self)

        
    def loadData(self, data):
        self._data = []
        for name, geometry in data.iteritems():
            self._data.append(Entry(name, geometry))
            
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
        elif col == COL_GEOMETRY: 
            return QVariant("%s" % `e.geometry`)
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_NAME:
                return QVariant("Name")
            elif section == COL_GEOMETRY:
                return QVariant("Geometry")            
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()
                         
    def selectedData(self):
        return self.get(self.view.currentIndex().row())


