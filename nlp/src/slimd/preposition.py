from PyQt4.QtCore import *
from PyQt4.QtGui import *
import features
import orange
import orangeUtils
import orngFSS
import os

def orangeToBoolean(orngValue):
    if orngValue.value == "True":
        return True
    elif orngValue.value == "False":
        return False
    else:
        raise ValueError("Unexpected value for cls " + `orngValue.value`)

def booleanToOrange(bool, var):
    if bool:
        txt = "True"
    else:
        txt = "False"
    return orange.Value(var, txt)



def dataFilesToTable(engine, files):
    first = True
    table = orange.ExampleTable(engine.domain())
    for fname in files:
        try:
            ex = engine.loadFile(fname)
        except InsaneExample:
            continue
        table.append(ex)    
    return table

def makeWidget(classifier, ex):
    if isinstance(classifier, orange.TreeClassifier):
        return makeTreeWidget(classifier, ex)
    elif isinstance(classifier, orngFSS.FilteredClassifier):
        return makeWidget(classifier.classifier, ex)
    elif isinstance(classifier, RejectInsaneExampleClassifier):
        return makeWidget(classifier._classifier, ex)
    else:
        return None
    
def makeTreeWidget(classifier, example):
    treeWidget = QTreeWidget()
    font = QFont(treeWidget.font())
    font.setPointSize(12)
    treeWidget.setFont(font)
    treeWidget.header().setStretchLastSection(False)
    treeWidget.header().setResizeMode(QHeaderView.ResizeToContents)

    sizePolicy = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
    treeWidget.setSizePolicy(sizePolicy)
    treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
    dataMap = {}
    def menu(point):
        idx = treeWidget.indexAt(point)
        data = treeWidget.model().data(idx)
        item = treeWidget.itemAt(point)
        if dataMap.has_key(item):
            node = dataMap[item]
            menu = QMenu(treeWidget)
            for ex in node.examples:
                action = menu.addAction(str(ex['filename']))
            menu.exec_(treeWidget.mapToGlobal(point))

    treeWidget.connect(treeWidget, SIGNAL("customContextMenuRequested(QPoint)"),
                       menu)

    makeTree(classifier.tree, treeWidget, example, dataMap)
    return treeWidget
def makeTree(classifierNode, guiNode, example, dataMap):
    if classifierNode.branchSelector:
        
        nodeIdx = classifierNode.branchSelector(example)
        nodeName = classifierNode.branchSelector.classVar.name
        for i, (node, desc) in enumerate(zip(classifierNode.branches, 
                                             classifierNode.branchDescriptions)):
            nodeValue = example[nodeName]
            if nodeName == "class":
                continue 
            if nodeValue.isDK():
                nodeText = "%s %s (value: ??)" % (nodeName, desc)
            else:
                nodeText = "%s %s (value: %.3f)" % (nodeName, desc, nodeValue)
            item = QTreeWidgetItem(guiNode)
            item.setText(0, nodeText)
            makeTree(node, item, example, dataMap)
            if not nodeIdx.isDK() and i == nodeIdx:
                item.setExpanded(True)
                item.setForeground(0, QBrush(Qt.red))
                if item.childCount() == 1:
                    item.child(0).setForeground(0, QBrush(Qt.red))

                    
    else:
        majorClass = classifierNode.nodeClassifier.defaultValue

        nodeText = "Class: %s" % (majorClass)
        item = QTreeWidgetItem(guiNode)
        dataMap[item] = classifierNode
        item.setText(0, nodeText)

def readDirectory(directory):
    for x in os.listdir(directory):
        if x[0] != '.':
            yield "%s/%s" % (directory, x)

def makeDomain(names):
    attributes = [orange.FloatVariable(n) for n in names] 
    domain = orange.Domain(attributes,
                           orange.EnumVariable("class", 
                                               values=["True", "False"]))
    domain.addmeta(orange.newmetaid(), orange.FloatVariable("weight"))

    domain.addmeta(orange.newmetaid(), 
                   orange.EnumVariable("isInsane",
                                       values=["True","False"]))


    domain.addmeta(orange.newmetaid(), orange.StringVariable("filename"))
    domain.addmeta(orange.newmetaid(), orange.StringVariable("sourceEngineName"))
    domain.addmeta(orange.newmetaid(), orange.StringVariable("engineName"))
    domain.addmeta(orange.newmetaid(), orange.StringVariable("landmarkName"))
    domain.addmeta(orange.newmetaid(), orange.PythonVariable("geometry"))
    domain.addmeta(orange.newmetaid(), orange.PythonVariable("track"))
    domain.addmeta(orange.newmetaid(), orange.PythonVariable("drawMap"))
    domain.addmeta(orange.newmetaid(), orange.PythonVariable("description"))
    domain.addmeta(orange.newmetaid(), orange.PythonVariable("farAway"))

    return domain

class Preposition:
    def __init__(self, name, signature, flist, masterList=None):
        self._flist = features.FeatureCollection(flist)
        self._name  = name
        self._signatureMap = {}
        self._signatureKeys = []
        self._signatureCardinality = {}
        for key, value, cardinality in signature:
            self._signatureMap[key] = value
            self._signatureCardinality[key] = cardinality
            self._signatureKeys.append(key)
        if masterList != None:
            self.setFeatureList(masterList)
        else:
            self.setFeatureList(self._flist.names())
        self._data = None
        self._classifier = None

    def setFeatureList(self, lst):
        self.masterList = list(lst)
        self._domain = makeDomain(self.masterList)



    def cardinality(self, key):
        return self._signatureCardinality[key]
    @property
    def data(self):
        if self._data == None:
            self._data = self.makeData()
        return self._data

    
    def loadClassifier(self):
        self._classifier = self.makeLearner()(self.data)
    def get_classifier(self):
        if self._classifier == None:
            self.loadClassifier()
        return self._classifier
    def set_classifier(self, classifier):
        self._classifier = classifier
    classifier = property(get_classifier, set_classifier)

    def type(self, key):
        return self._signatureMap[key]
    def signature(self):
        return self._signatureKeys
    def domain(self):
        return self._domain
    def flist(self):
        return self._flist

    def name(self):
        return self._name

    def makeData(self):
        return dataFilesToTable(self, self.dataFiles())
    def makeLearner(self):
        raise NotImplementedError()
    def dataFiles(self):
        raise NotImplementedError()

    #@memoize.memoize
    def makeExample(self, expectInsane=False, **iArgs):
        #args = filterQgis(iArgs)
        args = iArgs
        try:
            features, drawMap = self._flist.computeAndVisualize(**args)

            features['isInsane'] = "False"
            lst = []
            for attr in self._domain:
                if attr.name == "class":
                    lst.append("")
                else:
                    lst.append(features[attr.name])
            ex = orange.Example(self._domain, lst)                    
            ex['drawMap'] = drawMap

        except InsaneExample, e:
            e.exArgs = iArgs
            if expectInsane:
                ex = orange.Example(self._domain)
                ex['isInsane'] = "True"
            else:
                raise
        ex["geometry"] = args
        return ex
    def isValid(self, **args):
        value, probabilities, ex = self.classify(**args)
        return orangeToBoolean(value)



    def classify(self, raiseOnInsane=False, **args):
        """
        Takes the geometry of the figure and landmark, in slimd/python
        terms.  Polygons and linestrings are lists of points, and points
        are tuples.
        """
        if self.classifier == None:
            raise NotImplementedError()

        try:
            ex = self.makeExample(**args)
        except InsaneExample:
            if raiseOnInsane:
                raise
            else:
                return booleanToOrange(False, self.domain().classVar), None, None
        cls, probabilities = self.classifier(ex, orange.GetBoth)
        return cls, probabilities, ex

    def visualize(self, **args):
        try:
            ex = self.makeExample(**args)
            return makeWidget(self.classifier, ex)
        except InsaneExample:
            return QLabel("Insane example.")
            
class InsaneExample(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
    
class RejectInsaneExampleClassifier(orangeUtils.PythonClassifier):
    def __init__(self, *realClassifier):
        orangeUtils.PythonClassifier.__init__(self)
        if len(realClassifier) == 0:
            # calling from pickle mode.
            pass
        elif len(realClassifier) == 1:
            self._classifier = realClassifier[0]
        else:
            raise ValueError("Must pass exactly one argument")
    def classify(self, ex):
        if ex['isInsane'] == "True":
            return "False"
        else:
            return self._classifier(ex)
        
class SaneExampleFilter(orange.Filter):
    def __init__(self):
        orange.Filter.__init__(self)
    def __call__(self, ex):
        if ex['isInsane'] == "True":
            return False
        else:
            return True
class RejectInsaneExampleLearner(orange.Learner):
    def __init__(self, realLearner):
        orange.Learner.__init__(self)
        self._learner = realLearner
    def __call__(self, examples, weightID=0):
        filteredExamples = examples.filter(SaneExampleFilter())
        classifier = self._learner(filteredExamples)
        return  RejectInsaneExampleClassifier(classifier)
    
