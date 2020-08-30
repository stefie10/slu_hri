from eventLogic import allenRelations
from eventLogic.interval import Interval, endStatus, min_inf, max_inf, NINF, \
    PINF, lt_inf, gt_inf, le_inf, implies, eq_inf, everything, CL, toString, ge_inf, \
    OP, isInf
import numpy as na
import sys

    
class SpanningIntervalSet:
    
        
    def __init__(self, intervals):
        self.intervals = [i.normalized() for i in intervals]
        self.intervals = [i for i in self.intervals if i != emptySpanningInterval]
        #self.intervals = SpanningIntervalSet.condense(self.intervals)

    def __getitem__(self, idx):
        try:
            return self.intervals[idx]
        except:
            print "intervals", self.intervals
            print "idx", idx
            raise
    
    def contains(self, interval):
        """
        If true, it's definitely contained
        But if false, it still could be, if you merge some of the si's in this set together
        """
        for si in self.intervals:
            if interval.subset(si) or si == interval:
                return True
        return False
    
    def intersectInterval(self, interval):
        results = [SpanningInterval.intersection(si, interval) for si in self.intervals]
        return SpanningIntervalSet(results)
    
    
    
    def snappedToMin(self, value=0):
        return SpanningIntervalSet([i.snappedToMin() for i in self.intervals])
        
    def condensed(self):

        intervals = self.intervals
        lastLength = sys.maxint
        cnt = 0
        while(len(intervals) < lastLength):
            lastLength = len(intervals)
            results = []
            for si in intervals:
                unified = False
                for i, r in enumerate(results):
                    if si.subset(r):
                        unified = True
                        break
                    else:
                        union = SpanningInterval.union(si, r)
                        if len(union) == 1:
                            results[i] = union[0]
                            unified = True
                            break
                if not unified:
                    results.append(si)
            intervals = results
            cnt += 1
        
        return SpanningIntervalSet(intervals) 
    
    @property
    def averageLength(self):
        if len(self.intervals) == 0:
            return 0
        else:
            return na.mean([s.averageLength for s in self.intervals])
    
    @staticmethod    
    def subsetInterval(intervals, si):
        for i in intervals:
            if si.subset(i):
                return si
        return None
    def __len__(self):
        return len(self.intervals)
    
    def __iter__(self):
        return self.intervals.__iter__()
    def __repr__(self):
        return "SpanningIntervalSet([%s])" % ",".join([str(s) for s in self.intervals])
    
    def __ne__(self, si):
        return not (self == si)
    def __eq__(self, si):
        if si == None:
            return False
        for interval in self.intervals:
            if not interval in si.intervals:
                return False
        for interval in si.intervals:
            if not interval in self.intervals:
                return False
        return True            
            
emptySpanningIntervalSet = SpanningIntervalSet([])
    
class SpanningInterval:
    def __init__(self, alpha, i1, i2, beta, isNormalized=False):
        self.alpha = alpha
        self.i1 = i1
        self.i2 = i2
        self.beta = beta
        
        self.isNormalized = isNormalized
        
        assert isinstance(self.i1, Interval)
        assert isinstance(self.i2, Interval)
        assert self.alpha in endStatus
        assert self.beta in endStatus

    @property
    def gamma(self):
        return self.i1.alpha
        
    @property
    def delta(self):
        return self.i1.beta
    
    @property
    def epsilon(self):
        return self.i2.alpha
    @property
    def zeta(self):
        return self.i2.beta
    
    @property
    def i(self):
        return self.i1.i
    @property
    def j(self):
        return self.i1.j
    
    @property
    def k(self):
        return self.i2.i
    @property
    def l(self):
        return self.i2.j
    
    def subset(self, si):
        return si == self or self.properSubset(si)
    
    def properSubset(self, si):
        if self == si:
            return False
        
        if self.alpha != si.alpha or self.beta != si.beta:
            return False
        
        if self.i1.subset(si.i1) and self.i2.subset(si.i2):
            return True 
        
        if (self.i1 == si.i1 and self.i2.subset(si.i2)):
            return True
        
        if (self.i1.subset(si.i1) and self.i2 == si.i2):
            return True

        return False
    
    def superset(self, si):
        
        
        if self == si:
            return False
        
        if self.alpha != si.alpha or self.beta != si.beta:
            return False

        if self.i1.superset(si.i2) and self.i2.superset(si.i2):
            return True
        
        if self.i1 == si.i1 and self.i2.superset(si.i2):
            return True
        
        if self.i1.superset(si.i1) and self.i2 == si.i2:
            return True
        
        return False
        
        
    
    def snappedToMin(self, value=0):
        return SpanningInterval(self.alpha, self.i1.snappedToMin(value=value),
                                self.i2.snappedToMin(value=value),
                                self.beta).normalized()
    @property
    def averageLength(self):
        c1 = self.i1.center 
        c2 = self.i2.center
        
        if isInf(c1) or isInf(c2):
            return PINF
        else:
            return c2-c1
        

    def normalized(self):
        if self.isNormalized:
            return self
        
        jPrime = min_inf([self.j, self.l])
        kPrime = max_inf([self.k, self.i])
        gammaPrime = self.gamma and self.i != NINF
        deltaPrime = (self.delta and jPrime != PINF and  
                      (lt_inf(self.j, self.l) or (self.zeta and self.alpha and self.beta)))
        epsilonPrime = (self.epsilon and kPrime != NINF and
                        (gt_inf(self.k, self.i) or (self.gamma and self.beta and self.alpha)))
        zetaPrime = self.zeta and self.l != PINF
            
        if (le_inf(self.i, jPrime) and le_inf(kPrime, self.l) and
             implies(eq_inf(self.i, jPrime), gammaPrime and deltaPrime) and
             implies(eq_inf(kPrime, self.l), epsilonPrime and zetaPrime) and
             implies(eq_inf(self.i, self.l), (self.alpha and self.beta)) and
             self.i != PINF and jPrime != NINF and 
             kPrime != PINF and self.l != NINF):
            return SpanningInterval(self.alpha,
                                    Interval(gammaPrime, self.i, jPrime, deltaPrime),
                                    Interval(epsilonPrime, kPrime, self.l, zetaPrime),
                                    self.beta, isNormalized=True)
        else:
            return emptySpanningInterval

        
    def complement(self):
        
        return SpanningIntervalSet([SpanningInterval(self.alpha, 
                                 everything,
                                 Interval(CL, NINF, self.k, not self.epsilon),
                                 self.beta),
                SpanningInterval(self.alpha,
                                 everything,
                                 Interval(not self.zeta, self.l, PINF, CL),
                                 self.beta),
                SpanningInterval(self.alpha,
                                 Interval(CL, NINF, self.i, not self.gamma),
                                 everything,
                                 self.beta),
                SpanningInterval(self.alpha, 
                                 Interval(not self.delta, self.j, PINF, CL),
                                 everything, 
                                 self.beta),
                SpanningInterval(not self.alpha, everything, everything, self.beta),
                SpanningInterval(self.alpha, everything, everything, not self.beta),
                SpanningInterval(not self.alpha, everything, everything, not self.beta),
                ])
                                                            
    def containsInterval(self, interval):
        return (interval.alpha == self.alpha and interval.beta == self.beta and
                self.i1.contains(interval.i) and self.i2.contains(interval.j))
        
    @property
    def largestInterval(self):
        return Interval(self.alpha, self.i1.i, self.i2.j, self.beta)
    def contains(self, number):
        return self.largestInterval.contains(number)
        
    def __eq__(self, si):
        if si == None:
            return False
        return self.alpha == si.alpha and self.beta == si.beta and self.i1 == si.i1 and self.i2 == si.i2
    
    def __repr__(self):
        if self == emptySpanningInterval:
            return "emptySpanningInterval"
        else:
            return "SpanningInterval(%s, %s, %s, %s)" % (toString(self.alpha), repr(self.i1), repr(self.i2), toString(self.beta))
    
    
    @staticmethod
    def union(si1, si2):
        if si1.alpha == si2.alpha and si1.beta == si2.beta:
            bigUnion = SpanningInterval(si1.alpha, 
                                        Interval.span(si1.i1, si2.i1),
                                        Interval.span(si1.i2, si2.i2),
                                        si1.beta)
            bigUnionNotInSi1 = si1.complement().intersectInterval(bigUnion) 
            bigUnionNotInSi2 = si2.complement().intersectInterval(bigUnion)
            
            if (all([i.subset(si2) for i in bigUnionNotInSi1]) and
                all([i.subset(si1) for i in bigUnionNotInSi2])):
                return SpanningIntervalSet([bigUnion]) 

        return SpanningIntervalSet([si1, si2])
        
        

    @staticmethod
    def intersection(i1, i2):
        
        if i1.alpha  == i2.alpha and i1.beta == i2.beta:
            if gt_inf(i1.i, i2.i):
                gamma = i1.gamma
            elif i1.i == i2.i:
                gamma = i1.gamma and i2.gamma
            elif lt_inf(i1.i, i2.i):
                gamma = i2.gamma
            else:
                raise ValueError()
        
            if lt_inf(i1.j, i2.j):
                delta = i1.delta
            elif i1.j == i2.j:
                delta = i1.delta and i2.delta
            elif gt_inf(i1.j, i2.j):
                delta = i2.delta
            else:
                raise ValueError()
            
            if gt_inf(i1.k, i2.k):
                epsilon = i1.epsilon
            elif i1.k == i2.k:
                epsilon = i1.epsilon and i2.epsilon
            elif lt_inf(i1.k, i2.k):
                epsilon = i2.epsilon
            else:
                raise ValueError()
            
            if lt_inf(i1.l, i2.l):
                zeta = i1.zeta
            elif i1.l == i2.l:
                zeta = i1.zeta and i2.zeta
            elif gt_inf(i1.l, i2.l):
                zeta = i2.zeta
            else:
                raise ValueError()

            return SpanningInterval(i1.alpha, 
                                    Interval(gamma, max_inf([i1.i, i2.i]),
                                             min_inf([i1.j, i2.j]),
                                             delta),
                                    Interval(epsilon, max_inf([i1.k, i2.k]),
                                             min_inf([i1.l, i2.l]),
                                             zeta),
                                    i1.beta).normalized()
                                    
        else:
            return emptySpanningInterval 
                                                   
    @staticmethod
    def I(i, relation, j):
        results = []
        for iprime in j.D(allenRelations.inverse(relation)):
            iprimeprime  =  SpanningInterval.intersection(iprime, i)
            for jprime in i.D(relation):
                jprimeprime = SpanningInterval.intersection(jprime, j)
                results.extend(SpanningInterval.span(iprimeprime, jprimeprime))
        return SpanningIntervalSet(results)
    

    @staticmethod
    def span(i1, i2):
        j = min_inf([i1.j, i2.j])
        k = max_inf([i1.k, i2.k])
        delta = ((i1.delta and le_inf(i1.j, i2.j)) or
                 (i2.delta and ge_inf(i1.j, i2.j)))
        epsilon = ((i1.epsilon and ge_inf(i1.k, i2.k)) or
                   (i2.epsilon and le_inf(i1.k, i2.k)))
        
        return SpanningIntervalSet(
                [SpanningInterval(i1.alpha, 
                                  Interval(i1.gamma, i1.i, i1.j, i1.delta),
                                  Interval(i1.epsilon, i1.k, i1.l, i1.zeta),
                                  i1.beta),
                SpanningInterval(i1.alpha,
                                 Interval(i1.gamma, i1.i, j, delta),
                                 Interval(epsilon, k, i1.l, i1.zeta),
                                 i1.beta),
                SpanningInterval(i1.alpha,
                                 Interval(i1.gamma, i1.i, j, delta),
                                 Interval(epsilon, k, i2.l, i2.zeta),
                                 i2.beta),
                SpanningInterval(i2.alpha, 
                                 Interval(i2.gamma, i2.i, j, delta),
                                 Interval(epsilon, k, i1.l, i1.zeta),
                                 i1.beta),
                SpanningInterval(i2.alpha,
                                 Interval(i2.gamma, i2.i, j, delta),
                                 Interval(epsilon, k, i2.l, i2.zeta),
                                 i2.beta)])
        
    def D(self, allenRelation):
        if allenRelation == allenRelations.equals:
            return SpanningIntervalSet([self])
        elif allenRelation == allenRelations.lessThan:
            result = []
            for alpha2 in endStatus:
                for beta2 in endStatus:
                    result.append(SpanningInterval(alpha2,
                                                   Interval(not self.beta and not alpha2 and self.epsilon,
                                                            self.k, PINF, CL),
                                                    everything,
                                                    beta2))
            return SpanningIntervalSet(result)
        elif allenRelation == allenRelations.greaterThan:
            result = []
            for alpha2 in endStatus:
                for beta2 in endStatus:
                    result.append(SpanningInterval(alpha2, everything,
                                                   Interval(CL,
                                                            NINF, self.j,
                                                            not self.alpha and not beta2 and self.delta),
                                                    beta2))
                                                            
            return SpanningIntervalSet(result)
        elif allenRelation == allenRelations.meets:
            result = []
            for beta2 in endStatus:
                result.append(SpanningInterval(not self.beta,
                                               self.i2,
                                               everything,
                                               beta2))
            return SpanningIntervalSet(result)                
        elif allenRelation == allenRelations.iMeets:
            result = []
            for alpha2 in endStatus:
                result.append(SpanningInterval(alpha2, everything,
                                               self.i1,
                                               not self.alpha))
            return SpanningIntervalSet(result)                
        elif allenRelation == allenRelations.overlaps:
            result = []
            for alpha2 in endStatus:
                for beta2 in endStatus:
                    result.append(SpanningInterval(alpha2,
                                                   Interval(self.alpha and not alpha2 and self.gamma,
                                                            self.i, self.l,
                                                            self.beta and alpha2 and self.zeta),
                                                    Interval(not self.beta and beta2 and self.epsilon,
                                                             self.k, PINF, CL),
                                                    beta2))
            return SpanningIntervalSet(result)                                    
        elif allenRelation == allenRelations.iOverlaps:
            result = []
            for alpha2 in endStatus:
                for beta2 in endStatus:
                    result.append(SpanningInterval(alpha2,
                                                   Interval(CL, NINF, self.j,
                                                            not self.alpha and alpha2 and self.delta), 
                                                   Interval(self.alpha and beta2 and self.gamma,
                                                            self.i, self.l, 
                                                            self.beta and not beta2 and self.zeta),
                                                    beta2))
            return SpanningIntervalSet(result)
        elif allenRelation == allenRelations.starts:
            result = []
            for beta2 in endStatus:
                result.append(SpanningInterval(self.alpha, self.i1,
                                               Interval(not self.beta and beta2 and self.epsilon,
                                                        self.k, PINF, CL),
                                                beta2))
            return SpanningIntervalSet(result)
        elif allenRelation == allenRelations.iStarts:
            result = []
            for beta2 in endStatus:
                result.append(SpanningInterval(self.alpha, self.i1, 
                                               Interval(CL, NINF, self.l, 
                                                        self.beta and not beta2 and self.zeta),
                                                beta2))
            return SpanningIntervalSet(result)
        elif allenRelation == allenRelations.finishes:
            result = []
            for alpha2 in endStatus:
                result.append(SpanningInterval(alpha2,
                                               Interval(CL, NINF, self.j,
                                                        not self.alpha and alpha2 and self.delta),
                                                self.i2,
                                                self.beta))
            return SpanningIntervalSet(result)                
        elif allenRelation == allenRelations.iFinishes:
            result = []
            for alpha2 in endStatus:
                result.append(SpanningInterval(alpha2, Interval(self.alpha and not alpha2 and self.gamma,
                                                                self.i, PINF, CL),
                                                self.i2,
                                                self.beta))
            return SpanningIntervalSet(result)                
        elif allenRelation == allenRelations.during:
            result = []
            for alpha2 in endStatus:
                for beta2 in endStatus:
                    result.append(SpanningInterval(alpha2, Interval(CL, NINF, self.j,
                                                                    not self.alpha and alpha2 and self.delta),
                                                            Interval(not self.beta and beta2 and self.epsilon,
                                                                     self.k, PINF, CL),
                                                    beta2))
            return SpanningIntervalSet(result)                    
        elif allenRelation == allenRelations.iDuring:
            result = []
            for alpha2 in endStatus:
                for beta2 in endStatus:
                    result.append(SpanningInterval(alpha2,
                                                   Interval(self.alpha and alpha2 and self.gamma,
                                                            self.i, PINF, CL),
                                                   Interval(CL, NINF, self.l,
                                                            self.beta and not beta2 and self.zeta),
                                                    beta2))
            return SpanningIntervalSet(result)                    
        else:
            raise ValueError("Bad relation: " + `allenRelation`)
    

emptySpanningInterval = SpanningInterval(OP, Interval(OP, 0, 0, OP), Interval(OP, 0, 0, OP), OP,
                                         isNormalized=True)
allIntervals = SpanningIntervalSet([
    SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP),
    SpanningInterval(OP, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), CL),
    SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), OP),
    SpanningInterval(CL, Interval(OP, NINF, PINF, OP), Interval(OP, NINF, PINF, OP), CL),
    ])