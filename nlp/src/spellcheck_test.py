import unittest
from spellcheck import spellcheck



class TestCase(unittest.TestCase):
    def test_spellcheck(self):

        test = "He walked down the street."
        result = spellcheck(test)
        self.assertEqual("He walked down the street ." , result)


        test = "The woman exited the kitchen and is circumambulating the living room, beside the couch."
        result = spellcheck(test)

        self.assertEqual(result,
                         "The woman exited the kitchen and is perambulating the living room , beside the couch .")



        test = "From where he's seated at the dining room table---near the kitchen door---he enters the kitchen and heads toward the sink."
        result = spellcheck(test)
        self.assertEqual(result, "From where he s seated at the dining room table --- near the kitchen door --- he enters the kitchen and heads toward the sink .")
