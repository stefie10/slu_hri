from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter


counter = Counter()

counter = Counter()
COL_DIALOG_ID = counter.pp()
COL_NUM_TURNS = counter.pp()


 
class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self.entries = []
        self.view = view
        self.view.setModel(self)
 
    def load(self, dialogs):
        self.entries = dialogs
        self.reset()
                    
    def columnCount(self, parent):
        return counter.cnt

    def rowCount(self, parent):
        return len(self.entries)

    def get(self, idx):
        return self.entries[idx]
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        e = self.get(idx.row())
        
        if role != Qt.DisplayRole:
            return QVariant()         
        if col == COL_DIALOG_ID:
            return QVariant(`e.id`)
        elif col == COL_NUM_TURNS:
            return QVariant(`len(e.turns)`)        
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == COL_DIALOG_ID:
                return QVariant("dialog_id")
            elif col == COL_NUM_TURNS:
                return QVariant("num_turns")            
            else:
                raise ValueError("Bad id: %s" % col)
        else:
            return QVariant()
                         
    def selectedData(self):
        return self.get(self.view.currentIndex().row())
    

                    
