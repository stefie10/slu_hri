from voom import verb_classifier
from voom.agents import Agent
from voom.features import FeatureGroup
from voom.verb_classifier import Signature, InsaneExample
import math2d

class PathLength(FeatureGroup):
    
    def __init__(self):
        FeatureGroup.__init__(self, {"pathLength":"Ratio of the length of the path compared to the length of the shortest path between the two points."})

    def doCompute(self, drawer, situation):
        figurePath = situation.agent("figure").asPath()

        if len(figurePath) < 2:
            raise InsaneExample("Figure too short: " + `figurePath`)
        
        path = situation.shortestPath(figurePath[0], figurePath[-1])
        
        drawer.drawPoint("pathLength", path[0], "start")
        for p1, p2 in zip(path, path[1:]):
            drawer.drawDistance("pathLength", p1, p2)
            
        return {"pathLength": math2d.length(path) / math2d.length(figurePath)}
        
        

class PathSmoothness(FeatureGroup):
    def __init__(self):
        FeatureGroup.__init__(self, {"stdErrorOfRegression":"The scaled standard error of a regression line."})
        

    def doCompute(self, drawer, situation):

        figurePath = situation.agent("figure").asPath()
        if len(figurePath) == 0:
            raise InsaneExample("Figure was empty: " + `figurePath`)
        else:
            slope, intercept, r_value, p_value, std_err = math2d.regression(figurePath)
            startx = figurePath[0][0]
            endx = figurePath[-1][0]
            starty = startx * slope + intercept
            endy = endx * slope + intercept
            drawer.drawDistance("stdErrorOfRegression", (startx, starty), (endx, endy))
            return {"stdErrorOfRegression":std_err/math2d.length(figurePath)}
        
            
            
                                     


class Engine(verb_classifier.Engine):
    def __init__(self):
        verb_classifier.Engine.__init__(self, "wander", Signature(figure=Agent),
                                        [PathSmoothness(), PathLength()]
                                        )


        
        
                        
