from eventLogic.interval import lt_param, gt_param


def equals(i1, i2):
    return i1.i == i2.i and i1.alpha == i2.alpha and i1.j == i2.j and i1.beta == i2.beta    

def lessThan(i1, i2):
    return lt_param(not i1.beta and not i2.alpha, i1.j, i2.i)

def greaterThan(i1, i2):
    return gt_param(not i1.alpha and not i2.beta, i1.i, i2.j)


def meets(i1, i2):
    return i1.j == i2.i and i1.beta != i2.alpha

def iMeets(i1, i2):
    return i1.i == i2.j and i1.alpha != i2.beta

def overlaps(i1, i2):
    return (lt_param(i1.alpha and not i2.alpha, i1.i, i2.i) and
            lt_param(i1.beta and i2.alpha, i2.i, i1.j) and
            lt_param(not i1.beta and i2.beta, i1.j, i2.j))
    

def iOverlaps(i1, i2):
    return overlaps(i2, i1)
    

def starts(i1, i2):
    return (i1.i == i2.i and i1.alpha == i2.alpha and 
            lt_param(not i1.beta and i2.beta, i1.j, i2.j))

def iStarts(i1, i2):
    return starts(i2, i1)

def finishes(i1, i2):
    return (gt_param(not i1.alpha and i2.alpha, i1.i, i2.i) and
            i1.j == i2.j and i1.beta == i2.beta)

def iFinishes(i1, i2):
    return finishes(i2, i1)

def during(i1, i2):
    return (gt_param(not i1.alpha and i2.alpha, i1.i, i2.i) and
            lt_param(not i1.beta and i2.beta, i1.j, i2.j))

def iDuring(i1, i2):
    return during(i2, i1)

relations = [lessThan, greaterThan, meets, overlaps, starts, finishes, during, iMeets, iOverlaps, iStarts, iFinishes, iDuring, equals]

def inverse(relation):
    if relation == lessThan:
        return greaterThan
    elif relation == greaterThan:
        return lessThan
    elif relation == meets:
        return iMeets
    elif relation == iMeets:
        return meets
    elif relation == overlaps:
        return iOverlaps
    elif relation == iOverlaps:
        return overlaps
    elif relation == starts:
        return iStarts
    elif relation == iStarts:
        return starts
    elif relation == finishes:
        return iFinishes
    elif relation == iFinishes:
        return finishes
    elif relation == during:
        return iDuring
    elif relation == iDuring:
        return during
    elif relation == equals:
        return equals
    else:
        raise ValueError("Invalid relation: " + `relation`)

def findRelation(i1, i2):
    relation = None
    for r in relations:
        if r(i1, i2):
            if relation != None:
                raise ValueError("More than one relation is true: " + `r` + " " + `relation`)
            relation = r
    if relation == None:
        raise ValueError("No relation for " + `i1` + " and " + `i2`)
    return relation