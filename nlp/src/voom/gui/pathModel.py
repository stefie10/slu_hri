from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter
from voom.agents import Agent





counter = Counter()
COL_TIME = counter.pp()
COL_LOC = counter.pp()
COL_THETA = counter.pp()



class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self.agent = Agent("empty", [])
        self.view = view
        self.view.setModel(self)
        self.view.setColumnWidth(COL_LOC, 150)
        
    def loadData(self, agent):
        self.agent= agent
        self.reset()


    def columnCount(self, parent):
        return counter.cnt

    def rowCount(self, parent):
        return len(self.agent.data)

    def get(self, i):
        return self.agent.data[i]
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        t, (x, y, theta) = self.get(idx.row())
        
        if role != Qt.DisplayRole:
            return QVariant()         
        
        if col == COL_TIME:
            return QVariant("%d" % t)
        elif col == COL_LOC: 
            return QVariant("%.3f, %.3f" % (x, y))
        elif col == COL_THETA: 
            return QVariant("%.3f" % theta)
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_TIME:
                return QVariant("Time")
            elif section == COL_LOC:
                return QVariant("Loc")
            elif section == COL_THETA:
                return QVariant("Theta")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()
                         
    def selectedData(self):
        return self.get(self.view.currentIndex().row())


