threshold = 0.0000001
import math
import numpy as na

def sorta_eq(v1, v2, threshold=threshold):
    return math.fabs(v1 - v2) < threshold
def array_equal(arr1, arr2):
    if arr1 == None or arr2 == None:
        return False
    if len(arr1) != len(arr2):
        return False
    else:
        return (na.fabs(na.array(arr1) - na.array(arr2)) < threshold).all()
def assert_sorta_eq(v1, v2):
    assert sorta_eq(v1, v2), (v1, v2)

def assert_array_equal(arr1, arr2):
    try:
        for a1, a2 in zip(arr1, arr2):
            if hasattr(a1, "__iter__") and hasattr(a2, "__iter__"):
                assert_array_equal(a1, a2)
            else:
                assert_sorta_eq(a1, a2)            
        assert len(arr1) == len(arr2), (arr1, arr2)
    except:
        print "arr1", arr1
        print "arr2", arr2
        raise
    #assert array_equal(arr1, arr2), (arr1, arr2)



def has_unique_maximum(lst):
    """
    Whether the list has a unique maximum.
    """
    max_idx = na.argmax(lst)
    max_val = lst[max_idx]
    
    values = [v for v in lst if v == max_val]
    if len(values) == 1:
        return True
    elif len(values) > 1:
        return False
    else:
        raise ValueError("Should never get here: " + `values`)
