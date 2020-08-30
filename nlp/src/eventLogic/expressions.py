import eventLogic.allenRelations as ar

class Expression:
    pass


class Primitive(Expression):
    def __init__(self, *atoms):
        self.atoms = atoms
    def __eq__(self, p):
        return self.atoms == p.atoms and self.__class__ == p.__class__
    
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ",".join([repr(x) for x in self.atoms]))

class Or(Expression):
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return "Or(%s, %s)" % (repr(self.e1), repr(self.e2))
        
class Not(Expression):
    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return "Not(%s)" % (repr(self.e))
        
        
class AndR(Expression):
    def __init__(self, e1, allenRelations, e2):
        self.e1 = e1
        self.e2 = e2
        self.allenRelations = allenRelations
    def __repr__(self):
        return "AndR(%s, [%s], %s)" % (repr(self.e1), ",".join([x.__name__ for x in self.allenRelations]), repr(self.e2))


        
class Tense(Expression):

    """
    Annotated diamond_r in siskend01.pdf
    """
    def __init__(self, allenRelations, e):
        self.allenRelations = allenRelations
        self.e = e
        
    def __repr__(self):
        return "Tense([%s], %s)" % (",".join([x.__name__ for x in self.allenRelations]), repr(self.e))
    
def overlaps(e):
    return Tense([ar.overlaps, ar.iOverlaps, ar.starts, ar.iStarts, ar.finishes, ar.iFinishes, ar.during, ar.iDuring], e)


def cooccur(*args):
    if len(args) == 0:
        raise ValueError("Must pass something: " + `args`)
    elif len(args) == 1:
        return args[0]
    else:
        return AndR(args[0], [ar.equals], cooccur(*args[1:]))
