from voom.agents import Agent
import unittest

class TestCase(unittest.TestCase):
    
    def testLocation(self):
        agent = Agent("figure", [(0, (0, 0, 0)),
                                 (1000, (1, 1, 0)),
                                 ])

        self.assertEqual(agent.location(0), (0, 0, 0))
        self.assertEqual(agent.location(0.5), (0.00050000000000000001, 0.00050000000000000001, 0.0))

        


    def testDerivative(self):
        agent = Agent("figure", [(0, (0, 0, 0)),
                                 (1000, (1, 1, 0)),
                                 ])

        self.assertEqual(agent.derivative(0), (0.5, 0.5, 0))
        self.assertEqual(agent.location(0.5), (0.0005, 0.0005, 0.0))
        
        self.assertEqual(agent.location(500), (0.5, 0.5, 0.0))
        self.assertEqual(agent.derivative(500), (1, 1, 0.0))
        
        self.assertEqual(agent.derivative(10000), (0, 0, 0.0))
        