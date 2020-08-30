from breadbox.physical_objects import get_ancestors
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
import chunker
import nltk
import orange
import re

    
labels =["cell", "breadbox", "closet", "room", "house", "city", "universe"]
def from_file(fname):
    data = []
    for lineno, l in enumerate(open(fname, "r")):
        #tokens = [t.strip() for t in l.split("\t") if t.strip() != ""]
        tokens = [t.strip() for t in re.split("\\s+", l) if t.strip() != ""]

        if tokens[-1] in labels:
            label = tokens[-1]
            word = " ".join(tokens[0:-1])
        else:
            label = "None"
            word = " ".join(tokens)
            
        
        # if len(tokens) == 1:
#             word = tokens[0]
#             label = "None"
#         elif len(tokens) == 2:
#             word, label = tokens
#         else:
#             raise ValueError("Could not read " + `l` + " in " + `fname` + " line " + `lineno` + " got: " + `len(tokens)` + " tokens" + " tokens: " + `tokens`)    
        data.append((word, label))
    return Annotations(data)

def split(annotations, indices):
    dataset = {}
    for dataset_idx, x in zip(indices, annotations.data):
        dataset.setdefault(dataset_idx, [])
        dataset[dataset_idx].append(x)

    result = [Annotations(dataset[idx]) for idx in sorted(dataset.keys())]
    for a in result:
        a.labels = annotations.labels
        for l in annotations.labels:
            a.label_to_count.setdefault(l, 0)
    return result
        

class Annotations:

    def __init__(self, data):

        self.data = data
        self.label_to_count = {}
        for word, label in data:
            if label != "None":
                assert label in labels, label
            self.label_to_count.setdefault(label, 0)
            self.label_to_count[label] += 1


        self.labels = self.label_to_count.keys()
        self.words = [w for w, l in self.data]
    @property
    def orange_class_var(self):
        return orange.EnumVariable("class", values=self.labels)
    def as_orange_table(self):
        domain = orange.Domain([], self.orange_class_var)
        domain.addmeta(orange.newmetaid(), orange.StringVariable("word"))

        table = orange.ExampleTable(domain)
        for word, label in self.data:
            ex = orange.Example(domain)
            ex["class"] = label
            ex["word"] = word
            table.append(ex)

        return table
            
    def synsets(self, word):
        return wn.synsets(word.replace(" ", "_"))
    
    def synset(self, word):
        synsets = self.synsets(word)
        if len(synsets) == 0:
            raise ValueError("No synsets for " + `word`)
        else: 
            return synsets[0]


    def ancestors(self, word):
        return get_ancestors(self.synset(word), Synset.hypernyms)

    def meronym_ancestors(self, i):
        return get_ancestors(self.synset(i), Synset.member_meronyms())
        
    def ancestor_map(self):
        """
        Return a map containing keys which are Synsets and values which are
        # of times the synset appears in the ancestors of the annotations.
        """
        ancestor_dist = nltk.FreqDist()
        for i, word in enumerate(self.words):
            ancestors = self.ancestors(word)
            for a in ancestors:
                ancestor_dist.inc(a)
        return ancestor_dist

    def gloss_map(self):
        gloss_dist = nltk.FreqDist()
        for i, word in enumerate(self.words):
            synset = self.synset(i)
            indexes, tokens = chunker.tokenize(synset.definition)
            for t in tokens:
                gloss_dist.inc(t)
        return gloss_dist
            
            
    def tags(self):
        tags = []
        ancestors = self.ancestor_map()
        for w in self.words:
            tags.append(w)
        for ancestor in ancestors.keys():
            for l in ancestor.lemmas:
                tags.append(l.name)
        return tags
        
    def cmp(self, l1, l2):
        if l1 == "None" or l2 == "None":
            return None
        else:
            i1 = labels.index(l1)
            i2 = labels.index(l2)
            return cmp(i1, i2)
    
            
def to_big_small(table):

    newdomain = orange.Domain(table.domain.attributes,
                              orange.EnumVariable("class", 
                                                  values=["big", "small", "None"]))
    newtable = orange.ExampleTable(newdomain)
    for ex in table:
        if ex["class"] != "None":
            idx = Annotations.labels.index(ex["class"])
            if idx >= Annotations.labels.index("closet"):
                label = "big"
            else:
                label = "small"
        else:
            label = "None"

        newex = orange.Example(newdomain, ex)
        print "label", label
        newex["class"] = label
        newtable.append(newex)
    return newtable
    
