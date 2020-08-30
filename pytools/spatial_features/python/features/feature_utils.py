from itertools import chain

def convert_words(standoffs):
    return [s.text.lower().replace(" ", "_") for s in standoffs]

class EsdcFeatureTypeError(Exception):
    def __init__(self, *args, **margs):
        Exception.__init__(self, *args, **margs)


def add_prefix(prefix, fdict):
    return dict((prefix + key, value) for key, value in fdict.iteritems())

def compute_fdict(names, values):
    assert len(names) == len(values), (list(names), len(values))
    return dict(zip(names, values))

def merge(dict1, dict2):
    for key in dict1.keys() + dict2.keys():
        assert not(key in dict1 and key in dict2), ("key %s has value %.3f in dict1 and value %.3f in dict2" %
                                                    (key, dict1[key], dict2[key]))
        assert " " not in key, key

    return dict(chain(dict1.iteritems(), dict2.iteritems()))


def average_dicts(fdicts):
    keys = fdicts[0].keys()

    result_dict = dict((key, 0.0) for key in keys)

    for fdict in fdicts:
        for key, value in fdict.iteritems():
            result_dict[key] += value
            
    for key, value in result_dict.iteritems():
        result_dict[key] = float(value) / len(fdicts)
    return result_dict

def add_word_features(feature_dict, words):
    result_dict = {}
    for i, word in enumerate(words):
        for fname, fvalue in feature_dict.iteritems():
            new_key = "w_%s_%s" % (word, fname)
            result_dict[new_key] = fvalue

    #        new_key = "word_%d%s_%s" % (i, word, fname)
    #        result_dict[new_key] = fvalue

    # for word1, word2 in zip(words, words[1:]):
    #     for fname, fvalue in feature_dict.iteritems():
    #         new_key = "bigram_%s_%s_%s" % (word1, word2, fname)
    #         result_dict[new_key] = fvalue
            
    return result_dict

        
        
def typecheck(obj, expectedTypes):

    if isinstance(obj, expectedTypes):
        return True
    else:
        raise EsdcFeatureTypeError("obj " + `obj` + " " + `expectedTypes`)
    


def check_dicts(dict1, dict2):
    for key in dict1.keys() + dict2.keys():
        assert not(key in dict1 and key in dict2), ("key %s has value %.3f in dict1 and value %.3f in dict2" %
                                                    (key, dict1[key], dict2[key]))
