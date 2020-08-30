from pyTklib import sfe_f_path_l_polygon_names, \
     sfe_extract_f_path_l_polygon
import numpy as na
import math2d
import orange
import math

class CEngine:
    """
    Call the c implementation of the features, not the python.  This
    is a wrapper around the python features.
    """
    def __init__(self, engine):
        self.engine = engine


        self.name = engine.name
        try:
            self.featureNames = [x.split("_")[1]
                                 for x in sfe_f_path_l_polygon_names()]
        except:
            print "x", x
            raise
        self.featureNameToIdx = dict((name, i)
                                     for i, name in enumerate(self.featureNames))
    def domain(self):
        return self.engine.domain()
    def makeExample(self, landmark, figure, **args):
        features = self.compute(landmark, figure)
        features['isInsane'] = "False"
        features['class'] = ""
        flist = [features[attr.name] for attr in self.engine.domain()]
        ex = orange.Example(self.engine.domain(), flist)
        ex["geometry"] = args
        return ex
        
    def compute(self, landmark, figure):
        out = {}
        figure_xy = na.transpose(figure)
        figure_xyth = math2d.xy_to_xyth(figure_xy)
        ground_xy = na.transpose(landmark)

        fvec = sfe_extract_f_path_l_polygon(figure_xyth,
                                       ground_xy, normalize=True)

        for featureName in self.engine.masterList:
            featureIdx = self.featureNameToIdx.get(featureName)
            if featureIdx != None:
                featureValue = fvec[featureIdx]
                if math.isnan(featureValue):
                    featureValue = -1
                    
                out[featureName] = featureValue
        return out
            
