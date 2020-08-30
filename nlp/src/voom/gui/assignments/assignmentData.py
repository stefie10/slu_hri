from routeDirectionCorpusReader import Annotation
from voom import agents
from voom.agents import Situation, ControlledAgent
from voom.gui import turtle
import json



class Assignment:
    def __init__(self, entries, tagFile, skeleton):
        self.entries = entries
        
        for i, e in enumerate(self.entries):
            e.id = i
        self.tagFile = tagFile
        self.skeleton = skeleton
        
        
    def entryForId(self, id):
        return self.entries[id]
    
    def entriesForVerb(self, verb):
        return [e for e in self.entries if e.verb == verb]
        
        
    def asPrimitives(self):
        return {"entries": [e.asPrimitives() for e in self.entries]}
    
    @staticmethod
    def fromPrimitives(primitives, tagFile, skeleton):
        if "entries" in primitives:
            entries = primitives["entries"]
        else:
            entries = [primitives]
        
        return Assignment([VerbAssignmentEntry.fromPrimitives(e,
                                                              tagFile, skeleton)
                           for e in entries], tagFile, skeleton)


        
    def save(self, fname):
        json.dump(self.asPrimitives(), open(fname, "w"), indent=2)
        
    @staticmethod
    def load(fname, tagFile, skeleton):
        a = Assignment.fromPrimitives(json.load(open(fname, "r")),
                                         tagFile, skeleton)
        a.fname = fname
        return a
    

class VerbAssignmentEntry:
    def __init__(self, verb, command, tagFile, skeleton, situation=None, controllers=None, axisLimits=None, sdcMap={}):
        self.verb = verb
        self.command = command
        self.situation = situation
        self.tagFile = tagFile
        self.skeleton = skeleton
        
        self._sdcs = sdcMap
    
        if axisLimits == None:
            self.axisLimits = [0, tagFile.map.x_size, 0, tagFile.map.y_size]
        else:
            self.axisLimits = axisLimits 
        
        if self.situation == None:
            print "verb", self.verb
            self.situation = agents.situationForVerb(self.verb, self.tagFile, self.skeleton)


        if controllers == None:
            self.controllers = []
            for a in self.situation.agents:
                controller = agents.ControlledAgent(tagFile, skeleton, a, turtle.SplineTurtle)
                self.controllers.append(controller)
                if a.name == "figure":
                    controller.setTurtleClass(turtle.KeyboardTurtle)
        else:
            self.controllers = controllers
            
        for c in self.controllers:
            assert c.agent == self.situation.agent(c.agent.name)
        assert len(self.controllers) == len(self.situation.agents)
    
    def sdcs(self, tag):
        if not tag in self._sdcs:
            self._sdcs[tag] = []
        return self._sdcs[tag]

    
    def setSdcs(self, tag, sdcs):
        for sdc in sdcs:
            assert sdc.entireText == self.command
    
    def setAxisLimits(self, limits):
        assert len(limits) == 4
        self.axisLimits = limits
    def asPrimitives(self):
        return {"verb":self.verb, "command":self.command, 
                "situation":self.situation.asPrimitives(),
                "axisLimits":self.axisLimits,
                "controllers": [c.asPrimitives() for c in self.controllers],
                "sdcMap":dict([(key, [v.asPrimitives() for v in value])
                               for key, value in self._sdcs.iteritems()]),
                }
    
    @staticmethod
    def fromPrimitives(p, tagFile, skeleton):
        situation = Situation.fromPrimitives(p["situation"], tagFile,skeleton)
        if 'sdcMap' in p:
            sdcMap = dict([(key, [Annotation.fromPrimitives(v) for v in value] )
                           for key, value in p["sdcMap"].iteritems()])
        else:
            sdcMap = {}
                
        return VerbAssignmentEntry(p["verb"], p["command"], tagFile, skeleton,
                                   situation,
                                   [ControlledAgent.fromPrimitives(tagFile, skeleton, situation, c) for c in p["controllers"]],
                                   axisLimits=p["axisLimits"],
                                   sdcMap=sdcMap)


    def save(self, fname):
        json.dump(self.asPrimitives(), open(fname, "w"), indent=2)
        
    @staticmethod
    def load(fname, tagFile, skeleton):
        return VerbAssignmentEntry.fromPrimitives(json.load(open(fname, "r")),
                                                  tagFile, skeleton)
    
