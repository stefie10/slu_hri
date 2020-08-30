from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as na

COL_INDEX = 0
COL_NAME = 1
COL_LOCATION = 2
COL_LANDMARK_PROBABILITY = 3
COL_SREL_MAT_PROBABILITY = 4




class Model(QAbstractTableModel):
    def __init__(self, view, m4du):
        QAbstractTableModel.__init__(self)
        self.m4du = m4du
        self.tagName = None
        self.loaded = False

        self.view = view
        self.view.setModel(self)


    def load(self, sdc, L_mat, v1_i, v2_i):
        print "Loading"
        self.indices = na.arange(len(L_mat))
        self.sdc = sdc
        self.L_mat = L_mat
        if sdc["sr"] != None:
            self.sr_i = self.m4du.sr_class.engineToIdx(sdc["sr"])
        else:
            self.sr_i = None
        self.t1_i = self.m4du.vp_i_to_topo_i[v1_i]
        self.t2_i = self.m4du.vp_i_to_topo_i[v2_i]
        self.loaded = True

        self.reset()
        
    def columnCount(self, parent):
        return 5
    def rowCount(self, parent):
        if self.loaded:
            return len(self.L_mat)
        else:
            return 0



    def get(self, idx):
        return self.indices[idx]
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()

        l_i = self.get(idx.row())

        if role != Qt.DisplayRole:
            return QVariant()
            
        if col == COL_INDEX:
            return QVariant("%d" % l_i)
        elif col == COL_NAME:
            return QVariant("%s" % self.m4du.obj_geometries[l_i].tag)
        elif col == COL_LOCATION:
            mymap = self.m4du.clusters.get_map()
            point = mymap.to_xy(self.m4du.obj_geometries[l_i].centroid())
            return QVariant("%.2f, %.2f" % tuple(point))
        elif col == COL_LANDMARK_PROBABILITY:
            return QVariant("%.5f" % self.L_mat[l_i])
        elif col == COL_SREL_MAT_PROBABILITY:
            if self.sr_i == None:
                return QVariant("No sr")
            else:
                return QVariant("%.5f" % self.m4du.srel_mat[self.sr_i, self.t1_i, self.t2_i, l_i])
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_INDEX:
                return QVariant("Index")
            elif section == COL_NAME:
                return QVariant("Name")
            elif section == COL_LOCATION:
                return QVariant("Location")
            elif section == COL_LANDMARK_PROBABILITY:
                if self.loaded:
                    landmark = self.sdc["landmark"]
                else:
                    landmark = "X"
                return QVariant("P[%s]" % landmark)
            elif section == COL_SREL_MAT_PROBABILITY:
                return QVariant("srel_mat")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()

    def sort(self, col, order):
        if col == COL_LANDMARK_PROBABILITY:
            self.indices = na.argsort(self.L_mat)
        elif col == COL_SREL_MAT_PROBABILITY:
            self.indices = na.argsort(self.m4du.srel_mat[self.sr_i, self.t1_i, self.t2_i, :])
        else:
            self.indices = na.arange(len(self.L_mat))

        if order == Qt.DescendingOrder:
            self.indices = self.indices[::-1]
        self.reset()

    def selectedData(self):
        return self.get(self.view.currentIndex().row())
