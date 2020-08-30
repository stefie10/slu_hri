from wordnet_tools import *

def tree_to_dot(mytree, filename):
    mystr = "digraph G {\n"
    mystr += tree_to_str(mytree)
    mystr += "}"

    myfile = open(filename, 'w')
    myfile.write(mystr)
    myfile.close()

def write_tree(keyword, filename):
    sense = N[keyword][0]
    ti = tree(sense, HYPONYM)
    tree_to_dot(ti, filename)
    

if __name__=="__main__":
    if(len(argv) == 3):
        write_tree(argv[1], argv[2])
    else:
        print "usage:\n\t>>python tree_to_dot.py keyword outfilename"
