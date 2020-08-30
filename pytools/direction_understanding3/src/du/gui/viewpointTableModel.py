from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter

counter = Counter()
COL_INDEX = counter.pp()
COL_O_MAT_PROB = counter.pp()
COL_LOCATION = counter.pp()
COL_TOPO_INDEX = counter.pp()
COL_TOPO_KEY = counter.pp()

COL_TOPO_VTAGS = counter.pp()
COL_VP_VTAGS = counter.pp()

class Entry:
    def __init__(self, m4du, vp_i, O_mat = None):
        self.m4du = m4du
        self.vp_i = vp_i
        self.topo_i = self.m4du.vp_i_to_topo_i[self.vp_i]
        topo_st, ang = self.m4du.viewpoints[vp_i].split("_")
        self.topo_key = float(topo_st)
        self.loc = self.m4du.tmap_locs[self.topo_key]

        self.loc_xyz = self.m4du.tmap_locs_3d[self.topo_key]
        if len(self.loc_xyz) == 2:
            x, y = self.loc_xyz
            self.loc_xyz = (x, y, 0)
        self.angle = float(ang)
        self.O_mat = O_mat
        
        self.topo_vtags = self.m4du.topo_key_to_vtags[self.topo_key]
        self.vp_vtags = self.m4du.vp_i_to_vtags[self.vp_i]
    
    @property
    def o_mat_prob(self):
        if self.O_mat != None and len(self.O_mat) != 0:
            return self.O_mat[self.vp_i]
        else:
            return None
        


class Model(QAbstractTableModel):
    def __init__(self, view, m4du, title):
        QAbstractTableModel.__init__(self)
        self.m4du = m4du
        self.title = title
        self._data = []
        for i, vp in enumerate(self.m4du.viewpoints):
            self._data.append(Entry(self.m4du, i))

        self.view = view
        self.view.setModel(self)

        self.view.setColumnWidth(COL_INDEX, 35)
        self.view.setColumnWidth(COL_TOPO_INDEX, 100)  
        self.view.setColumnWidth(COL_TOPO_KEY, 100)  
        
    def columnCount(self, parent):
        return counter.cnt
    def rowCount(self, parent):
        return len(self._data)

    def setData(self, O_mat):
        for e in self._data:
            e.O_mat = O_mat
        self.reset()
    def get(self, i):
        return self._data[i]

    def selectedEntries(self):
        return [self.get(e.row()) 
                for e in self.view.selectionModel().selectedRows()]
    def selectedData(self):
        return self.get(self.view.currentIndex().row())
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()

        e = self.get(idx.row())
        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_LOCATION:
            return QVariant("%.2f, %.2f, %.2f" % tuple(e.loc_xyz))
        elif col == COL_INDEX:
            return QVariant("%d" % e.vp_i)
        elif col == COL_TOPO_INDEX:
            return QVariant("%d" % e.topo_i)
        elif col == COL_TOPO_KEY:
            return QVariant("%d" % e.topo_key)        
        elif col == COL_O_MAT_PROB:
            if e.o_mat_prob != None:
                return QVariant("%e" % e.o_mat_prob)
            else:
                return QVariant("")
        elif col == COL_TOPO_VTAGS:
            return QVariant(`e.topo_vtags`)
        elif col == COL_VP_VTAGS:
            return QVariant(`e.vp_vtags`)
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_LOCATION:
                return QVariant(self.title)
            elif section == COL_INDEX:
                return QVariant("Idx")
            elif section == COL_TOPO_INDEX:
                return QVariant("Topo Index")
            elif section == COL_TOPO_KEY:
                return QVariant("Topo Key")            
            elif section == COL_O_MAT_PROB:
                return QVariant("p_o_mat")
            elif section == COL_TOPO_VTAGS:   
                return QVariant("topo vtags")
            elif section == COL_VP_VTAGS:   
                return QVariant("vp vtags")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()


    def sort(self, col, order):


        if col == COL_INDEX:
            self._data.sort(key=lambda e: e.vp_i)
        elif col == COL_O_MAT_PROB:
            self._data.sort(key=lambda e: e.o_mat_prob)
        elif col == COL_LOCATION:
            self._data.sort(key=lambda e: `e.loc`)
        elif col == COL_TOPO_INDEX:
            self._data.sort(key=lambda e: e.topo_i)
        elif col == COL_TOPO_KEY:
            self._data.sort(key=lambda e: e.topo_key)
        elif col == COL_TOPO_VTAGS:
            self._data.sort(key=lambda e: `e.topo_vtags`)
        elif col == COL_VP_VTAGS:
            self._data.sort(key=lambda e: `e.vp_vtags`)

        if order == Qt.DescendingOrder:
            self._data.reverse()
            
        self.reset()
            
        
