from voom import verb_classifier
from voom.agents import Agent
from voom.verb_classifier import Signature
from voom.verbs import follow


class Engine(verb_classifier.Engine):
    def __init__(self):
        verb_classifier.Engine.__init__(self, "avoid", 
                                        Signature(figure=Agent,
                                                  landmark=Agent),
                                        [follow.AverageDistance(),
                                         #Approach(),
                                         #AverageOfPrimitives(),                                         
                                         ],
                                         isLiquid=True
                                         )
        

        

        
