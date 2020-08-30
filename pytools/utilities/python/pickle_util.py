import cPickle

def save(fname, obj):
    with open(fname, "wb") as f:
        cPickle.dump(obj, f, protocol=2)

def load(fname):
    with open(fname, "r") as f:
        return cPickle.load(f)
