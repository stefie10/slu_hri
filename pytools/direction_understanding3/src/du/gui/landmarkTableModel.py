from PyQt4.QtCore import *
from PyQt4.QtGui import *

COL_NAME = 0
COL_PROBABILITY = 1
COL_SREL_PROBABILITY = 2
COL_OBS_PROBABILITY = 3
COL_INDEX = 4
COL_LOCATION = 5

class Entry:
    def __init__(self, m4du, i, L_mat, SR_mat, num_topologies, iSloc, iEloc):
        self.L_mat = L_mat
        self.SR_mat = SR_mat

        self.i = i
        self.m4du = m4du
        self.iSloc = None
        self.iEloc = None
        self.setEndPoints(iSloc, iEloc)
        self.num_topologies = num_topologies

    def setEndPoints(self, iSloc=None, iEloc=None):
        if iSloc != None:
            self.iSloc = iSloc
            self.iSlocTopo = self.m4du.vp_i_to_topo_i[iSloc]
        if iEloc != None:
            self.iEloc = iEloc
            self.iElocTopo = self.m4du.vp_i_to_topo_i[iEloc]

    @property
    def geometry_obj(self):
        return self.m4du.obj_geometries[self.i]

    @property
    def name(self):
        return self.geometry_obj.tag

    @property
    def location(self):
        return self.m4du.clusters.get_map().to_xy(self.geometry_obj.centroid())
    
        
    @property
    def has_viewpoints(self):
        return self.iSloc != None and self.iEloc != None
        
    @property
    def l_prob(self):
        return self.L_mat[self.i]

    @property
    def o_mat_prob(self):
        if self.has_viewpoints:
            return self.L_mat[self.iEloc]

    @property
    def o_prob(self):
        if self.has_viewpoints:
            return self.l_prob * self.sr_prob
        else:
            return None
    
    @property
    def sr_prob(self):
        if self.has_viewpoints:
            return self.SR_mat[self.iSlocTopo*self.num_topologies + 
                               self.iElocTopo][self.i]
        else:
            return None


        

class Model(QAbstractTableModel):
    def __init__(self, view, m4du):
        QAbstractTableModel.__init__(self)

        self.m4du = m4du

        self.tagName = None
        self._data = []

        self.view = view
        self.view.setModel(self)
        
    def setData(self, m4du, tagName, L_mat, SR_mat, num_topologies, iSloc, iEloc):
        self.tagName = tagName
        self._data = []
        for i in range(len(L_mat)):
            self._data.append(Entry(m4du, i, L_mat, SR_mat, num_topologies, iSloc, iEloc))
        self.reset()
            
    def columnCount(self, parent=None):
        return 6
    def rowCount(self, parent=None):
        return len(self._data)

    def selectSloc(self, idx):
        for e in self._data:
            e.setEndPoints(iSloc=idx)
        self.reset()

    def selectEloc(self, idx):
        for e in self._data:
            e.setEndPoints(iEloc=idx)
        self.reset()


    def get(self, viewIdx):
        return self._data[viewIdx]

    def selectedData(self):
        return self.get(self.view.currentIndex().row())
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()

        e = self.get(idx.row())

        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_NAME:
            return QVariant(e.name)
        elif col == COL_LOCATION:
            return QVariant("%.2f, %.2f" % tuple(e.location))
        elif col == COL_PROBABILITY:
            return QVariant("%e" % e.l_prob)
        elif col == COL_SREL_PROBABILITY:
            if e.has_viewpoints:
                return QVariant("%e" % e.sr_prob)
            else:
                return QVariant("")
        elif col == COL_OBS_PROBABILITY:
            if e.has_viewpoints:
                return QVariant("%e" % e.o_prob)
            else:
                return QVariant("")
        elif col == COL_INDEX:
            return QVariant("%d" % e.i)
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_NAME:
                return QVariant("Name")
            elif section == COL_LOCATION:
                return QVariant("Location")
            elif section == COL_PROBABILITY:
                return QVariant("P[%s]" % self.tagName)
            elif section == COL_OBS_PROBABILITY:
                return QVariant("p_obs")
            elif section == COL_SREL_PROBABILITY:
                return QVariant("p_srel")
            elif section == COL_INDEX:
                return QVariant("srel_mat index")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()

    def sort(self, col, order):


        if col == COL_PROBABILITY:
            self._data.sort(key=lambda e: e.l_prob)
        elif col == COL_OBS_PROBABILITY:
            self._data.sort(key=lambda e: e.o_prob)
        elif col == COL_SREL_PROBABILITY:
            self._data.sort(key=lambda e: e.sr_prob)
        elif col == COL_INDEX:
            self._data.sort(key=lambda e: e.i)
        elif col == COL_NAME:
            self._data.sort(key=lambda e: e.name)            

        if order == Qt.DescendingOrder:
            self._data.reverse()
            
        self.reset()
            
        
