from voom import verb_classifier
from voom.agents import Agent
from voom.verb_classifier import Signature
from voom.verbs.follow import AverageDistance


class Engine(verb_classifier.Engine):
    def __init__(self):
        verb_classifier.Engine.__init__(self, "check", 
                                        Signature(figure=Agent,
                                                  landmark=Agent),
                                        [AverageDistance()])
        

        

        
