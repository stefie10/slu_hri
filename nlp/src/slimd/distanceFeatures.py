import math2d
import features
class DistanceFeatures(features.FeatureGroup):
    def __init__(self):
        features.FeatureGroup.__init__(self, 
                                       {"averageDistanceToGround":"The average distance between the figure and the ground.",
                                        "minimumDistanceToGround":"The minimum distance between the figure and the ground."})

    def doCompute(self, drawer, ground, figure, **args):
        steps = 100
        fPoints = list(math2d.stepAlongLine(figure, math2d.length(figure)/100))
        
        gPoints = [math2d.closestPointOnPolygon(ground, p) 
                     for p in fPoints]
        distances = [math2d.squaredist(f1, g1) 
                     for f1, g1 in zip(fPoints,gPoints)]
        
        i, minDist = math2d.argMin(distances)
        bborigin, (width, height) = math2d.boundingBox(ground + figure)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        featureMap = {}
        drawer.distanceFeature(self, featureMap, 
                                 "minimumDistanceToGround", 
                                 "Figure",
                                 "Ground",
                                 fPoints[i], gPoints[i], 
                                 scale)
        
        for f1, g1 in zip(fPoints, gPoints):
            self.drawSegment("averageDistanceToGround", f1, g1)
        featureMap["averageDistanceToGround"] = math2d.mean(distances)/scale

                                       
        return featureMap
