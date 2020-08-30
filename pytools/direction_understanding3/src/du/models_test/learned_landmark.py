from du.models import hri2010_global
from nltk.stem.wordnet import WordNetLemmatizer
import cPickle

class model(hri2010_global.model):
    
    @property
    def wnet_lemmatizer(self):
        try:
            if(self.wl != None):
                return self.wl
        except:
            self.wl = WordNetLemmatizer()
        
        return self.wl
    
    def p_can_see_tag(self, tag, vtags, itags):
        #tag = self.wnet_lemmatizer.lemmatize(tag)
        
        if tag in vtags:
            return 1 - 1e-6
        
        l =  self.lmap_flickr
        res = l.predict(tag, vtags, learner="svm")
        if(res == None):
            return 1.0 - 1e-6
        
        return res[1].values()[-1]


    def load_lmap(self, fname):
        print "loading lmap", fname
        f = open(fname, "r")
        self.lmap_cache = cPickle.load(f)
        f.close()
        mynames = self.lmap_cache.tagnames
        
        
        #get the non-redundant names
        self.mynames = []
        for elt in mynames:
            if not elt in self.mynames:
                if (not "lda" in self.__module__ or
                    not elt in ["room", "type", "back", "area", "end", 
                                "intersection", "set", "space", "facing", 
                                "corner", "keep", "carpet", "grey", "gray", 
                                "stand", "till", "way", "ceiling", "cross", 
                                "number", "lead", "point", "row", "first"]):
                    self.mynames.append(elt)
        self.mynames.extend(self.clusters.tf.get_tag_names())
        self.mynames.append('EPSILON')

        #get a tag name to index hash
        i = 0
        self.names_to_index = {}
        for elt in self.mynames:
            self.names_to_index[elt] = i
            i+=1
            
