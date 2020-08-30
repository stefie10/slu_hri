import unittest
from corpus_rrg_openended import Corpus, Annotation

from environ_vars import TKLIB_HOME

class TestCase(unittest.TestCase):
    def testOpen(self):
        corpus = Corpus("%s/data/verbs/corpus-11-2009.ods" % TKLIB_HOME)

        self.assertEqual(len(corpus.questionTypes), 2)

        commands = corpus.commandsForType("Guiding people")
        self.assertEqual(len(commands), 60)


        annotations = corpus.loadAnnotations("%s/data/verbs/Guiding people.stefie10.txt" % TKLIB_HOME)
        print annotations

    def testSchemeParser(self):
        self.assertEqual(Annotation.parse("x"), "x")
        self.assertEqual(Annotation.parse("(x)"), ('x',))
        self.assertEqual(Annotation.parse("(SDC (V Go get) (L everyone))"), 
                         ("SDC", ("V", "Go get"), ("L", "everyone")))
        

        
        
