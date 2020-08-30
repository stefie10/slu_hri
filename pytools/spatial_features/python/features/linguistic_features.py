from environ_vars import TKLIB_HOME
import wordnet_util as wu
import readonly_shelf
#global variables for flickr and wordnet similarity
from memoized import memoized
#import cPickle

wmap = None;

def merge(dict1, dict2):
    #check_dicts(dict1, dict2)
    result = {}
    result.update(dict1)
    result.update(dict2)
    return result


@memoized
def wordnet_similarity(kword, qword):
    load_wmap()
    kword = str(kword)
    if (wmap.has_key(kword) and wmap[kword].has_key(qword)):
        return wmap[kword][qword]
    else:
        #print "recomputing", kword, qword
        return wu.get_word_similarity_path(kword,qword)
    
lmap = None; 

def load_lmap():
    global lmap;
    
    if(lmap == None):
        fname = TKLIB_HOME+"/data/flickr/flickr_cache.shelf"
        try:
            lmap = readonly_shelf.open(fname)
        except:
            print "can't open", fname
            raise
                                   

def load_wmap():
    global wmap
    if(wmap == None):
        try:
            fname = TKLIB_HOME+"/data/wordnet/wordnet_cache.shelf"
            wmap = readonly_shelf.open(fname)
        except:
            print "can't open", fname
            raise
                                   

def flickr_similarity(kword, qword):
    load_lmap()    
    kword = str(kword)

    if lmap.has_key(kword) and lmap[kword].has_key(qword):
        return lmap[kword][qword]

    return 0;

def load_maps():
    load_lmap()
    load_wmap()
import enchant
enchantDict = enchant.Dict("en_us")
enchantDict.__del__ = lambda x: None
print "del", enchantDict.__del__
def depluralize(word):
    stems = []
    if(word == 's'):
        return word
    if word[-2:] == 'es':
        stems.append(word[:-2])
    if word[-1:] == 's':
        stems.append(word[:-1])
    for stem in stems:
        if enchantDict.check(stem):
            return stem
    return word

def sfe_language_object(f_words, visible_obj_words, selected_obj_words):
    """
    Compute language-object features for groups of words.
    """

    f_words = [depluralize(w) for w in f_words]
    
    result = {}
    if visible_obj_words != None:
        visible_obj_words = [depluralize(w) for w in visible_obj_words]
        map1 = word_features(f_words, visible_obj_words, "f_context")
        result = merge(result, map1)
    
    if selected_obj_words != None:
        selected_obj_words = [depluralize(w) for w in selected_obj_words]
        map3 = word_features(f_words, selected_obj_words, "f_selected")
        result = merge(result, map3)

    return result

def word_features(command_words, environment_words, prefix):
    """
    Compute similarity between two groups of words.
    """
    #now iterate through and get the features
    ret_map = {}
    
    if len(command_words) == 0 or len(environment_words) == 0:
        return ret_map
    
    #how much objects are related to a given word in the language
    max_all_flr = 0;     max_all_sim = 0;



    for cword in command_words:
        max_flr = 0; max_sim = 0;
        overlap_cnt = 0

        for eword in environment_words:
            #if the word is in the query
            if eword in cword:
                ret_map[prefix + "_e" + eword + "_in_cword"] = 1.0
                overlap_cnt += 1
                    
            #flickr similarity...
            f_flr = flickr_similarity(eword, cword)
            if(f_flr > max_flr):
                max_flr = f_flr
            if(f_flr > max_all_flr):
                max_all_flr = f_flr

            #wordnet similarity...
            f_sim = wordnet_similarity(eword, cword)
            if(f_sim > max_all_sim):
                max_all_sim = f_sim
            if(f_sim > max_sim):
                max_sim = f_sim

            #co-occurrance between two objects
            #ret_names.append(prefix + "_" + cword+"_rel_"+eword)
            #ret_vals.append(1.0)
            ret_map[prefix + "_c_" + cword + "_e_" + eword] = True
            key = prefix + "_c_" + cword + "_e_" + eword

        ret_map[prefix + "_c_" + cword + "_overlap_cnt"] = overlap_cnt
        ret_map[prefix + "_c_" + cword + "_has_overlap"] = True if overlap_cnt != 0 else False
        ret_map[prefix + "_c_" + cword + "_max_flickr"] = max_flr
        ret_map[prefix + "_c_" + cword + "_max_wordnet"] = max_sim
        
    ret_map[prefix+"_max_all_flickr"] = max_all_flr

    ret_map[prefix+"_max_all_wordnet"] = max_all_sim
    
    # how much words are related to a given object in the world...
    for eword in environment_words:
        max_flr = 0; max_sim = 0;
        for cword in command_words:
            f_flr = flickr_similarity(eword, cword)
            if(f_flr > max_flr):
                max_flr = f_flr

            f_sim = wordnet_similarity(eword,cword)
            if(f_sim > max_sim):
                max_sim = f_sim
        ret_map[prefix+"_max_wordnet_object_"+eword] = max_sim
        ret_map[prefix+"_max_flickr_object_"+eword] = max_flr

    ret_map = dict((key.replace(" ", "_"), value) for key, value in ret_map.iteritems())

    return ret_map
