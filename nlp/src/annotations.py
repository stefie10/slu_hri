import numpy as na

from routeDirectionCorpusReader import Annotation

"""
Input: a list of annotations
Return a matrix.  Each entry i, j represents whether annotations[i].contains(annotations[j])
"""
def containmentMatrix(annotations):
    matrix = na.zeros((len(annotations), len(annotations)), dtype=bool)
    
    for i, a in enumerate(annotations):
        for j, b in enumerate(annotations):
            if a.contains(b):
                matrix[i,j] = True
            else:
                matrix[i,j] = False
    return matrix
                

def tree(annotations):
    containment = containmentMatrix(annotations)
    
    tree = na.array(containment)

    numberOfParents = [(i, containment[:,i].sum()) 
                       for i in range(len(annotations))]
    numberOfParents.sort(key=lambda x: x[1])
    
    for key, count in numberOfParents:
        print key, count            
        if count >= 2:
            print "larger than 2, have to implement the real algorithm"
            raise ValueError()
        else:
            continue

    
    
    return tree


def containingAnnotations(annotations, targetRange):
    for annotation in annotations:
        for key in Annotation.keys:
            if annotation.annotationMap[key].contains(targetRange):
                return annotation, key
    return None, None
