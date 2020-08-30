

        
class ModelEntry:
    def __init__(self, primitive, spanningInterval):
        self.primitive = primitive
        self.spanningInterval = spanningInterval.normalized()
        
    @property
    def si(self):
        """ 
        spanning interval
        """
        return self.spanningInterval
    
    def __repr__(self):
        return 'ModelEntry(%s, %s)' % (self.primitive, self.spanningInterval)
        
class Model:
    def __init__(self, modelEntries):
        self.entries = modelEntries
    def __repr__(self):
        return "Model([%s])" % (",\n    ".join([str(x) for x in self.entries]))
        