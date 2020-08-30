from wordnet_tools import *

def list_elements(mytree, filename):
    return tree_to_hyponyms(mytree)

def write_tree(keyword, filename):
    myfile = open(filename, 'w')
    
    #get the possible senses
    senses = N[keyword]
    for i in range(len(senses)):
        myfile.write("-----------------------\n")
        sense = senses[i]
        ti = tree(sense, HYPONYM)
        mylist = list_elements(ti, filename)

        #write to file
        for elt in mylist:
            myfile.write(str(elt)+"\n")
    myfile.close()
    
if __name__=="__main__":
    if(len(argv) == 3):
        write_tree(argv[1], argv[2])
    else:
        print "usage:\n\t>>python list_elements.py keyword outfilename"
