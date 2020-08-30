from pyTklib import tklib_range
from scipy import arange

def test1():
    print "arange", arange(0, 1, 0.1)
    print "tklib_range", tklib_range(0, 1, 0.1)

if __name__=="__main__":
    test1()
