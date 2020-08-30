from PyQt4.QtCore import *
from PyQt4.QtGui import *
import mpl_drawer


class InsaneExample(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

    

def makeDrawMethod(name):
    def drawMethod(self, key, time, *args):
        assert isinstance(key, str)
        self.drawMap.setdefault(key, [])
        self.drawMap[key].append({"time":time, "name":name, "args":args})
    return drawMethod

class Drawer:
    def __init__(self):
        self.drawMap = {}
        
    for k, v in mpl_drawer.Drawer.__dict__.iteritems(): #@UndefinedVariable
        if k.startswith("draw"):
            exec("%s = makeDrawMethod(\'%s\')" % (k, k))


class FeatureGroup:
    
    cache = {}
    
    @staticmethod
    def clearCache():
        FeatureGroup.cache = {}
        
    def __init__(self, featureDescs):
        assert isinstance(featureDescs, dict), featureDescs
        self.featureDescs = featureDescs
        self.names = sorted(self.featureDescs.keys())
        self.lastValues = None
    

    def __len__(self):
        return len(self.names)

    def description(self, name):
        return self.featureDescs[name]
    """
    Returns a map of features with values.  Keys are in names. 
    """
    def compute(self, situation):
        memkey = (self.__class__, situation)
        if memkey in self.cache:
            return self.cache[memkey]
        drawer = Drawer()
        try:
            map = self.doCompute(drawer, situation)
        except Exception, e:
            e.args = (self, e.args)
            raise
        if map != None:
            # if you bailed, don't require that you drew everything. 
            for name in self.names:
                assert map.has_key(name), (map, name)
                #assert drawer.drawMap.has_key(name), (self, drawer.drawMap, name, "Did you draw this feature?")
        else:
            map = {}
            for x in self.names():
                map[x] = -1
        drawer.lastValues = map
        self.lastValues = map
        
        result = self.lastValues, drawer 
        #self.cache[memkey] = result
        return result

    """
    The method that clients actually override. 
    """
    def doCompute(self, **args):
        pass



class FeatureCollection:
    def __init__(self, groups):
        self.groups = groups
        self._map = {}
        for group in self.groups:
            for x in group.names:
                self._map[x] = group

        self.names = self._map.keys()
        self.names.sort()

        

    def __len__(self):
        return sum([len(g) for g in self.groups])

    def __getitem__(self, idx):
        return self.names[idx]

        

    def compute(self, **args):
        result, drawMap = self.computeAndVisualize(**args)
        return result

    def computeAndVisualize(self, situation):
        result = {}
        drawMap = {}
        exceptions = []
        for feature in self.groups:
            try:
                vMap, drawer = feature.compute(situation)
                result.update(vMap)
                drawMap.update(drawer.drawMap)
            except InsaneExample, e:
                exceptions.append(e)
        return result, drawMap, exceptions

    @property
    def names(self):
        for feature in self.groups:
            for name in feature.names:
                yield name


    def description(self, name):
        return self._map[name].description(name)
    def visualize(self, name):
        try:
            group = self._map[name]
            return group.visualize(name)
        except KeyError:
            print "self", self
            raise
                          
        
