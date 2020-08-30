from eventLogic import stub_model, allenRelations
from eventLogic.allenRelations import greaterThan, meets, finishes, \
    starts, iStarts, iMeets, equals
from eventLogic.expressions import Or, Not, AndR, Tense, overlaps
from eventLogic.inference import inference
from eventLogic.model import Model, ModelEntry
from eventLogic.spanningInterval import SpanningInterval, Interval, OP, CL, NINF, \
    PINF, SpanningIntervalSet, emptySpanningIntervalSet, allIntervals
from eventLogic.stub_model import Visible, Close, Following
import unittest


class TestCase(unittest.TestCase):
    def testInferenceBase(self):
        
        model = Model([ModelEntry(Visible("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 0, 0, CL),
                                                  Interval(CL, 1, 1, CL),
                                                  CL))]) 
        
        result = inference(model, stub_model.Visible("figure", "landmark"))
        self.assertEqual(result, SpanningIntervalSet([SpanningInterval(CL,
                                                                      Interval(CL, 0, 0, CL),
                                                                      Interval(CL, 1, 1, CL),
                                                                      CL)]))


        result = inference(model, stub_model.Close("figure", "landmark"))
        self.assertEqual(result, emptySpanningIntervalSet)
        
        
        result = inference(model, Not(stub_model.Close("figure", "landmark")))
        self.assertEqual(result, allIntervals)
        
        result = inference(model, overlaps(stub_model.Close("figure", "landmark")))
        self.assertEqual(result, emptySpanningIntervalSet)                


        result = inference(model, Not(overlaps(stub_model.Close("figure", "landmark"))))
        self.assertEqual(result, allIntervals)                

        
        
    def testInferenceOr(self):
        
        model = Model([ModelEntry(Visible("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                       ModelEntry(Close("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 2, 3, CL),
                                                   Interval(CL, 2, 3, CL),
                                                   CL)),
                       ModelEntry(Following("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 1, 3, CL),
                                                   Interval(CL, 1, 3, CL),
                                                   CL))])                                                                                              
                                                  
        result = inference(model, stub_model.Visible("figure", "landmark"))
        self.assertEqual(result, 
                         SpanningIntervalSet([SpanningInterval(True, Interval(True, 1.0, 3.0, True), 
                                                               Interval(True, 1.0, 3.0, True), True)]))
        

        result = inference(model, Or(stub_model.Visible("figure", "landmark"),
                                     stub_model.Following("figure", "landmark")))
        self.assertEqual(result,
                         SpanningIntervalSet([SpanningInterval(True, Interval(True, 1.0, 3.0, True), 
                                           Interval(True, 1.0, 3.0, True), True)]))
        
        result = inference(model, Or(stub_model.Close("figure", "landmark"),
                                     stub_model.Following("figure", "landmark")))
        
        self.assertEqual(result, SpanningIntervalSet([
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(CL, 1.0, 3.0, CL), CL)])) 
        
        
        
    def testInferenceNot(self):
        
        model = Model([ModelEntry(Visible("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                       ModelEntry(Close("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 2, 3, CL),
                                                   Interval(CL, 2, 3, CL),
                                                   CL)),
                       ModelEntry(Following("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 1, 3, CL),
                                                   Interval(CL, 1, 3, CL),
                                                   CL))])                                                                                              
                                                  
                                                  
        result = inference(model, Not(stub_model.Visible("figure", "landmark")))
        
        print "result", result
        
        self.assertEqual(result, SpanningIntervalSet([
             SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, PINF, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, 3.0, PINF, OP), CL),
             SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP),
             SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP)]))                         



    def testInferenceNotEmpty1(self):
        
        model = Model([ModelEntry(Visible("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                       ModelEntry(Visible("figure", "landmark"), 
                                 SpanningInterval(OP, 
                                                  Interval(CL, 1, 3, CL), 
                                                  Interval(CL, 1, 3, CL), 
                                                  OP)),
                       ModelEntry(Visible("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 1, 3, CL),
                                                   Interval(CL, 1, 3, CL),
                                                   OP)),
                       ModelEntry(Visible("figure", "landmark"), 
                                  SpanningInterval(OP,
                                                   Interval(CL, 1, 3, CL),
                                                   Interval(CL, 1, 3, CL),
                                                   CL)),                                                                                                     
                ])
        result = inference(model, stub_model.Visible("figure", "landmark"))
        
        self.assertEqual(result, 
                         SpanningIntervalSet([SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(CL, 1.0, 3.0, CL), CL), 
                          SpanningInterval(OP, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP), 
                          SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP), 
                          SpanningInterval(OP, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, CL), CL)]))
                         
        
        result = inference(model, Not(stub_model.Visible("figure", "landmark")))
        self.assertEqual(result, SpanningIntervalSet([
            SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, 3.0, PINF, OP), CL),
            SpanningInterval(OP, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, PINF, OP), CL),
            SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, 3.0, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, PINF, OP), OP),
            SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, 3.0, PINF, OP), OP),
            SpanningInterval(OP, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, PINF, OP), OP),
            SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, 3.0, PINF, OP), OP)]))                          
            
    def testInferenceNotEmpty(self):
        
        model = Model([ModelEntry(Visible("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL))])

        result = inference(model, stub_model.Visible("figure", "landmark"))
        
        self.assertEqual(result, 
                         SpanningIntervalSet([SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)]))
        
        
        complement = result[0].complement()
        
        self.assertEqual(complement, 
                         SpanningIntervalSet([SpanningInterval(CL, Interval(CL, NINF, PINF, CL), Interval(CL, NINF, 1.0, OP), CL), 
                                                  SpanningInterval(CL, Interval(CL, NINF, PINF, CL), Interval(OP, 3.0, PINF, CL), CL), 
                                                  SpanningInterval(CL, Interval(CL, NINF, 1.0, OP), Interval(CL, NINF, PINF, CL), CL), 
                                                  SpanningInterval(CL, Interval(OP, 3.0, PINF, CL), Interval(CL, NINF, PINF, CL), CL), 
                                                  SpanningInterval(OP, Interval(CL, NINF, PINF, CL), Interval(CL, NINF, PINF, CL), CL), 
                                                  SpanningInterval(CL, Interval(CL, NINF, PINF, CL), Interval(CL, NINF, PINF, CL), OP), 
                                                  SpanningInterval(OP, Interval(CL, NINF, PINF, CL), Interval(CL, NINF, PINF, CL), OP)]))

        result = inference(model, Not(stub_model.Visible("figure", "landmark")))
        self.assertEqual(result, SpanningIntervalSet(complement).condensed())

        
        
#        print "result", result
#        
#        self.assertEqual(result,
#                         [SpanningInterval(CL, Interval(CL, NINF, PINF, CL), 
#                                           Interval(CL, NINF, 1.0, OP), CL), 
#                          SpanningInterval(CL, Interval(CL, NINF, PINF, CL), 
#                                           Interval(OP, 3.0, PINF, CL), CL), 
#                          SpanningInterval(CL, Interval(CL, NINF, 1.0, OP), 
#                                           Interval(CL, NINF, PINF, CL), CL), 
#                          SpanningInterval(CL, Interval(OP, 3.0, PINF, CL), 
#                                           Interval(CL, NINF, PINF, CL), CL),
#                          SpanningInterval(OP, Interval(CL, NINF, PINF, CL), 
#                                           Interval(CL, NINF, PINF, CL), CL), 
#                          SpanningInterval(CL, Interval(CL, NINF, PINF, CL), 
#                                           Interval(CL, NINF, PINF, CL), OP), 
#                          SpanningInterval(OP, Interval(CL, NINF, PINF, CL), 
#                                           Interval(CL, NINF, PINF, CL), OP)])



    def testFinishes(self):
        
        model = Model([ModelEntry(Close("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                                                  ])



        result = inference(model, Tense([finishes],
                                        stub_model.Close("figure", "landmark")))

        self.assertEqual(result,
                         SpanningIntervalSet([SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), CL), 
                          SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), CL)]))
                         

    def testOverlaps(self):
        
        model = Model([ModelEntry(Close("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                                                  ])

        result = inference(model, Not(overlaps(stub_model.Visible("figure", "landmark"))))
        
        self.assertEqual(result, SpanningIntervalSet([
             SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP),
             SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP),
             SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), CL)])) 
        

        result = inference(model, overlaps(stub_model.Close("figure", "landmark")))
        self.assertEqual(result, SpanningIntervalSet([
                    SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(CL, 1.0, PINF, OP), CL)]))
        
        result = inference(model, Not(overlaps(stub_model.Close("figure", "landmark"))))
        
        
        self.assertEqual(result, SpanningIntervalSet([
            SpanningInterval(OP, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, 1.0, CL), OP),
            SpanningInterval(OP, Interval(CL, 3.0, PINF, OP), Interval(OP, 3.0, PINF, OP), OP),
            SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, 1.0, CL), OP),
            SpanningInterval(CL, Interval(OP, 3.0, PINF, OP), Interval(OP, 3.0, PINF, OP), OP),
            SpanningInterval(OP, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, 1.0, OP), CL),
            SpanningInterval(OP, Interval(CL, 3.0, PINF, OP), Interval(OP, 3.0, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, 1.0, OP), CL),
            SpanningInterval(CL, Interval(OP, 3.0, PINF, OP), Interval(OP, 3.0, PINF, OP), CL)])) 
        
    def testTenseAndStarts(self):
        
        model = Model([ModelEntry(Close("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                                                  ])


        result = inference(model, Tense([starts], stub_model.Close("figure", "landmark")))
        self.assertEqual(result, SpanningIntervalSet([
        SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
        SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), CL)]))

        result = inference(model, Tense([iStarts], stub_model.Close("figure", "landmark")))
        self.assertEqual(result, SpanningIntervalSet([
        SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, 3.0, CL), OP),
        SpanningInterval(CL, Interval(CL, 1.0, 3.0, OP), Interval(CL, 1.0, 3.0, OP), CL)]))
        
        result = inference(model, Tense([starts, iStarts], stub_model.Close("figure", "landmark")))
        self.assertEqual(result.condensed(), SpanningIntervalSet([
             SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
             SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(CL, 1.0, PINF, OP), CL)]))      
        
        
    def testInferenceAnd(self):
        model = Model([ModelEntry(Visible("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 1, 3, CL),
                                                   Interval(CL, 1, 3, CL),
                                                   CL)),
                       ModelEntry(Close("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 2, 3, CL),
                                                   Interval(CL, 2, 3, CL),
                                                   CL)),
                       ModelEntry(Following("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 1, 3, CL),
                                                   Interval(CL, 1, 3, CL),
                                                   CL))])                                                                                              
                                                  
        
        result = inference(model, AndR(stub_model.Visible("figure", "landmark"),
                                       [allenRelations.finishes],
                                       stub_model.Close("figure", "landmark")))

        self.assertEqual(result, SpanningIntervalSet([
            SpanningInterval(CL, Interval(CL, 2.0, 3.0, CL), Interval(CL, 2.0, 3.0, CL), CL)]))


        result = inference(model, AndR(stub_model.Close("figure", "landmark"),
                                       [allenRelations.finishes],
                                       stub_model.Visible("figure", "landmark")))

        self.assertEqual(result, SpanningIntervalSet([
            SpanningInterval(CL, Interval(CL, 1.0, 3.0, CL), Interval(CL, 2.0, 3.0, CL), CL)]))


    def testInferenceTense(self):
        model = Model([ModelEntry(Visible("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 1, 3, CL),
                                                   Interval(CL, 1, 3, CL),
                                                   CL)),
                       ModelEntry(Close("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 2, 3, CL),
                                                   Interval(CL, 2, 3, CL),
                                                   CL)),
                       ModelEntry(Following("figure", "landmark"), 
                                  SpanningInterval(CL,
                                                   Interval(CL, 1, 3, CL),
                                                   Interval(CL, 1, 3, CL),
                                                   CL))])
        result = inference(model, Tense([allenRelations.finishes],
                                        stub_model.Visible("figure", "landmark")))
                                        
        self.assertEqual(result, SpanningIntervalSet([SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), 
                                                   Interval(CL, 1.0, 3.0, CL), CL), 
                                  SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), 
                                                   Interval(CL, 1.0, 3.0, CL), CL)]))

        result = inference(model, Tense([allenRelations.overlaps],
                                        stub_model.Visible("figure", "landmark")))
        
        self.assertEqual(result, SpanningIntervalSet([
            SpanningInterval(OP, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(OP, Interval(CL, 1.0, 3.0, OP), Interval(OP, 1.0, PINF, OP), CL),
            SpanningInterval(CL, Interval(OP, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(CL, Interval(OP, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), CL)]))        
        
        result = inference(model, overlaps(stub_model.Visible("figure", "landmark")))
        self.assertEqual(result, SpanningIntervalSet([
             SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(OP, 1.0, PINF, OP), OP),
             SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, PINF, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
             SpanningInterval(CL, Interval(OP, NINF, 3.0, CL), Interval(CL, 1.0, PINF, OP), CL)]))
        
        
    
    def testMeets(self):
        model = Model([ModelEntry(Close("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                                                  ])
        result = inference(model, Tense([iMeets],
                                       stub_model.Close("figure", "landmark")))

        self.assertEqual(result, SpanningIntervalSet([
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), OP),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), OP)]))
        
        result = result.snappedToMin(0)
        self.assertEqual(result, SpanningIntervalSet([
             SpanningInterval(OP, Interval(CL, 0.0, 3.0, OP), Interval(CL, 1.0, 3.0, CL), OP),
             SpanningInterval(CL, Interval(CL, 0.0, 3.0, OP), Interval(CL, 1.0, 3.0, CL), OP)]))
                         

    def testGt(self):    
        model = Model([ModelEntry(Close("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                                                  ])
        result = inference(model, AndR(Not(overlaps(stub_model.Close("figure", "landmark"))),
                                       [equals],
                                       Tense([greaterThan], stub_model.Close("figure", "landmark"))))
        
        self.assertEqual(result, SpanningIntervalSet([
             SpanningInterval(OP, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, 1.0, CL), OP),
             SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, 1.0, CL), OP),
             SpanningInterval(OP, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, 1.0, OP), CL),
             SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(OP, NINF, 1.0, OP), CL)]))


    def testMeetsAndClose(self):    
        model = Model([ModelEntry(Close("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                                                  ])
        result = inference(model, AndR(Not(overlaps(stub_model.Close("figure", "landmark"))),
                                       [equals],
                                       Tense([meets], stub_model.Close("figure", "landmark"))))

        self.assertEqual(result, SpanningIntervalSet([
             SpanningInterval(OP, Interval(CL, 3.0, 3.0, CL), Interval(OP, 3.0, PINF, OP), OP),
             SpanningInterval(OP, Interval(CL, 3.0, 3.0, CL), Interval(OP, 3.0, PINF, OP), CL)]))        



    def testIMeets(self):    
        model = Model([ModelEntry(Close("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                                                  ])
        result = inference(model, Tense([iMeets], stub_model.Close("figure", "landmark")))

        self.assertEqual(result, SpanningIntervalSet([
            SpanningInterval(OP, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), OP),
            SpanningInterval(CL, Interval(OP, NINF, 3.0, OP), Interval(CL, 1.0, 3.0, CL), OP)]))

        result = inference(model, Tense([meets], stub_model.Close("figure", "landmark")))
        self.assertEqual(result, SpanningIntervalSet([
            SpanningInterval(OP, Interval(CL, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), OP),
            SpanningInterval(OP, Interval(CL, 1.0, 3.0, CL), Interval(OP, 1.0, PINF, OP), CL)]))





    def testApproach(self):    
        model = Model([ModelEntry(Close("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 1, 3, CL),
                                                  Interval(CL, 1, 3, CL),
                                                  CL)),
                                                  ])
        result = inference(model, AndR(Not(overlaps(stub_model.Close("figure", "landmark"))),
                                       [equals],
                                       Tense([iMeets], stub_model.Close("figure", "landmark"))))

        self.assertEqual(result, SpanningIntervalSet([
             SpanningInterval(CL, Interval(OP, NINF, 1.0, OP), Interval(CL, 1.0, 1.0, CL), OP),
             SpanningInterval(OP, Interval(OP, NINF, 1.0, OP), Interval(CL, 1.0, 1.0, CL), OP)]))


    def testNoApproach(self):    
        model = Model([ModelEntry(Close("figure", "landmark"), 
                                 SpanningInterval(CL,
                                                  Interval(CL, 0, 3, CL),
                                                  Interval(CL, 0, 3, CL),
                                                  CL)),
                                                  ])
        result = inference(model, AndR(Not(overlaps(stub_model.Close("figure", "landmark"))),
                                       [equals],
                                       Tense([iMeets], stub_model.Close("figure", "landmark"))))

        self.assertEqual(result, SpanningIntervalSet([
             SpanningInterval(CL, Interval(OP, NINF, 0, OP), Interval(CL, 0, 0, CL), OP),
             SpanningInterval(OP, Interval(OP, NINF, 0, OP), Interval(CL, 0, 0, CL), OP)]))
        
        self.assertEqual(result.snappedToMin(0), emptySpanningIntervalSet)
        



        