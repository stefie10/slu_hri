import unittest
import sentenceTokenizer
from routeDirectionCorpusReader import readSession
class SentenceTokenizerTestCase(unittest.TestCase):
    def testSentenceTokenizer(self):
        fname = "data/Direction understanding subjects Floor 1 (Final).ods"

        sessions = readSession(fname, "stefie10")

        session = sessions[0]

        tokenizer = sentenceTokenizer.SentenceTokenizer()
        standoffs = tokenizer.tokenize(session.routeInstructions[0])
        self.assertEqual(len(standoffs), 4)
        self.assertEqual(standoffs[0].text, 
                         "With your back to the glass entryways, walk toward the question mark sign.")
        for session in sessions:
            for instructionIdx, instruction in enumerate(session.routeInstructions):
                standoffs = tokenizer.tokenize(session.routeInstructions[0])
    def testRepeatedSentences(self):
        tokenizer = sentenceTokenizer.SentenceTokenizer()
        string = "Turn right.  Turn right."
        standoffs = tokenizer.tokenize(string)
        print standoffs
        sentences = [string[standoff.range[0]:standoff.range[1]] for standoff in standoffs]
        self.assertEqual(sentences[0], "Turn right.")
        self.assertEqual(sentences[1], "Turn right.")

        
        
