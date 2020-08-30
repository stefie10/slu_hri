import features
import awayFrom
import preposition
import math2d
import orngBayes
import argTypes
import numpy as na

class DistToLandmarkFeatures(features.FeatureGroup):
    def __init__(self,):
        features.FeatureGroup.__init__(self, 
                                       {
                "minimumDistanceToLandmark":"The minimum distance between figure and landmark.",
                "numInteriorPoints":"Whether any points are inside the landmark."
                
                })
    def doCompute(self, drawer, landmark, figure, **args):
        figureSteps = list(math2d.stepAlongLine(figure, math2d.length(figure)/100.0))
        points = [math2d.closestPointOnPolygon(landmark, p) for p in figureSteps]
        interiorPoints = math2d.interiorPoints(landmark, figureSteps)
        landmarkCentroid = math2d.centroid(landmark)
        distances = [math2d.squaredist(p, (0, 0)) for p in points]
        bborigin, (width, height) = math2d.boundingBox(na.append(landmark,
                                                                 figure,
                                                                 0))
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        out = {}
        i, dist = math2d.argMin(distances)
        drawer.distanceFeature(out,
                               "minimumDistanceToLandmark",
                               "Closest point on landmark",
                               "Figure End",
                               figureSteps[i], points[i], scale)


        for p in interiorPoints:
            drawer.drawPoint("numInteriorPoints", p)
        if len(interiorPoints) == 0:
            drawer.drawText("numInteriorPoints", landmarkCentroid, "No interior points.")
            #if out["numInteriorPoints"] > 0:
            #out["numInteriorPoints"] = 1

        out["numInteriorPoints"] = len(interiorPoints)
        if math2d.isInteriorPoint(landmark, figureSteps[i]):
            out["minimumDistanceToLandmark"] = 0
        if math2d.isInteriorPoint(landmark, figure[-1]):
            out["distFigureEndToLandmark"] = 0

            
        differences = [d1 - d2 for d1, d2 in zip(distances, distances[1:])]
        differences = [d/d if d != 0 else 0 for d in differences]
        if len(differences) == 0:
            out["averageDistanceDifference"]= 0
        else:
            out["averageDistanceDifference"]= math2d.mean(differences)
        for p1, p2 in zip(points, points[1:]):
            drawer.drawLine("averageDistanceDifference", [p1, p2])


        return out

        
        
class BoundingBoxFeatures(features.FeatureGroup):
    """
    These features correspond to whether various parts of the figure
    intersect the bounding box of the landmark.x
    """
    def __init__(self):
        features.FeatureGroup.__init__(self, 
                                       {
                "endPointsInLandmarkBoundingBox":"Is the endpoint of the landmark inside the figure's bounding box?",
                "startPointsInLandmarkBoundingBox":"Is the starting point of the landmark inside the figure's bounding box?",

                },
                                       )
    def doCompute(self, drawer, landmark, figure, **args):
        (lowerLeft, lowerRight), (width, height) = math2d.boundingBox(landmark)
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)

        scaleFactor = scale * 0.1
        

        polygon = math2d.boxToPolygon((lowerLeft - scaleFactor, lowerRight - scaleFactor),
                                      (width + 2*scaleFactor, height + 2*scaleFactor))

        
        out = {}
        figureSteps = list(math2d.stepAlongLine(figure, math2d.length(figure)/100.0))


        out["endPointsInLandmarkBoundingBox"] = 0
        for p in figureSteps[90:]:
            if math2d.isInteriorPoint(polygon, p):
                out["endPointsInLandmarkBoundingBox"] += 1
                drawer.drawPoint("endPointsInLandmarkBoundingBox", p)
        drawer.drawLine("endPointsInLandmarkBoundingBox", 
                        math2d.polygonToLine(polygon))


        out["startPointsInLandmarkBoundingBox"] = 0
        for p in figureSteps[:10]:
            if math2d.isInteriorPoint(polygon, p):
                out["startPointsInLandmarkBoundingBox"] += 1
                drawer.drawPoint("startPointsInLandmarkBoundingBox", p)
        drawer.drawLine("startPointsInLandmarkBoundingBox", 
                        math2d.polygonToLine(polygon))

        return out


class EndPointFeatures(features.FeatureGroup):
    def __init__(self):
        features.FeatureGroup.__init__(self, 
                                       {
                "distFigureEndToLandmarkCentroid": 
                "Distance of the end point to the landmark.",
                "distFigureEndToLandmark":"The distance from the end point of the figure to the landmark.",
                "distFigureStartToLandmark":"The distance from the start point of the figure to the landmark.",                                           

                                        })
        
    def doCompute(self, drawer, landmark, figure, **args):
        out = {}
        bborigin, (width, height) = math2d.boundingBox(na.append(landmark,
                                                                 figure,
                                                                 0))
        scale = pow(pow(width, 2) + pow(height, 2), 0.5)
        landmarkCentroid = math2d.centroid(landmark)
        drawer.distanceFeature(out,
                               "distFigureEndToLandmarkCentroid",
                               "Landmark center of mass",
                               "Figure",
                               landmarkCentroid, figure[-1], scale)

        drawer.distanceFeature(out,
                               "distFigureStartToLandmarkCentroid",
                               "Landmark center of mass",
                               "Figure",
                               landmarkCentroid, figure[0], scale)


        if math2d.isInteriorPoint(landmark, figure[0]):
            drawer.distanceFeature(out,
                                   "distFigureStartToLandmark",
                                   "Closest point on landmark",
                                   "Figure Start",
                                   figure[0], figure[0], scale)
        else:
            cp = math2d.closestPointOnPolygon(landmark, 
                                              figure[0])
                    
            drawer.distanceFeature(out,
                                   "distFigureStartToLandmark",
                                   "Closest point on landmark",
                                   "Figure Start",
                                   figure[0], cp, scale)            
        

        if math2d.isInteriorPoint(landmark, figure[-1]):
            drawer.distanceFeature(out,
                                   "distFigureEndToLandmark",
                                   "Closest point on landmark",
                                   "Figure End",
                                   figure[-1], figure[-1], scale)
        else:
            cp = math2d.closestPointOnPolygon(landmark, 
                                              figure[-1])
            drawer.distanceFeature(out,
                                   "distFigureEndToLandmark",
                                   "Closest point on landmark",
                                   "Figure End",
                                   cp, figure[-1], scale)




        return out




class To(preposition.Preposition):
    def __init__(self):
        preposition.Preposition.__init__(self, "to", 
                                         [("landmark",argTypes.Polygon, 1),
                                          ("figure",argTypes.LineString, 1)],
                                         [EndPointFeatures(),
                                          DistToLandmarkFeatures(),
                                          BoundingBoxFeatures(),
                                          awayFrom.DisplacementFeatures()
                                          ],
                                         ["distFigureEndToLandmark",
#                                          "distFigureEndToLandmarkCentroid",
 #                                         "endPointsInLandmarkBoundingBox",
#                                          "startPointsInLandmarkBoundingBox",
#                                          "minimumDistanceToLandmark",
#                                          "numInteriorPoints",
                                          "displacementFromLandmark",
                                          ])
        
        

    def makeLearner(self):
        return orngBayes.BayesLearner()
        
    
