import unittest
import chunker
from chunker import IndexedTokenizer
from nltk.tokenize import PunktWordTokenizer, TreebankWordTokenizer

class AnnotationTestCase(unittest.TestCase):
    def testPunktTokenizer(self):
        tokenizer = IndexedTokenizer(PunktWordTokenizer())
        string = " Facing the long wall in front of you, your destination will be the first door to your left (36-880)."
        indexes, tokens = tokenizer.tokenize(string)
        self.assertEqual(tokens,
                         ['Facing', 'the', 'long', 'wall', 'in', 'front', 'of', 'you', ',', 'your', 'destination', 'will', 'be', 'the', 'first', 'door', 'to', 'your', 'left', '(', '36-880', ')', '.'])

        for i, token in enumerate(tokens):
            self.assertEqual(string[indexes[i]:indexes[i] + len(token)], token)

        


    def testPunktTokenizerContraction(self):
        tokenizer = IndexedTokenizer(PunktWordTokenizer())
        string = " You'll see a large white question mark."
        indexes, tokens = tokenizer.tokenize(string)
        self.assertEqual(tokens,
                         ['You', "'ll", 'see', 'a', 'large', 'white', 'question', 'mark', '.'])

        for i, token in enumerate(tokens):
            self.assertEqual(string[indexes[i]:indexes[i] + len(token)], token)

        

    def testPunktTokenizerNiceView(self):
        tokenizer = IndexedTokenizer(PunktWordTokenizer())
        string = "you should have  a    nice   view ."
        indexes, tokens = tokenizer.tokenize(string)
        self.assertEqual(tokens,
                         ['you', "should", 'have', 'a', 'nice', 'view', '.'])
        self.assertEqual(indexes,
                         [0,      4,       11,     17,   22,     29,     34])

        for i, token in enumerate(tokens):
            self.assertEqual(string[indexes[i]:indexes[i] + len(token)], token)

        



    def testTreebankTokenizer(self):
        tokenizer = IndexedTokenizer(TreebankWordTokenizer())
        string = " Facing the long wall in front of you, your destination will be the first door to your left (36-880)."
        indexes, tokens = tokenizer.tokenize(string)
        self.assertEqual(tokens,
                         ['Facing', 'the', 'long', 'wall', 'in', 'front', 'of', 'you', ',', 'your', 'destination', 'will', 'be', 'the', 'first', 'door', 'to', 'your', 'left', '(', '36-880', ')', '.'])

        for i, token in enumerate(tokens):
            self.assertEqual(string[indexes[i]:indexes[i] + len(token)], token)

        


    def testEmpty(self):
        tokens, indexes = chunker.tokenize("  ")
        self.assertEqual(len(tokens), 0)
        self.assertEqual(len(indexes), 0)
        
