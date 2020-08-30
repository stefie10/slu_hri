from eventLogic.inference import inference
from eventLogic.model import Model
from eventLogic.spanningInterval import emptySpanningIntervalSet
from voom.event_logic.primitives import IsMoving, IsVisible, IsClose, approach, \
    Inverted, following, MovingTowards
from voom.features import FeatureGroup
import numpy as na

primitives = [IsMoving("figure"), 
              IsMoving("landmark"),
              IsVisible("figure", "landmark"),
              IsClose("figure", "landmark"),
              MovingTowards("figure", "landmark"),
              MovingTowards("landmark", "figure"),
              ]

class AverageOfPrimitives(FeatureGroup):
    
    
    def __init__(self):
        
        names = [p.name for p in primitives]
        fmap = []
        
        for i, p1 in enumerate(primitives):
            fmap.append((p1.name, p1.name))
            for p2 in primitives[i:]:
                if p1 != p2:
                    name = "%s AND %s" % (p1.name, p2.name)
                    names.append(name)
                    fmap.append((name, name))
        FeatureGroup.__init__(self, dict(fmap))
        self.names = names # so the order is right
    
    TRUE_CNT = 0
    TOTAL = 1         
    def doCompute(self, drawer, situation):
        
        countMap = na.zeros((len(self.names), 2))
        

        start = situation.startTime
        end = max(situation.agent("landmark").endTime,
                  situation.agent("figure").endTime) 
        times = list(range(start, end, 1000))
        if len(times) == 0:
            raise ValueError("No times: ", start, end)        
        results = na.zeros((len(times), len(self.names)))
        
        for tdx, t in enumerate(times):
            
            truthValues = [p.compute(situation, t) for p in primitives]
            
            for i, p1 in enumerate(primitives):
                for j, p2 in enumerate(primitives[i:]):
                    if p1 != p2:
                        truthValues.append(truthValues[i] and truthValues[j])
                                                    
            results[tdx] = truthValues             

        means = na.mean(results, axis=0)
        resultMap = {}
        for i, n in enumerate(self.names):
            resultMap[n] = means[i]

        return resultMap 
            
         

def modelForSituation(situation):
    negated = [Inverted(p) for p in primitives]
        
    expressions = primitives + negated
    entries = []
    for p in expressions:
        newEntries = p.modelEntries(situation)
        entries.extend(newEntries)
        
    return Model(entries)
    
class Approach(FeatureGroup):
    def __init__(self):
        FeatureGroup.__init__(self, {"hasApproach":"Whether figure approaches ground.",
                                     "hasFollow":"Whether figure follows landmark",
                                     })
        
    
    def doCompute(self, drawer, situation):
        model = modelForSituation(situation)
        approachResults = inference(model, approach("figure", "landmark")).snappedToMin(0)
        drawer.drawPoint("hasApproach", (0, 0), "has approach initial")
        for t in range(situation.startTime, situation.endTime, 100):
            for interval in approachResults:
                if interval.contains(t):
                    x, y, theta = situation.agent("figure").location(t)
                    drawer.drawPoint("hasApproach", (x, y), "approach")
        
        followResults = inference(model, following("figure", "landmark")).snappedToMin(0)
        drawer.drawPoint("hasFollow", (0, 0), "has follow initial")
        for t in range(situation.startTime, situation.endTime, 100):
            for interval in followResults:
                if interval.contains(t):
                    x, y, theta = situation.agent("figure").location(t)
                    drawer.drawPoint("hasFollow", (x, y), "follow")
        
        
        ret = {"hasApproach": True if approachResults != emptySpanningIntervalSet else False,
                "hasFollow": True if followResults != emptySpanningIntervalSet else False,
                }
        return ret
        
            
            
                                     
