from wordnet_tools import *

def list_elements(mytree, filename):
    mylist = tree_to_hypernyms(mytree)
    myfile = open(filename, 'w')
    for elt in mylist:
        myfile.write(str(elt)+"\n")
    myfile.close()

def write_tree(keyword, filename):
    sense = N[keyword][0]
    ti = tree(sense, HYPERNYM)
    list_elements(ti, filename)
    

if __name__=="__main__":
    if(len(argv) == 3):
        write_tree(argv[1], argv[2])
    else:
        print "usage:\n\t>>python list_elements.py keyword outfilename"
