import unittest
import chunker

class ChunkerTestCase(unittest.TestCase):
    def testTrimPunctuation(self):
        self.assertEqual(chunker.trimPunctuation("test."), "test")
        self.assertEqual(chunker.trimPunctuation("test"), "test")
        self.assertEqual(chunker.trimPunctuation(",..,,.test,.,.,"), "test")

        self.assertEqual(chunker.trimPunctuation(",..,,.test. asdfas,.,.,"), "test. asdfas")
        
    def testSplit(self):
        self.assertEqual(chunker.splitIdx("a b"), [("a", 0), ("b", 2)])
        self.assertEqual(chunker.splitIdx("asdf b"), [("asdf", 0), ("b", 5)])
        self.assertEqual(chunker.splitIdx("asdf  b"), [("asdf", 0), ("b", 6)])
        self.assertEqual(chunker.splitIdx("asdf  b "), [("asdf", 0), ("b", 6)])



    def testChunking(self):
        c = chunker.Chunker()
        indxes, tokens, annotations = c.chunk("towards the door")
        nps = [x for x in chunker.getChunks(annotations, "NP")]
        self.assertEqual(" ".join([word for word, tag in nps[0].leaves()]),
                         "the door")


