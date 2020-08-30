from nltk_contrib.wordnet import synset
from nltk_contrib.wordnet.browse import synsets
from physical_objects import pos_tag, get_wn_objects, get_wn_object_lemmas, \
    get_ancestors, is_person
import unittest

class TestCase(unittest.TestCase):
    def testPosTag(self):
        self.assertEqual(pos_tag("trees"), "NNS")

    def test_get_ancestors(self):
        self.assertEqual(len(get_ancestors(synset("cat.n.01"))), 
                         13)

    def dest_get_wn_objects(self):
        wn_objs = get_wn_objects()
        print len(wn_objs)
        self.assertEqual(len(wn_objs), 29581)

    def dest_get_wn_object_lemmas(self):
        lemmas = get_wn_object_lemmas()
        self.assertEqual(len(lemmas), 47049)
        self.assertEqual(lemmas[0].name, "person")

        
    def test_is_person(self):
        self.assertEqual(is_person(synsets("cat")[0].lemmas[0]), False)
        self.assertEqual(is_person(synsets("man")[0].lemmas[0]), True)
        self.assertEqual(is_person(synsets("girl")[0].lemmas[0]), True)
        self.assertEqual(is_person(synsets("wife")[0].lemmas[0]), True)
        
