import cPickle
from sys import argv
from nltk import word_tokenize
from routeDirectionCorpusReader import readSession
from tag_util import tag_file
from environ_vars import TKLIB_HOME
from du.stopwords import get_stopwords

def make_symmetric(prior):
    """
    There are entries where prior[key1][key2] exists, but not key2 in prior.
    This fixes that problem by putting in the corresponding entries. 
    """
    print "making symmetric"

    new_map = {}
    for key1 in prior.keys():
        for key2 in prior[key1].keys():
            if not key2 in prior:
                new_map.setdefault(key2, {})
                new_map[key2][key1] = prior[key1][key2]

    for key in new_map:
        assert not key in prior
        prior[key] = new_map[key]
    print "fixed", len(new_map), "entries"

    return prior


class keyword_extractor:
    def __init__(self):
        self.mytagger = cPickle.load(open('%s/pytools/direction_understanding2/bin/data/tagger/tagger.pck' % TKLIB_HOME, 'r'))
        self.swords = set(get_stopwords()) 
        #stopwords.words())

    def run_text(self, prior_cache, text):
        #mytags = mytagger.tag(words)
        #print "behind" in self.swords
        tokens = word_tokenize(text) 

        ret_keywords = set([])
        
        for i, token in enumerate(tokens):
            token = token.lower()

            if(prior_cache.has_key(token) and not token in self.swords):
                ret_keywords.add(token)

            #see if any of the pairs are reasonable
            if(i < len(tokens)-1 and not token in self.swords):
                token2 = tokens[i+1].lower()

                if(prior_cache.has_key(token+token2) and not token2 in self.swords):
                    ret_keywords.add(token+token2)
        
        return ret_keywords

    def run_dataset(self, prior_cache, corpus_fn):
        dsession = readSession(corpus_fn, "none")    
        prior_cache = make_symmetric(prior_cache)

        words = set([])

        for elt_i, elt in enumerate(dsession):
            print str(elt_i/(1.0*len(dsession)))+"% done"
            for i in range(len(elt.routeInstructions)):
                sentence = elt.routeInstructions[i]
                words.update(self.run_text(prior_cache, sentence))

        return words

    def run_tagfile(self, prior_cache, tag_fn):
        tf = tag_file(tag_fn, map_filename=None)

        words = set([])
        mynames = tf.get_tag_names()
        for name in mynames:
            words.update(self.run_text(prior_cache, name))

        return words


if __name__=="__main__":
    print argv
    if(len(argv) == 5):
        prior_cache = cPickle.load(open(argv[1], 'r'))
        
        kwex = keyword_extractor()

        #get the keywords from the dataset
        keywords = kwex.run_dataset(prior_cache, argv[2])
        
        #get the keywords from the tagfile
        keywords_tagfile = kwex.run_tagfile(prior_cache, argv[3])
        
        #update, convert to a list, and sort
        keywords.update(keywords_tagfile)
        keywords = list(keywords)
        keywords.sort()
        
        #save to a file
        print "Number of keywords found:", len(keywords)
        output_file = open(argv[4], 'w')
        for elt in keywords:
            output_file.write(elt+"\n");
    else:
        print "usage:\n\tpython extract_keywords.py prior_cache.pck direction_dataset tag_filename output_filename.txt"

