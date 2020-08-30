from voom import verb_classifier
from voom.agents import Agent
from voom.event_logic.features import AverageOfPrimitives
from voom.verb_classifier import Signature

class Engine(verb_classifier.Engine):
    def __init__(self):
        verb_classifier.Engine.__init__(self, "bring", 
                                        Signature(figure=Agent,
                                                  landmark=Agent),
                                        [#follow.AverageDistance(),
                                         #Approach(),
                                         AverageOfPrimitives(),
                                         ])
        

        

        
