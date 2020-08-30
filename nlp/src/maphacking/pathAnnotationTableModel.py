import glob
from os.path import basename
from qt_utils import convertVariant
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from slimd import preposition
COL_CLASSIFIER = 0
COL_LANDMARK = 1
COL_CLASS = 2
COL_SCORE = 3
COL_ANNOTATED_CLASS = 4


class PathAnnotation:
    def __init__(self, fname, groundName, engineMap):
        self.fname = fname
        self.engineMap = engineMap
        self.groundName = groundName
        self.properties, self.layerMap = preposition.loadInstance(self.fname, engineMap)
        
        self.engine = self.engineMap[self.properties["preposition"]]
        
        groundLayer, self.ground = self.layerMap["ground"]
        figureLayer, self.figure = self.layerMap["figure"]

        self.geometry = {"ground":self.ground,
                         "figure":self.figure}


        self.classified = False

    def doClassify(self):
        if len(self.figure) > 1 and self.figure != [(0, 0), (0, 0)]:
            self._cls, self._dist, self._ex = self.engine.classify(**self.geometry)
            self._score = self.dist[self.cls]
        else:
            self._cls = None
            self._score = None
            self._dist = None
            self._ex = None
        self.classified = True

    @property
    def cls(self):
        if not self.classified:
            self.doClassify()
        return self._cls

    @property
    def score(self):
        if not self.classified:
            self.doClassify()
        return self._score
            

    def load(self):
        self.properties, self.layerMap = preposition.loadInstance(self.fname, self.engineMap)
    def ensureLoaded(self):
        if self.layerMap != None:
            self.load()
            
    def unload(self):
        for key, layer in self.layerMap.iteritems():
            del layer
        self.layerMap = None

    @property
    def groundLayer(self):
        self.ensureLoaded()
        return self.layerMap["ground"][0]
    
    @property
    def figureLayer(self):
        self.ensureLoaded()
        return self.layerMap["figure"][0]

                                                           
def loadAnnotations(dirName, engineMap, maxExamples = None):
    tagLayer = layers.openLayer(dirName + "/tags", "tags", "ogr")
    tagFeatures = [layers.getGeometry(f.geometry()) for f in layers.features(tagLayer)]
    tagNames = [convertVariant(layers.attribute(tagLayer, f, "name")) for f in layers.features(tagLayer)]
    annotations = []
    for i, dir in enumerate(sorted(glob.glob("%s/landmark.*.ex.*" % dirName))):
        print "dir", dir

        landmark, landmarkId, ex, exId = basename(dir).split(".")
        print "landmark", landmarkId
        landmarkId = int(landmarkId)
        annotations.append(PathAnnotation(dir, tagNames[landmarkId], engineMap))
        if not(maxExamples is None) and i > maxExamples:
            break;

    return tagLayer, annotations
        
    
    


class Model(QAbstractTableModel):
    def __init__(self, view, dirName, engineMap):
        QAbstractTableModel.__init__(self)
        self.view = view
        tagLayer, self._data = loadAnnotations(dirName, engineMap)
        self.view.setModel(self)

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
            return QVariant(dc.groundName)
        elif col == COL_CLASS:
            return QVariant(str(dc.cls))
        elif col == COL_SCORE:
            return QVariant(dc.score)
        else:
            raise ValueError("Bad id: %s" % col)
        
        
