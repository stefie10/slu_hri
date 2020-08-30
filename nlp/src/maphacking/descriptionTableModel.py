from PyQt4.QtCore import *
from PyQt4.QtGui import *
COL_CLASSIFIER = 0
COL_LANDMARK = 1
COL_CLASS = 2
COL_SCORE = 3
COL_ANNOTATED_CLASS = 4


class DescriptionCandidate:
    def __init__(self, engine, landmarkPolygon, path):
        self.engine = engine
        self.landmark = landmarkPolygon
        self.path = path
        self.geometry = {"ground":self.landmark.vertices,
                         "figure":path}
        self.cls, self.dist = self.engine.classify(**self.geometry)
        self.score = self.dist[self.cls]

        print "cls", self.cls
        print "dist", self.dist

        print "score", self.score
        

                                                           



class Model(QAbstractTableModel):
    def __init__(self, view, descriptions):
        QAbstractTableModel.__init__(self)
        self.view = view
        self._data = descriptions
        view.setModel(self)

    def columnCount(self, parent):
        return 4
    def rowCount(self, parent):
        return len(self._data)

    def get(self, idx):
        dc = self._data[idx.row()]
        return dc

    def selectedData(self):
        return self.get(self.view.currentIndex())

    def data(self, idx, role=Qt.DisplayRole):
        dc = self.get(idx)
        

        
        col = idx.column()
        if role != Qt.DisplayRole:
            return QVariant()            
        
        if col == COL_CLASSIFIER:
            return QVariant(dc.engine.name())
        elif col == COL_LANDMARK:
            return QVariant(dc.landmark.tag)
        elif col == COL_CLASS:
            return QVariant(str(dc.cls))
        elif col == COL_SCORE:
            return QVariant(dc.score)
        else:
            raise ValueError("Bad id: %s" % col)
        
        
