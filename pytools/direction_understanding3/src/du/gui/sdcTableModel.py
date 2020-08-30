from PyQt4.QtCore import Qt, QAbstractTableModel, QVariant


from qt_utils import Counter
counter = Counter()

COL_VERB = counter.pp()
COL_SPATIAL_RELATION = counter.pp()
COL_LANDMARKS = counter.pp()
COL_V1 = counter.pp()
COL_V2 = counter.pp()
COL_USED_EPSILON = counter.pp()
COL_FIGURE = counter.pp()
COL_LANDMARK = counter.pp()
COL_KEYWORD_SDC = counter.pp()

class Entry:
    def __init__(self, i, m4du, sdc, v1Txt, v2Txt):
        self.i = i
        self.m4du = m4du
        self.sdc = sdc
        self.v1Txt = v1Txt
        self.v2Txt = v2Txt
        if v1Txt != None:
            self.v1 = self.m4du.vpt_to_num[self.v1Txt]
        else:
            self.v1 = None

        if v2Txt != None:
            self.v2 = self.m4du.vpt_to_num[self.v2Txt]
        else:
            self.v2 = None

        if hasattr(self.m4du.mygm, "used_epsilons"):
            self.used_epsilon = self.m4du.mygm.used_epsilons[i][self.v1, self.v2]
        else:
            self.used_epsilon = None


class Model(QAbstractTableModel):
    def __init__(self, m4du, view):
        QAbstractTableModel.__init__(self)
        self._data = []
        self.m4du = m4du
        self.view = view
        self.view.setModel(self)
        
        


    def columnCount(self, parent):
        return 8
    def rowCount(self, parent):
        return len(self._data)
    def setData(self, data, path=None):
        self._data = []
        for i, sdc in enumerate(data):
            p1 = None
            p2 = None
            if path != None and i + 1 < len(path):
                p1 = path[i]
                p2 = path[i+1]

            self._data.append(Entry(i, self.m4du, sdc, p1, p2))
        self.reset()
    def get(self, i):
        return self._data[i]

    def selectedData(self):
        entry = self.get(self.view.currentIndex().row())
        return entry
    
    def data(self, idx, role=Qt.DisplayRole):

        e = self.get(idx.row())
        sdc = e.sdc
        col = idx.column()
        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_FIGURE:
            return QVariant(sdc["figure"])
        elif col == COL_VERB:
            return QVariant(sdc["verb"])
        elif col == COL_SPATIAL_RELATION:
            return QVariant(sdc["sr"])
        elif col == COL_V1:
            return QVariant(e.v1)
        elif col == COL_V2:
            return QVariant(e.v2)
        elif col == COL_LANDMARK:
            return QVariant(`sdc["landmark"]`)
        elif col == COL_LANDMARKS:
            return QVariant(`sdc["landmarks"]`)
        elif col == COL_USED_EPSILON:
            return QVariant(e.used_epsilon)
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == COL_FIGURE:
                return QVariant("Figure")
            elif section == COL_VERB:
                return QVariant("Verb")
            elif section == COL_SPATIAL_RELATION:
                return QVariant("Spatial Relation")
            elif section == COL_LANDMARK:
                return QVariant("Landmark")
            elif section == COL_LANDMARKS:
                return QVariant("Landmarks")
            elif section == COL_V1:
                return QVariant("v1")
            elif section == COL_V2:
                return QVariant("v2")
            elif section == COL_USED_EPSILON:
                return QVariant("used epsilon")
            else:
                raise ValueError("Bad id: %s" % section)
        else:
            return QVariant()
