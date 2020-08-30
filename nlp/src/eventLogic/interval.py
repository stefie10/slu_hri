CL = True
OP = False
CL = CL
OP = OP

def toString(endStatus):
    if endStatus == CL:
        return "CL"
    elif endStatus == OP:
        return "OP"
    else:
        raise ValueError("Bad argument: " + `endStatus`)

endStatus = [OP, CL]

PINF = "PINF"
NINF = "NINF"
PINF = PINF
NINF = NINF
infinities = [PINF, NINF]

class Interval:
    def __init__(self, alpha, i, j, beta):
        self.alpha = alpha
        assert self.alpha in endStatus
        
        self.i = i
        if self.i not in infinities:
            self.i = float(i)
        
        self.j = j    
        if self.j not in infinities:
            self.j = float(j)            
        
        self.beta = beta
        assert self.beta in endStatus

    def isNormalized(self):
        return lt_param(self.alpha and self.beta, self.i, self.j)
    
    @property
    def center(self):
        if self.i == NINF and self.j == PINF:
            return 0
        elif self.i == NINF:
            return NINF
        elif self.j == PINF:
            return PINF
        else:
            return (self.i + self.j)/2.0
    @property
    def length(self):
        if self.i == NINF or self.j == PINF:
            return PINF
        else:
            return self.j - self.i
        
    def snappedToMin(self, value=0):
        
        if lt_inf(self.i, value):
            return Interval(CL, value, self.j, self.beta)
        else:
            return self
        
    def contains(self, number):
        truthValue = True
        
        if self.i == PINF:
            truthValue = truthValue and False
        elif self.i == NINF:
            truthValue = truthValue and True
        else:
            if self.alpha == CL:
                truthValue = truthValue and self.i <= number
            elif self.alpha == OP:
                truthValue = truthValue and self.i < number
            else:
                raise ValueError("Bad alpha; " + `self.alpha`)
        
        if self.j == PINF:
            truthValue = truthValue and True
        elif self.j == NINF:
            truthValue = truthValue and False
        else:        
            if self.beta == CL:
                truthValue = truthValue and number <= self.j
            elif self.beta == OP:
                truthValue = truthValue and number < self.j
            else:
                raise ValueError("Bad alpha; " + `self.beta`)
        
        return truthValue
    
    def __eq__(self, interval):
        return self.i == interval.i and self.j == interval.j and self.alpha == interval.alpha and self.beta == interval.beta
    def __repr__(self):
        return "Interval(%s, %s, %s, %s)" % (toString(self.alpha), self.i, self.j, toString(self.beta))
    
    @staticmethod
    def span(i1, i2):
        return Interval((i1.alpha and le_inf(i1.i, i2.i) or 
                        (i2.alpha and ge_inf(i1.i, i2.i))), 
                        min_inf([i1.i, i2.i]), max_inf([i1.j, i2.j]),
                        (i1.beta and ge_inf(i1.j, i2.j) or
                         i2.beta and le_inf(i1.j, i2.j)))
        
    def superset(self, i):
        import allenRelations
        allenRelation = allenRelations.findRelation(self, i)
        
        if allenRelation in (allenRelations.iStarts, allenRelations.iFinishes, allenRelations.iDuring):
            return True
        else:
            return False
        
        
    def subset(self, i):
        import allenRelations
        allenRelation = allenRelations.findRelation(self, i)
        
        if allenRelation in (allenRelations.starts, allenRelations.finishes, allenRelations.during):
            return True
        else:
            return False
        

def isInf(x):
    return x in (PINF, NINF)            
def cmp_inf(x, y):
    if x == y:
        return 0
    else:
        if x == NINF:
            return -1
        elif x == PINF:
            return 1
        elif y == NINF:
            return 1
        elif y == NINF:
            return -1
        else:
            return cmp(x, y)
def lt_inf(x, y):
    return cmp_inf(x, y) == -1

def gt_inf(x, y):
    return cmp_inf(x, y) == 1

def lt_param(openOrClosed, x, y):
    if openOrClosed == OP:
        return lt_inf(x, y)
    elif openOrClosed == CL:
        return le_inf(x, y)
    else:
        raise ValueError("openOrClosed: " + `openOrClosed`)

def gt_param(openOrClosed, x, y):
    if openOrClosed == OP:
        return gt_inf(x, y)
    elif openOrClosed == CL:
        return ge_inf(x, y)
    else:
        raise ValueError("openOrClosed: " + `openOrClosed`)

def le_inf(x, y):
    return cmp_inf(x, y) in (-1, 0)

def ge_inf(x, y):
    return cmp_inf(x, y) in (1, 0)
def eq_inf(x, y):
    return cmp_inf(x, y) == 0

def min_inf(lst):
    if NINF in lst:
        return NINF
    else:
        noinf = [x for x in lst if x not in infinities]
        if len(noinf) != 0:
            return min(noinf)
        else:
            return lst[0]

def max_inf(lst):
    if PINF in lst:
        return PINF
    else:
        noinf = [x for x in lst if x not in infinities]
        if len(noinf) != 0:
            return max(noinf)
        else:
            return lst[0]

def implies(c1, c2):
    return not c1 or (c1 and c2)


everything = Interval(CL, NINF, PINF, CL)
emptyInterval = Interval(OP, 0, 0, OP)