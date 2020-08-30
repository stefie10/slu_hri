from pyTklib import SplineC
from scipy import pi, arange
from pylab import *


def test1():
    mystart = [0, 0, 0];
    myend = [10, 10, pi/4.0];
    myrange = arange(0,1,0.01);

    ion()
    for i in range(100):
        myspline = SplineC(mystart, myend, i, i);
        X, Y = myspline.value(myrange);
        plot(X, Y);
        draw();
    
    show()

def test2():
    mystart = [0, 0, 0];
    myend = [10, 10, pi/4.0];
    myrange = arange(0,1,0.01);

    for i in range(1000):
        myspline = SplineC(mystart, myend, i, i);
        X, Y = myspline.value(myrange);
    
if __name__=="__main__":
    test1()


