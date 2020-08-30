from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter

counter = Counter()
COL_SR = counter.pp()
COL_LANDMARK = counter.pp() 
COL_GEOMETRY = counter.pp() 



class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self._data = []
        self.view = view
        self.view.setModel(self)

        
    def loadData(self, data):
        self._data = data
        self.reset()


    def columnCount(self, parent):
        return counter.cnt

    def rowCount(self, parent):
        return len(self._data)

    def get(self, i):
        return self._data[i]
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        sr, landmark, geometry = self.get(idx.row())
        
        if role != Qt.DisplayRole:
            return QVariant()         
        
        if col == COL_GEOMETRY:
            return QVariant("%s" % `geometry`)
        elif col == COL_SR: 
            return QVariant("%s" % sr)
        elif col == COL_LANDMARK: 
            return QVariant("%s" % sr)        
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_SR:
                return QVariant("SR")
            elif section == COL_LANDMARK:
                return QVariant("Landmark")
            elif section == COL_GEOMETRY:
                return QVariant("Geometry")            
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()
                         
    def selectedData(self):
        return self.get(self.view.currentIndex().row())


