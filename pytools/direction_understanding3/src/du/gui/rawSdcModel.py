from PyQt4.QtCore import *
from PyQt4.QtGui import *

COL_VERB = 0
COL_SR = 1
COL_LANDMARK = 2
COL_FIGURE = 3
class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self.sdcs = []
        self.view = view
        self.view.setModel(self)
        
    def load(self, sdcs):
        self.sdcs = sdcs
        self.reset()


    def columnCount(self, parent):
        return 4
    def rowCount(self, parent):
        return len(self.sdcs)

    def get(self, i):
        return self.sdcs[i]
    
    def selectedData(self):
        return self.get(self.view.currentIndex().row())
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        sdc = self.get(idx.row())
        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_FIGURE:
            return QVariant(sdc.figure.text)
        elif col == COL_VERB:
            return QVariant(sdc.verb.text)
        elif col == COL_SR:
            return QVariant(sdc.spatialRelation.text)
        elif col == COL_LANDMARK:
            return QVariant(sdc.landmark.text)
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_FIGURE:
                return QVariant("figure")
            elif section == COL_VERB:
                return QVariant("verb")
            elif section == COL_SR:
                return QVariant("sr")
            elif section == COL_LANDMARK:
                return QVariant("landmark")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()


