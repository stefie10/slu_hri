from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter


counter = Counter()

counter = Counter()
COL_SPEAKER = counter.pp()
COL_UTTERANCE = counter.pp()
COL_START = counter.pp()
COL_END = counter.pp()
COL_DURATION = counter.pp()



 
class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self.entries = []
        self.view = view
        self.view.setModel(self)
 
    def load(self, turns):
        self.entries = turns
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

        if col == COL_SPEAKER:
            return QVariant(`e.speaker`)
        elif col == COL_UTTERANCE:
            return QVariant(`e.utterance`)
        elif col == COL_START:
            return QVariant(`e.start`)
        elif col == COL_END:
            return QVariant(`e.end`)
        elif col == COL_DURATION:
            return QVariant(`e.duration`)            
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:

            if col == COL_SPEAKER:
                return QVariant("speaker")
            elif col == COL_UTTERANCE:
                return QVariant("utterance")
            elif col == COL_START:
                return QVariant("start")
            elif col == COL_END:
                return QVariant("end")
            elif col == COL_DURATION:
                return QVariant("duration")
            else:
                raise ValueError("Bad id: %s" % col)

        else:
            return QVariant()
                         
    def selectedData(self):
        return self.get(self.view.currentIndex().row())
    

                    
