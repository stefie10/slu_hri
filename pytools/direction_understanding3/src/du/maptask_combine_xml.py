
from numpy import *
from sys import argv
import platform

if(int(platform.python_version_tuple()[1]) <= 4):
    from elementtree.ElementTree import *
else:
    from xml.etree.ElementTree import *
    
def immutable_dict(dct):
    return tuple(zip(dct.keys(),dct.values()))

def parse_xml(xml_filename):
    rss = parse(xml_filename).getroot()

    roothash={}
    roothash[(rss.tag,immutable_dict(rss.attrib))]=parse_xml_recurse(rss)
    return roothash

def parse_xml_recurse(element):
    if(len(element.getchildren()) == 0):
        return element.text
    
    myhash = {}
    for newelt in element.getchildren():
        if(not myhash.has_key(newelt.tag)):
            myhash[(newelt.tag,immutable_dict(newelt.attrib))] = parse_xml_recurse(newelt)
        else:
            if(not isinstance(myhash[newelt.tag], list)):
                tmpelt = myhash[newelt.tag] 
                myhash[(newelt.tag,immutable_dict(newelt.attrib))] = [tmpelt]
            myhash[(newelt.tag,immutable_dict(newelt.attrib))].append(parse_xml_recurse(newelt))

    return myhash



def start(tu):
    return float(dict(tu[1])['start'])
#    print "dict(tu[1])['start']", dict(tu[1])['start']
    
def compare_tu(tu1,tu2):
    value = start(tu1) - start(tu2)
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0
  

def speaker(giver_says):
    if giver_says:
        return "Giver"
    else:
        return "Follower"
    

def raw_combine_timed_words(timed_words_g,timed_words_f):
    g_i = 0
    f_i = 0
    
    text = []
    
    while g_i<len(timed_words_g) and f_i<len(timed_words_f):
        w_g = timed_words_g[g_i]
        w_f = timed_words_f[f_i]
        
        giver_says = bool(float(w_g[0])<float(w_f[0]))
        if(giver_says):
            w = w_g
            g_i += 1
        else:
            w = w_f
            f_i += 1
        
        if w[1] != None:
            text.append((speaker(giver_says),w[1]))
    
    #TODO add the remaining words 
    text.extend([(speaker(True ),w[1]) for w in filter(lambda x: bool(x[1]!=None),timed_words_g[g_i:])])           
    text.extend([(speaker(False),w[1]) for w in filter(lambda x: bool(x[1]!=None),timed_words_f[f_i:])])           
    
    return text  
    
def fine_timed(raw):
    
    text = []
    sent = ""
    current = raw[0][0]
    
    for wrd in raw:
        wt = wrd[1]
        ws = wrd[0]
        
        if ws != current:
            text.append((current,sent))
            current = ws
            sent = wt+" "
        else:
            sent += wt+" "
    text.append((current,sent))
    
    return text
        
def fine_to_csv(fine,filename):
    f = open(filename,"w")
    for person, sent in fine:
        f.write(person+","+sent+"\n")
    f.close()


    
def combine_maptask_dialogue(dialog_id,xml_dir,output_dir):
    
    # "q1ec1.g.timed-units.xml"
    hash_g = parse_xml(xml_dir+dialog_id+".g.timed-units.xml")
    hash_f = parse_xml(xml_dir+dialog_id+".f.timed-units.xml")

    root_g = hash_g.keys()[0]
    root_f = hash_f.keys()[0]
       
    g_timed = sorted(hash_g[root_g].keys(),compare_tu)
    f_timed = sorted(hash_f[root_f].keys(),compare_tu)

    timed_words_g = [(dict(key[1])["start"],hash_g[root_g][key]) for key in g_timed]
    timed_words_f = [(dict(key[1])["start"],hash_f[root_f][key]) for key in f_timed]
                
    raw_timed = raw_combine_timed_words(timed_words_g,timed_words_f)       
    fine = fine_timed(raw_timed)
        
    fine_to_csv(fine, output_dir+dialog_id+".csv")
    
def combine_all():
       
    xml_dir = "/home/stevend/Desktop/code/tklib/data/dialogue/Map Task/xml/"
    output_dir = "/home/stevend/Desktop/code/tklib/data/dialogue/Map Task/csv/"    
    
#    xml/q[1-8][en]c[1-8].[fg].timed-units.xml
    
    for i1 in range(1,9):
        for j in ['e','n']:
            for i2 in range(1,9):
                dialog_id = "q"+str(i1)+j+"c"+str(i2)
                combine_maptask_dialogue(dialog_id, xml_dir, output_dir)
                print "Did "+dialog_id
                
combine_all()            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    


