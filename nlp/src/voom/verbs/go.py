from voom import verb_classifier
from voom.agents import Agent
from voom.features import FeatureGroup
from voom.verb_classifier import Signature
import math2d

class DisplacementFeatures(FeatureGroup):
    def __init__(self):
        FeatureGroup.__init__(self,
                                       {"netDisplacement":"The scaled distance traveled by the figure."})
        
    def doCompute(self, drawer, situation):
        out = {}
        figurePath = situation.agent("figure").asPath()
        
        bborigin, (width, height) = math2d.boundingBox(figurePath)

        scale = pow(pow(width, 2) + pow(height, 2), 0.5)

        drawer.drawDistance("netDisplacement", 0, figurePath[0], figurePath[-1])
        out["netDisplacement"] =  math2d.dist(figurePath[0], figurePath[-1])
        return out

class Engine(verb_classifier.Engine):
    def __init__(self):
        verb_classifier.Engine.__init__(self, "go", Signature(figure=Agent),
                                        [DisplacementFeatures()])


        
        
                        
