from pyTklib import procrustes
from scipy import arange, pi, cos, sin, zeros, transpose, dot, array
from pylab import *
from scipy_addons import *

def test1():
    th1 = arange(0.0, pi, 0.1)
    th2 = arange(pi/2.0,pi+pi/2.0, 0.1)
    
    X1 = cos(th1)
    Y1 = sin(th1)
    
    X2 = cos(th2)
    Y2 = sin(th2)    

    
    measured_pts = transpose(zip(X1,Y1))
    p1 = procrustes()
    
    #run procrustes
    p1.run(measured_pts, transpose(zip(X2, Y2)));
    X, Y = p1.get_rotated_points()
    plot(X2,Y2, 'rx')

    #X, Y, Z = pts
    plot(X, Y, 'g<')
    
    show()


def test2():
    p1 = procrustes()

    
    t1 = arange(-1,1,0.5);
    t2 = ones(len(t1))*1.0
    
    X_top = array([t1,t2])
    X_left = array([-1.0*t2, t1])
    X_right = array([t2, t1])
    X_bottom = array([t1,-1.0*t2])

    first = matrix_concatenate(X_right, X_top)
    second = matrix_concatenate(X_top, X_left)

    p1.run(first, second);
    X, Y = p1.get_rotated_points()
    
    plot(second[0],second[1], 'rx')

    plot(X, Y, 'g<')

    show()


def test3_icp():
    th1 = arange(0.0, pi, 0.1)
    th2 = arange(pi/2.0,pi+pi/2.0, 0.1)
    
    X1 = cos(th1)
    Y1 = sin(th1)
    
    X2 = cos(th2)
    Y2 = sin(th2)    

    
    measured_pts = transpose(zip(X1,Y1))
    #run procrustes
    X, Y = icp(measured_pts, transpose(zip(X2, Y2)), 0.01, 0.1);


    plot(X2,Y2, 'rx')

    #X, Y, Z = pts
    plot(X, Y, 'g<')
    
    show()

if __name__=="__main__":
    test1()
    #test2()
    #test3_icp()
