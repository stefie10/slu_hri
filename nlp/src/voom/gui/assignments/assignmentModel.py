from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter, convertVariant
from voom.gui.assignments import assignmentData
import comboBoxDelegate
import traceback



counter = Counter()
COL_ID = counter.pp()
COL_VERB = counter.pp()
COL_COMMAND = counter.pp()



class Model(QAbstractTableModel):
    def __init__(self, verbMap, view, isEditable=False):
        QAbstractTableModel.__init__(self)

        self.verbMap = verbMap
        self.isEditable = isEditable
        self.assignment = None
        boxData = list(enumerate(sorted(self.verbMap.keys())))
        self.verbDelegate = comboBoxDelegate.Delegate(boxData)

        self.view = view
        self.view.setModel(self)
        self.view.setItemDelegateForColumn(COL_VERB, self.verbDelegate)
        self.view.setColumnWidth(COL_VERB, 50)
        self.view.setColumnWidth(COL_COMMAND, 400) 
    def loadData(self, assignment):
        assert isinstance(assignment, assignmentData.Assignment), assignment
        self.assignment = assignment
        self.reset()

    @property
    def entries(self):
        try:
            if self.assignment == None:
                return []
            else:
                return self.assignment.entries
        except:
            traceback.print_exc()
            raise
        

    def columnCount(self, parent):
        return counter.cnt

    def rowCount(self, parent):
        return len(self.entries)

    

    def get(self, i):
        return self.entries[i]
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        e = self.get(idx.row())
        
        if role != Qt.DisplayRole:
            return QVariant()         
        
        if col == COL_VERB:
            return QVariant(e.verb)
        elif col == COL_COMMAND:
            return QVariant(e.command)
        elif col == COL_ID:
            return QVariant(e.id)
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_VERB:
                return QVariant("verb")
            elif section == COL_COMMAND:
                return QVariant("command")
            elif section == COL_ID:
                return QVariant("ID")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()
                         
    def selectedData(self):
        return self.get(self.view.currentIndex().row())

    def setData(self, idx, value, role):
        entry = self.get(idx.row())
        if idx.column() == COL_VERB:
            verbIdx = convertVariant(value)
            entry.verb = self.verbDelegate.valueForIdx(verbIdx)
            self.emit(SIGNAL("dataChanged"), (idx, idx))
            return True
        elif idx.column() == COL_COMMAND:
            entry.command = convertVariant(value)
            return True
        else:
            return False
                         

    def flags(self, idx):
        baseflags = QAbstractTableModel.flags(self, idx)
        if idx.column() in [COL_VERB,COL_COMMAND] and self.isEditable:
            baseflags = baseflags | Qt.ItemIsEditable
        return baseflags
