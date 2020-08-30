
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qt_utils import Counter
import tag_util

counter = Counter()

counter = Counter()
COL_TAG = counter.pp()
COL_CENTROID = counter.pp()
COL_TYPE = counter.pp()



class Entry:
    def __init__(self, tagFile, obj):
        self.tagFile = tagFile
        self.object = obj

    @property
    def tag(self):
        return self.object.tag

    @property
    def centroid(self):
        return self.object.centroid()

    @property
    def geometry_pixel(self):
        if isinstance(self.object, tag_util.point):
            return [self.object.x], [self.object.y]
        else:
            return self.object.X, self.object.Y
    @property
    def geometry(self):
        X_px, Y_px = self.geometry_pixel

        X = []
        Y = []
        for x, y in zip(X_px, Y_px):
            xp, yp = self.tagFile.get_map().to_xy([x, y])
            X.append(xp)
            Y.append(yp)
        return X, Y
        
class Model(QAbstractTableModel):
    def __init__(self, view):
        QAbstractTableModel.__init__(self)
        self.entries = []
        self.view = view
        self.view.setModel(self)
        self.view.setColumnWidth(COL_CENTROID, 200)
        self.view.setColumnWidth(COL_TAG, 200)
 
    def load(self, tagFile):
        self.tagFile = tagFile
        entries = []
        for o in tagFile.objects:
            entries.append(Entry(tagFile, o))
        self.entries = entries
        self.reset()
                    
    def columnCount(self, parent):
        return counter.cnt

    def rowCount(self, parent):
        return len(self.entries)

    def get(self, idx):
        return self.entries[idx]
    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()
        
        e = self.get(idx.row())
        
        if role != Qt.DisplayRole:
            return QVariant()         
        if col == COL_TAG:                        
            return QVariant(`e.tag`)
        elif col == COL_CENTROID:
            return QVariant(`e.centroid`)
        elif col == COL_TYPE:
            return QVariant(`e.object.__class__`)        
        else:
            raise ValueError("Bad id: %s" % col)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == COL_CENTROID:
                return QVariant("centroi")
            elif col == COL_TAG:
                return QVariant("tag")
            elif col == COL_TYPE:
                return QVariant("type")
            else:
                raise ValueError("Bad id: %s" % col)
        else:
            return QVariant()
                         
    def selectedData(self):
        return self.get(self.view.currentIndex().row())

    def selectedEntries(self):
        return [self.get(e.row()) 
                for e in self.view.selectionModel().selectedRows()]        

    
    def sort(self, col, order):
        if col == COL_CENTROID:
            self.entries.sort(key=lambda e: e.centroid)
        elif col == COL_TAG:
            self.entries.sort(key=lambda e: e.tag)
        elif col == COL_TYPE:
            self.entries.sort(key=lambda e: e.object.__class__ )
        else:
            raise ValueError("Bad id: %s" % col)
        if order == Qt.DescendingOrder:
            self.entries.reverse()
        self.reset()
            
    def delete(self, entriesToDelete):
        selectedIdx = self.view.selectionModel().selectedRows()[0]
        self.entries = [e for e in self.entries if not e in entriesToDelete]
        self.reset()

        self.view.selectRow(selectedIdx.row())

                    
    def add(self, point):
        self.entries.append(Entry(self.tagFile, point))
        self.reset()

        self.view.selectRow(len(self.entries) - 1)

    def getPoints(self):
        return [e.object for e in self.entries
                if isinstance(e.object, tag_util.point)]

    def getPolygons(self):
        return [e.object for e in self.entries
                if isinstance(e.object, tag_util.polygon)]    
