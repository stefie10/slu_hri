from memoized import memoized
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
import itertools
import nltk.corpus

if False:
    wn.synset = None # silence eclipse errors

def pos_tag(word):
    """
    Get pos tag for a single word.  Generally not a great idea because
    it will do much better on a sequence of words.
    """
    tags = nltk.pos_tag([word])
    assert len(tags) == 1
    word, tag = tags[0]
    return tag

def get_ancestors(synset, method=Synset.hypernyms):
    ancestors = set()
    curr_ancestors = set(method(synset))
    while len(curr_ancestors) != 0:
        new_ancestors = set()
        for a in curr_ancestors:
            new_ancestors.update(method(a))
        ancestors.update(curr_ancestors)
        curr_ancestors = new_ancestors
    return ancestors

def is_ancestor(lemma, synset):
    lemma.synset.hypernyms()
        

def is_physical_entity(word):
    wn = nltk.corpus.wordnet

    phys_yes = 0
    total = 0

    for synset in wn.synsets(word):
        all_parents = set([s.name 
                           for s in itertools.chain(*synset.hypernym_paths())])    

        if "physical_entity.n.01" in all_parents:
            phys_yes += 1

        total += 1
    if total == 0:
        return False

    ratio = phys_yes / float(total)
    if ratio > 0.5:
        return True
    else:
        return False

def get_wn_objects():
    wn_obj = wn.synset("object.n.01")
    objects = set()
    active_set = [wn_obj]
    while len(active_set) != 0:
        new_active_set = []
        for o in active_set:
            objects.add(o)
            new_active_set.extend(o.hyponyms())
        active_set = new_active_set
    return objects

def is_person(lemma):
    person = wn.synset("person.n.01")
    if person in get_ancestors(lemma.synset):
        return True
    else:
        return False
    
@memoized
def get_wn_object_lemmas():
    wn_objects = get_wn_objects()
    lemmas = set()
    for o in wn_objects:
        lemmas.update(o.lemmas)
    lemmas = sorted(lemmas, key=lambda l: l.count(), reverse=True)
    return lemmas

def main():
    #unigram_counts = FreqDist(word.lower()
    #                          for word in nltk.corpus.gutenberg.words())

    wn_object_lemmas = get_wn_object_lemmas()
    for i, l in enumerate([x for x in wn_object_lemmas if not is_person(x)]):
        print l.name.replace("_", " ")
        if i > 2000:
            break
if __name__ == "__main__":
    main()
