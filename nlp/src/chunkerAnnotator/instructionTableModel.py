from PyQt4.QtCore import *
from PyQt4.QtGui import *
COL_NULL = 0
COL_TIMESTAMP = 1
COL_SUBJECT = 2
COL_FLOOR = 3
COL_INSTRUCTION = 4




class Model(QAbstractTableModel):
    def __init__(self, view, sessions):
        QAbstractTableModel.__init__(self)

        self.view = view
        
        self._data = []
        for s in sessions:
            for i, r in enumerate(s.routeInstructions):
                self._data.append((i, s))

        print 'data in table', len(self._data)
        view.setModel(self)

    def columnCount(self, parent):
        return 5
    def rowCount(self, parent):
        return len(self._data)

    def get(self, idx):
        instructionIdx, session = self._data[idx.row()]
        instruction = session.routeInstructions[instructionIdx]
        return session, instructionIdx, instruction

    def selectedData(self):
        return self.get(self.view.currentIndex())


    def data(self, idx, role=Qt.DisplayRole):
        session, instructionIdx, instruction = self.get(idx)

        
        col = idx.column()
        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_NULL:
            return QVariant()
        elif col == COL_TIMESTAMP:
            return QVariant(session.timestamp)
        elif col == COL_FLOOR:
            return QVariant(session.floor)
        elif col == COL_INSTRUCTION:
            return QVariant(instruction)
        elif col == COL_SUBJECT:
            return QVariant(session.subject)
        else:
            raise ValueError("Bad id: %s" % col)
        
        
