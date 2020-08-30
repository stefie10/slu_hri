from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qt_utils import Counter

c = Counter()

COL_FIGURE_TEXT = c.pp()
COL_VERB_TEXT = c.pp()
COL_SPATIAL_RELATION_TEXT = c.pp()
COL_LANDMARK_TEXT = c.pp()
COL_LANDMARK2_TEXT = c.pp()





class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self.view = view
        self.setAnnotations([])
        view.setModel(self)


    def setAnnotations(self, annotations):
        self._data = annotations
        self.reset()
        
    def addAnnotation(self, annotation):
        self._data.append(annotation)
        self.reset()

    def deleteAnnotation(self, idx):
        del self._data[idx]
        self.reset()        
        
    def columnCount(self, parent):
        return c.cnt
    def rowCount(self, parent):
        return len(self._data)

    def get(self, idx):
        annotation = self._data[idx.row()]
        return annotation

    def selectedData(self):
        return self.get(self.view.currentIndex())

    def data(self, idx, role=Qt.DisplayRole):
        annotation = self.get(idx)
        

        
        col = idx.column()
        if role != Qt.DisplayRole:
            return QVariant()            
        
        if col == COL_SPATIAL_RELATION_TEXT:
            return QVariant(annotation.spatialRelation.text)
        elif col == COL_LANDMARK_TEXT:
            return QVariant(annotation.landmark.text)
        elif col == COL_LANDMARK2_TEXT:
            return QVariant(annotation.landmark2.text)        
        elif col == COL_FIGURE_TEXT:
            return QVariant(annotation.figure.text)
        elif col == COL_VERB_TEXT:
            return QVariant(annotation.verb.text)
        else:
            raise ValueError("Bad id: %s" % col)
        
        
