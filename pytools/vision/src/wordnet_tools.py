from wordnet import *
#from nltk.wordnet import *
from wntools import *
from sys import argv

#from sys import argv


def tree_to_str(mytree):
    return tree_to_str_rec(mytree, 0)

#fixme 
def tree_to_str_rec(mytree, i):
    mystr = ""
    for elt in mytree:
        if(str(type(elt)) == "<type 'list'>" and len(elt) == 1 and i == 0):
            #print '"'+ str(list_to_elts(mytree[0]))+ '" -> "' + str(list_to_elts(elt[0])) + '";\n'
            print mytree[0]
            mystr += '"'+ str(mytree[0].getWord()) + '" -> "' + str(list_to_elts(elt[0])) + '";\n'

        elif(str(type(elt)) == "<type 'list'>" and len(elt) == 1):
            #print '"'+ str(list_to_elts(mytree[0]))+ '" -> "' + str(list_to_elts(elt[0])) + '";\n'
            mystr += '"'+ str(list_to_elts(mytree[0]))+ '" -> "' + str(list_to_elts(elt[0])) + '";\n'

        elif(str(type(elt)) == "<type 'list'>" and i == 0):
            print mytree[0]
            mystr += '"'+ str(mytree[0].getWord())+ '" -> "' + str(list_to_elts(elt[0])) + '";\n'
            mystr += tree_to_str_rec(elt, i+1)

        elif(str(type(elt)) == "<type 'list'>"):
            print mytree[0]
            mystr += '"'+ str(list_to_elts(mytree[0]))+ '" -> "' + str(list_to_elts(elt[0])) + '";\n'
            mystr += tree_to_str_rec(elt, i+1)

    return mystr



def tree_to_hyponyms(mytree):
    return tree_to_hyponyms_rec(mytree, 0)

#fixme 
def tree_to_hyponyms_rec(mytree, i):
    mylist = []
    for elt in mytree:
        if(str(type(elt)) == "<type 'list'>" and len(elt) == 1 and i == 0):
            print mytree[0]
            mylist.extend(list_to_elts(elt[0]))
        elif(str(type(elt)) == "<type 'list'>" and len(elt) == 1):
            print mytree[0]
            mylist.extend(list_to_elts(elt[0]))
        elif(str(type(elt)) == "<type 'list'>" and i == 0):
            print mytree[0]
            mylist.extend(list_to_elts(elt[0]))
            print "rec"
            mylist.extend(tree_to_hyponyms_rec(elt, i+1))
        elif(str(type(elt)) == "<type 'list'>"):
            print mytree[0]
            mylist.extend(list_to_elts(elt[0]))
            print "rec"
            mylist.extend(tree_to_hyponyms_rec(elt, i+1))
    return mylist


def list_to_elts(mylist):
    retlist = []
    for i in range(len(mylist)):
        myword = mylist[i].getWord()
        retlist.append(myword)
    return retlist
    


    
