from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter, convertVariant
import comboBoxDelegate
import math2d
import traceback
import turtle


counter = Counter()



COL_NAME = counter.pp()
COL_PATH = counter.pp()
COL_GEOMETRY = counter.pp()
COL_TURTLE = counter.pp()
COL_LENGTH = counter.pp()
COL_TIME = counter.pp()
COL_START_TIME = counter.pp()
COL_END_TIME = counter.pp()


class Model(QAbstractTableModel):
    def __init__(self, view, assignmentEntry, tagFile, skeleton):
        QAbstractTableModel.__init__(self)


        self.tagFile = tagFile
        self.skeleton = skeleton
        
        self.setAssignmentEntry(assignmentEntry)
        

        self._turtleClasses = [turtle.PlaybackTurtle,
                               turtle.SplineTurtle,
                               turtle.RandomTurtle,
                               turtle.KeyboardTurtle,
                               turtle.StaticTurtle,
                               turtle.FollowTurtle,
                               ]
        
        boxData = [(idx, t.name) for idx, t in enumerate(self._turtleClasses)]
        self.turtleDelegate = comboBoxDelegate.Delegate(boxData)
        

        self.view = view
        self.view.setItemDelegateForColumn(COL_TURTLE, self.turtleDelegate)
        self.view.setModel(self)

    @property
    def situation(self):
        if self.assignmentEntry != None:
            return self.assignmentEntry.situation
        else:
            return None
    def setAssignmentEntry(self, assignmentEntry):
        self.assignmentEntry = assignmentEntry
        self.reset()
        
    

    def selectedData(self):
        idx = self.view.currentIndex().row()
        if idx == -1:
            return None
        else:
            return self.get(self.view.currentIndex().row())

    @property
    def agents(self):
        return self.situation.agents
    
    @property
    def entries(self):
        try:
            return self.assignmentEntry.controllers
        except:
            traceback.print_exc()
            raise
    def columnCount(self, parent):
        return counter.cnt

    def rowCount(self, parent):
        try:
            return len(self.entries)
        except:
            traceback.print_exc()
            raise

    def get(self, i):
        return self.entries[i]
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        a = self.get(idx.row())
        
        if role != Qt.DisplayRole:
            return QVariant()         

        if col == COL_PATH:
            return QVariant(`a.agent.data`)
        if col == COL_GEOMETRY:
            return QVariant(`a.agent.geometry(0)`)
        elif col == COL_NAME:
            return QVariant(a.agent.name)
        elif col == COL_TURTLE:
            return QVariant(a.turtle.name)
        elif col == COL_LENGTH:
            return QVariant(math2d.length(a.agent.positions))
        elif col == COL_TIME:
            if a.agent.endTime != None and a.agent.startTime != None:
                return QVariant((a.agent.endTime - a.agent.startTime)/1000.0)
            else:
                return QVariant()
        elif col == COL_START_TIME:
            return QVariant(str(a.agent.startTime))
        elif col == COL_END_TIME:
            return QVariant(str(a.agent.endTime))        
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_PATH:
                return QVariant("path")
            elif section == COL_NAME:
                return QVariant("name")
            elif section == COL_TURTLE:
                return QVariant("Controller")
            elif section == COL_GEOMETRY:
                return QVariant("Geometry")
            elif section == COL_TIME:
                return QVariant("Time")
            elif section == COL_LENGTH:
                return QVariant("Length")
            elif section == COL_START_TIME:
                return QVariant("Start Time")
            elif section == COL_END_TIME:
                return QVariant("End Time")                        
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()

    def setTurtle(self, row, turtleCls):
        entry = self.get(row)
        entry.setTurtleClass(turtleCls)
    def setData(self, idx, value, role):
        if idx.column() == COL_TURTLE:
            turtleIdx = convertVariant(value)
            self.setTurtle(idx.row(), self._turtleClasses[turtleIdx])
            self.emit(SIGNAL("dataChanged"), (idx, idx))
            return True
        else:
            return False
                         
    def flags(self, idx):
        baseflags = QAbstractTableModel.flags(self, idx)
        if idx.column() == COL_TURTLE:
            baseflags = baseflags | Qt.ItemIsEditable
        return baseflags

            
