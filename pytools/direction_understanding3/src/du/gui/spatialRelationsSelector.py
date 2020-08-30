from PyQt4.QtCore import *
from PyQt4.QtGui import *
import spatialRelationsSelector_ui

from qt_utils import Counter
counter = Counter()

COL_SR_NAME = counter.pp()

class SpatialRelationsModel(QAbstractTableModel):
    def __init__(self, view, m4du):
        QAbstractTableModel.__init__(self)
        self.m4du = m4du
        self.engineMap = self.m4du.sr_class.engineMap
        self.keys = sorted(self.engineMap.keys())

        self.view = view
        self.view.setModel(self)
        self.view.selectAll()
        
    def selectedEngineMap(self):
        engineMap = dict([(key, None) for key in self.keys])
        for idx in self.view.selectedIndexes():
            key = self.keys[idx.row()]
            engineMap[key] = self.engineMap[key]
        return engineMap
            
    def columnCount(self, parent=None):
        return counter.cnt

    def rowCount(self, parent=None):
        return len(self.engineMap)

    def get(self, viewIdx):
        return self.engineMap[self.keys[viewIdx]]

    
    def data(self, idx, role=Qt.DisplayRole):
        col = idx.column()

        e = self.get(idx.row())

        if role != Qt.DisplayRole:
            return QVariant()            
        if col == COL_SR_NAME:
            return QVariant(e.name())
        else:
            raise ValueError("Bad id: %s" % col)


    
class MainWindow(QMainWindow, spatialRelationsSelector_ui.Ui_MainWindow):
    def __init__(self, m4du):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.m4du = m4du
        self.model = SpatialRelationsModel(self.spatialRelationsTable,
                                           m4du)
        self.connect(self.spatialRelationsTable.selectionModel(),
                     SIGNAL("selectionChanged ( QItemSelection, QItemSelection )"),
                     self.selectSpatialRelations)
    def selectSpatialRelations(self):
        engineMap = self.model.selectedEngineMap()
        self.m4du.sr_class.set_engine_map(engineMap)
