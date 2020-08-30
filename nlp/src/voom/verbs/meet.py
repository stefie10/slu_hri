from voom import verb_classifier
from voom.agents import Agent
from voom.features import FeatureGroup
from voom.verb_classifier import Signature
import math2d


class DisplacementFeatures(FeatureGroup):
    def __init__(self):
        FeatureGroup.__init__(self,
                              {"displacementFromGround":"The difference between the distance of the start of the figure and the centroid of the ground,a and the end of the figure and the centroid of the ground.",
                               "endpointDist":"Distance between ground endpoitn and my endpoint",
                               "startpointDist":"Distance between ground endpoitn and my endpoint",
                               })
    def doCompute(self, drawer, situation):        
        
        figureA = situation.agent("figure")
        landmarkA = situation.agent("landmark")
        
        figure = [(x, y) for x, y, theta in figureA.positions]
        landmark = [(x, y) for x, y, theta in landmarkA.positions]
                
        out = {}
        bborigin, (width, height) = math2d.boundingBox(figure)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        if scale == 0:
            bborigin, (width, height) = math2d.boundingBox(figure + landmark)
            scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        
        pt = landmark[-1]

        dFigureStartToGround = math2d.dist(pt, figure[0])
        dFigureEndToGround = math2d.dist(pt, figure[-1])
        drawer.drawDistance("displacementFromGround", 
                            [pt, figure[0]])

        drawer.drawDistance("displacementFromGround", 
                            [pt, figure[-1]])

        out["endpointDist"] = math2d.dist(figure[-1], landmark[-1])/ scale
        out["startpointDist"] = math2d.dist(figure[0], landmark[0])/ scale

        out["displacementFromGround"] = (dFigureEndToGround - dFigureStartToGround)/scale
        return out


class Engine(verb_classifier.Engine):
    def __init__(self):
        verb_classifier.Engine.__init__(self, "meet", Signature(figure=Agent,
                                                                landmark=Agent),
                                                                
                                      [#follow.AverageDistance(), 
                                       #follow.Visibility(),
                                       #Approach(),
                                       #follow.AverageOfPrimitives(),
                                       DisplacementFeatures(),
                                       #follow.MovingTowards(),
                                       ])

        
        
                        
