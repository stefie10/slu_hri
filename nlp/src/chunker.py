from environ_vars import TKLIB_HOME
from tokenizer import IndexedTokenizer
from nltk.chunk.util import tree2conlltags
from routeDirectionCorpusReader import readSession, Standoff
from sentenceTokenizer import SentenceTokenizer
import nltk.corpus
import pickle
import re

class SpatialTagger(nltk.TaggerI):
    def __init__(self, baseTagger):
        nltk.TaggerI.__init__(self)
        self.baseTagger = baseTagger
    def filterTags(self, tags):
        for token, tag in tags:
            token = token.lower()
            if token == "of":
                yield token, "OF"
            elif token == "ON":
                yield token, "ON"
            elif token == "with":
                yield token, "WITH"
            elif token in ("left", "right"):
                yield token, "SIDE"
            elif token in ("until", "till", "til"):
                yield token, "UNTIL"
            elif tag is None:
                yield token, "NN"
            else:
                yield token, tag
            
    def tag(self, tokens):
        tags = self.baseTagger.tag(tokens)
        tags = [x for x in self.filterTags(tags)]
        return tags

def getChunks(chunks, type):
    for c in chunks:
        if hasattr(c, "node") and c.node == type:
            yield c

def addChunks(chunkSequence, session, instructionIdx):
    for c in chunkSequence:
        if hasattr(c, "node"):
            if c.node == "NP":
                print "leaves", c.leaves()
                words = [word for word, tag, range in c.leaves()]
                print "chunk", " ".join(["%s/%s" % (word, tag) 
                                         for word, tag, range in c.leaves()])
                ranges = [range for word, tag, range in c.leaves()]
                entireRange = (ranges[0].start, ranges[-1].end)
                session.addAnnotation(instructionIdx, verb=None, 
                                      spatialRelation = None,
                                      landmark = Standoff(session, instructionIdx, entireRange))
                                      



def chunked_tags(train):
    """Generate a list of tags that tend to appear inside chunks"""
    cfdist = nltk.ConditionalFreqDist()
    for t in train:
        for word, tag, chtag in tree2conlltags(t):
            if chtag == "O":
                cfdist[tag].inc(False)
            else:
                cfdist[tag].inc(True)
    return [tag for tag in cfdist.conditions() if cfdist[tag].max() == True]


def baseline_chunker(train):
    chunk_tags = [re.sub(r'(\W)', r'\\\1', tag)
                  for tag in chunked_tags(train)]
    grammar = 'PP: {<%s>+}' % '|'.join(chunk_tags)
    return nltk.RegexpParser(grammar)


def makeSimpleTagger():
    #brown_a = nltk.corpus.brown.tagged_sents(fileids=['ca01', 'ca02', 'ca03', 'ca04', 'ca05'])
    brown_a = nltk.corpus.brown.tagged_sents()
    #brown_a = nltk.corpus.brown.tagged_sents(fileids=['ca01'])
    t0 = nltk.DefaultTagger("NN")
    t1 = nltk.UnigramTagger(brown_a, backoff=t0)
    t2 = nltk.BigramTagger(brown_a, backoff=t1)
    tagger = SpatialTagger(t2)
    pickle.dump(tagger, open("tagger.dat", "w"))
    return tagger

def backoff_tagger(tagged_sents, tagger_classes, backoff=None):
    if not backoff:
        backoff = tagger_classes[0](tagged_sents)
        del tagger_classes[0]
        
    for cls in tagger_classes:
        tagger = cls(tagged_sents, backoff=backoff)
        backoff = tagger
 
    return backoff
"""
From
http://streamhacker.com/2008/11/03/part-of-speech-tagging-with-nltk-part-1/
"""
def makeBrillTagger():
    import nltk.tag
    from nltk.tag import brill
    train_sents = nltk.corpus.brown.tagged_sents()
    word_patterns = [
        (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
        (r'.*ould$', 'MD'),
        (r'.*ing$', 'VBG'),
        (r'.*ed$', 'VBD'),
        (r'.*ness$', 'NN'),
        (r'.*ment$', 'NN'),
        (r'.*ful$', 'JJ'),
        (r'.*ious$', 'JJ'),
        (r'.*ble$', 'JJ'),
        (r'.*ic$', 'JJ'),
        (r'.*ive$', 'JJ'),
        (r'.*ic$', 'JJ'),
        (r'.*est$', 'JJ'),
        (r'^a$', 'PREP'),
        ]

    raubt_tagger = backoff_tagger(train_sents, [nltk.tag.AffixTagger,
                                                nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger],
                                  backoff=nltk.tag.RegexpTagger(word_patterns))

    # templates = [
    #     brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,1)),
    #     brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (2,2)),
    #     brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,2)),
    #     brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,3)),
    #     brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,1)),
    #     brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (2,2)),
    #     brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,2)),
    #     brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,3)),
    #     brill.ProximateTokensTemplate(brill.ProximateTagsRule, (-1, -1), (1,1)),
    #     brill.ProximateTokensTemplate(brill.ProximateWordsRule, (-1, -1), (1,1))
    #     ]
    templates = brill.fntbl37()
    trainer = nltk.BrillTaggerTrainer(raubt_tagger, templates)
    braubt_tagger = trainer.train(train_sents, max_rules=100, min_score=3)
    pickle.dump(braubt_tagger, open("data/braubt_tagger.dat", "w"))
    return braubt_tagger

def makeTagger():
#    return makeBrillTagger()
    tagger = pickle.load(open(TKLIB_HOME+"/nlp/data/braubt_tagger.dat"))
    tagger = SpatialTagger(tagger)
    return tagger

wordTokenizer = IndexedTokenizer()
def tokenize(string):
    return wordTokenizer.tokenize(string)
    
def simpleTokenize(string):
    indexedTokens = splitIdx(string)
    tokens = []
    for token, index in indexedTokens:
        newToken = trimPunctuation(token)
        if len(newToken) == 0:
            tokens.append(token)
        else:
            tokens.append(newToken)

    indexes = [index for token, index in indexedTokens]
    return indexes, tokens



class Chunker:
    def __init__(self):
        self.tagger = makeTagger()
        cp1 = nltk.RegexpParser(r"""
  NP: {<DT><JJ><NN>}      # Chunk det+adj+noun
      {<DT|NN>+}          # Chunk sequences of NN and DT
  """)
        
        training = nltk.corpus.conll2000.chunked_sents('train.txt', chunk_types=('PP',))
        
        cp2 = baseline_chunker(training)
        
        cp3 = nltk.RegexpParser(r"""
  NP: {<AT>?<JJ>*<NN.*>+}    # noun phrase chunks
  VP: {<TO>?<VB.*>}          # verb phrase chunks
  PP: {<IN>}                 # prepositional phrase chunks
  """)
        
        grammar = r"""
  NP: {<AT|JJ|NN.*>+}       # Chunk sequences of DT, JJ, NN
  NP: {<PP$|JJ|NN.*>+}       # Chunk sequences of DT, JJ, NN
  NP: {<AT|NN.*>+}       # Chunk sequences of DT, JJ, NN
  NP: {<PP$|NN.*>+}       # Chunk sequences of DT, JJ, NN
  PP: {<IN><NP>}            # Chunk prepositions followed by NP
  PP: {<AP><NP>}            # Chunk prepositions followed by NP
  VP: {<VB.*><NP|PP|S>+$}   # Chunk rightmost verbs and arguments/adjuncts
  S:  {<NP><VP>}            # Chunk NP, VP
  """

        grammar = r"""
  NP: {<AT><JJ|NNS$>*<NN|NNS>+}
  NP: {<NP><OF><NP>}
  """
        self.chunker = nltk.RegexpParser(grammar)
        #self.chunker = cp2
        
    def chunk(self, string):
        indexes, tokens = tokenize(string)
        tags = self.tagger.tag(tokens)
        chunk = self.chunker.parse(tags)
        return indexes, tokens, chunk
        

def chunkInstructions(fname):
    
    chunker = Chunker()
    sentenceTokenizer = SentenceTokenizer()
    sessions = readSession(fname, "regexp_chunker")
    for session in sessions:
        session.clearAnnotations()
        for instructionIdx, instruction in enumerate(session.routeInstructions):
            for sentenceStandoff in sentenceTokenizer.tokenize(session, instructionIdx):
                offset = sentenceStandoff.start
                print "instruction", instruction
                indexes, tokens, chunks = chunker.chunk(sentenceStandoff.text)
                print "# of chunks", len(chunks)
                for i, c in enumerate(chunks.leaves()):
                    str, tag = c
                    range = Standoff(session, instructionIdx, 
                                     (indexes[i] + offset, indexes[i] + len(str) + offset))
                    chunks[chunks.leaf_treeposition(i)] = (str, tag, range)
                    
                semantics = addChunks(chunks, session, instructionIdx)

            
        session.saveAnnotations()


def trimPunctuation(str):
    m = re.match(r"""^\W*(.*?)\W*$""", str)
    # *? means put as many punctuation characters as possible
    return m.groups()[0]
        
def splitIdx(str, regexp="\s+"):
    start = 0
    result = []
    def addResult(str, offset):
        if str != '':
            result.append((str, offset))
        
    for m in re.finditer(regexp, str):
        addResult(str[start:m.start()], start)
        start = m.end()
    addResult(str[start:], start)
    return result

if __name__ == "__main__":
    chunkInstructions("data/Direction understanding subjects Floor 1 (Final).ods")

