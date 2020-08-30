from PyQt4.QtCore import *
import math2d
from PyQt4.QtGui import *
import numpy as na


COL_SCORE = 0 
COL_LANDMARK = 1
COL_DIST_TO_ENDPOINTS = 2
COL_SLOC = 3
COL_ELOC = 4
COL_IDX_TUPLE = 5
COL_ROW_NUM = 6

class EngineData:
    def __init__(self, m4du, engine, engineIdx, srel_mat):
        self.engine = engine
        self.engineIdx = engineIdx
        self.smat = srel_mat[engineIdx]
        self.flatMat = na.ravel(self.smat)

        self.indices = na.arange(len(self.flatMat))

        self.indices = na.take(self.indices, na.arange(0, len(self.flatMat),
                                                       len(m4du.obj_names)));


        self.indices = self.indices[na.argsort(na.take(self.flatMat, 
                                                       self.indices))]
        
        self.indices = na.argsort(self.flatMat)

        self.indices = self.indices[::-1]

        #self.entries = [(i,) + self.get_raw(i) for i in range(self.rowCount())]

    def idxForKey(self, i):
        value = (self.engineIdx,) + na.unravel_index(self.indices[i], self.smat.shape)
        return value
    def data(self, i):
        value =  self.flatMat[self.indices[i]]
        return value

    def rowCount(self):
        return len(self.indices)

    def get_raw(self, i):
        v1 = self.engine
        v2 = self.idxForKey(i)
        v3 = self.data(i)
        return v1, v2, v3

    def get(self, i):
        return self.get_raw(i)

class Model(QAbstractTableModel):
    def __init__(self, view, m4du):
        QAbstractTableModel.__init__(self)
        self.m4du = m4du
        self.maxExamples = len(na.ravel(m4du.srel_mat[0]))
        self.engineToSortedMatrix = {}

        self.selectEngine(self.m4du.sr_class.engineNames[0])


        self.view = view
        self.view.setModel(self)
        

    def columnCount(self, parent):
        return 7
    def rowCount(self, parent):
        return self.currentEngineData().rowCount()

    def selectedData(self):
        engineData = self.currentEngineData()
        engine, idxTuple, data = engineData.get(self.view.currentIndex().row())
                                                
        return engine, idxTuple, data
    
    def selectEngine(self, key):
        assert key in self.m4du.sr_class.engineNames

        if not key in self.engineToSortedMatrix:
            self.engineToSortedMatrix[key] = \
                EngineData(self.m4du,
                self.m4du.sr_class.engineMap[key], 
                self.m4du.sr_class.engineToIdx(key),
                self.m4du.srel_mat)
        self.selectedEngine = key
        self.reset()

    def currentEngineData(self):
        return self.engineToSortedMatrix[self.selectedEngine]



    def data(self, midx, role=Qt.DisplayRole):
        engineData = self.currentEngineData()
        col = midx.column()
        idx = midx.row()
        #idx = midx.row()
        metadata = self.m4du.metadataForMatrixKey(engineData.idxForKey(idx),
                                                  wantArgs=False)
        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_SCORE:
            return QVariant("%e" % engineData.data(idx))
        elif col == COL_LANDMARK:
            return QVariant(metadata.groundName)
        elif col == COL_DIST_TO_ENDPOINTS:
            return QVariant(math2d.dist(metadata.sloc, metadata.eloc))
        elif col == COL_SLOC:
            return QVariant("(%.3f, %.3f)" % tuple(metadata.sloc))
        elif col == COL_ELOC:
            return QVariant("(%.3f, %.3f)" % tuple(metadata.eloc))
        elif col == COL_IDX_TUPLE:
            return QVariant(`metadata.key`)
        elif col == COL_ROW_NUM:
            return QVariant(idx)
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_SCORE:
                return QVariant("Score")
            elif section == COL_LANDMARK:
                return QVariant("Ground")
            elif section == COL_DIST_TO_ENDPOINTS:
                return QVariant("Dst btwn VPs")
            elif section == COL_SLOC:
                return QVariant("sloc")
            elif section == COL_ELOC:
                return QVariant("eloc")
            elif section == COL_IDX_TUPLE:
                return QVariant("key")
            elif section == COL_ROW_NUM:
                return QVariant("row")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()
 
