from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyTklib import tklib_du_lp_obs_array, tklib_du_lp_sr_array
from qt_utils import Counter
import numpy as na

counter = Counter()

COL_SR_TIMES_TRANS_TIMES_VERB = counter.pp()
COL_P_OBS = counter.pp()
COL_P_TRANS = counter.pp()
COL_P_VERB = counter.pp()
COL_P_SR = counter.pp()
COL_P_PREV = counter.pp()
COL_P_CURR = counter.pp()
COL_I_SLOC = counter.pp()
COL_I_ELOC = counter.pp()
COL_SLOC = counter.pp()
COL_SLOC_STR = counter.pp()
COL_ELOC = counter.pp()
COL_ELOC_STR = counter.pp()


class Entry:
    def __init__(self, m4du, iSlocVp, iElocVp, p_obs, p_trans, p_prev, p_curr, p_verb, p_sr):
        self.iSloc = iSlocVp
        self.iEloc = iElocVp

        self.slocStr = m4du.viewpoints[self.iSloc]
        self.elocStr = m4du.viewpoints[self.iEloc]


        slocTopo_st, self.sloc_ang = self.slocStr.split("_")
        elocTopo_st, self.eloc_ang = self.elocStr.split("_")

        self.sloc_ang = float(self.sloc_ang)
        self.eloc_ang = float(self.eloc_ang)
        
        self.keySlocTopo = float(slocTopo_st)
        self.keyElocTopo = float(elocTopo_st)

        self.iSlocTopo = m4du.vp_i_to_topo_i[self.iSloc]
        self.iElocTopo = m4du.vp_i_to_topo_i[self.iEloc]
        
        #self.sloc = m4du.tmap_locs[self.keySlocTopo]
        #self.eloc = m4du.tmap_locs[self.keyElocTopo]
        
        self.sloc = m4du.vp_i_to_loc(self.iSloc)
        self.eloc = m4du.vp_i_to_loc(self.iEloc)
        
        self.p_obs = p_obs
        self.p_trans = p_trans
        self.p_prev = p_prev
        self.p_curr = p_curr
        self.p_verb = p_verb
        self.p_sr = p_sr

class Model(QAbstractTableModel):
    def __init__(self, view, m4du):
        QAbstractTableModel.__init__(self)
        self.m4du = m4du
        self._data = []
        self._alldata = []
        self.view = view
        self.view.setModel(self)


    def load(self, O_mat, T_mat, D_mat, SR_mat, L_mat, topo_to_location_mask, P_prev=None, P_curr=None):
        self._alldata = []
        num_topologies = len(self.m4du.tmap.keys())
        print "L", L_mat.shape
        pobs_matrix = na.exp(tklib_du_lp_obs_array(len(self.m4du.viewpoints),
                                                   self.m4du.vp_i_to_topo_i + 0.0,
                                                   na.log(T_mat),
                                                   na.log(D_mat),
                                                   na.log(SR_mat),
                                                   na.log(L_mat),
                                                   na.log(O_mat),
                                                   topo_to_location_mask,
                                                   num_topologies))


        psr_matrix = na.exp(tklib_du_lp_sr_array(len(self.m4du.viewpoints),
                                                 self.m4du.vp_i_to_topo_i + 0.0,
                                                 na.log(SR_mat),
                                                 na.log(L_mat),
                                                 na.log(O_mat),
                                                 num_topologies))
        
        for v1_i in range(len(self.m4du.viewpoints)):
            for v2_i in range(len(self.m4du.viewpoints)):
                p_obs = pobs_matrix[v1_i][v2_i]
                p_trans = T_mat[v2_i, v1_i]
                if P_prev != None:
                    p_prev = P_prev[v1_i, v2_i]
                else:
                    p_prev = None
                if P_curr != None:
                    p_curr = P_curr[v1_i, v2_i]
                else:
                    p_curr = None
                p_verb = D_mat[v1_i, v2_i]
                p_sr = psr_matrix[v1_i, v2_i]
                                      
                self._alldata.append(Entry(self.m4du, v1_i, v2_i, p_obs, p_trans, p_prev, p_curr, p_verb, p_sr))
        self._data = self._alldata

        self.reset()


    def columnCount(self, parent):
        return counter.cnt
    def rowCount(self, parent):
        return len(self._data)

    def get(self, i):
        return self._data[i]
    
    def selectedData(self):
        return self.get(self.view.currentIndex().row())
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        e = self.get(idx.row())
        
        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_SLOC:
            return QVariant("%.2f, %.2f" % tuple(e.sloc))
        elif col == COL_ELOC:
            return QVariant("%.2f, %.2f" % tuple(e.eloc))
        elif col == COL_I_SLOC:
            return QVariant("%d" % e.iSloc)
        elif col == COL_I_ELOC:
            return QVariant("%d" % e.iEloc)
        elif col == COL_SLOC_STR:
            return QVariant("%s" % e.slocStr)
        elif col == COL_ELOC_STR:
            return QVariant("%s" % e.elocStr)
        elif col == COL_P_OBS:
            return QVariant("%e" % e.p_obs)
        elif col == COL_P_SR:
            if e.p_sr != None:
                return QVariant("%e" % e.p_sr)        
            else:
                return QVariant(`e.p_sr`) 
        elif col == COL_P_TRANS:
            return QVariant("%e" % e.p_trans)
        elif col == COL_P_VERB:
            return QVariant("%e" % e.p_verb)
        elif col == COL_SR_TIMES_TRANS_TIMES_VERB:
            if e.p_sr != None:
                return QVariant("%e" % (e.p_trans * e.p_sr * e.p_verb))        
            else:
                return QVariant("p_sr is None")
        elif col == COL_P_PREV:
            if e.p_prev != None:
                return QVariant("%e" % e.p_prev)
            else:
                return QVariant("Unknown")
        elif col == COL_P_CURR:
            if e.p_curr != None:
                return QVariant("%e" % e.p_curr)
            else:
                return QVariant("Unknown")
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_SLOC:
                return QVariant("sloc")
            elif section == COL_ELOC:
                return QVariant("eloc")
            elif section == COL_P_OBS:
                return QVariant("p_obs")
            elif section == COL_P_TRANS:
                return QVariant("p_trans")
            elif section == COL_P_VERB:
                return QVariant("p_verb")
            elif section == COL_SR_TIMES_TRANS_TIMES_VERB:
                return QVariant("p_trans * p_sr * p_verb")            
            elif section == COL_P_PREV:
                return QVariant("p_prev")
            elif section == COL_P_SR:
                return QVariant("p_sr")            
            elif section == COL_P_CURR:
                return QVariant("p_curr")
            elif section == COL_I_SLOC:
                return QVariant("sloc idx")
            elif section == COL_I_ELOC:
                return QVariant("eloc idx")
            elif section == COL_SLOC_STR:
                return QVariant("sloc str")
            elif section == COL_ELOC_STR:
                return QVariant("sloc str")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()


    def sort(self, col, order):
        if col == COL_SLOC or col == COL_I_SLOC:
            self._data.sort(key=lambda e: e.iSloc)
        elif col == COL_ELOC or col == COL_I_ELOC:
            self._data.sort(key=lambda e: e.iEloc)
        elif col == COL_P_OBS:
            self._data.sort(key=lambda e: e.p_obs)
        elif col == COL_P_TRANS:
            self._data.sort(key=lambda e: e.p_trans)
        elif col == COL_SR_TIMES_TRANS_TIMES_VERB:           
            self._data.sort(key=lambda e: e.p_trans * e.p_sr * e.p_verb) 
        elif col == COL_P_PREV:
            self._data.sort(key=lambda e: e.p_prev)
        elif col == COL_P_SR:
            self._data.sort(key=lambda e: e.p_sr)
        elif col == COL_P_CURR:
            self._data.sort(key=lambda e: e.p_curr)
        elif col == COL_P_VERB:
            self._data.sort(key=lambda e: e.p_verb)
        if order == Qt.DescendingOrder:
            self._data.reverse()
        self.reset()
            

    def setFilter(self, iSloc=None, iEloc=None):
        self._data = []
        for e in self._alldata:
            if ((iSloc == None or e.iSloc == iSloc) and
                (iEloc == None or e.iEloc == iEloc)):
                self._data.append(e)
        self.reset()
