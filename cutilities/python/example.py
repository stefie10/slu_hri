from scipy import *
from pyTklib import icp
from pylab import *
from random import *

def test1():
    th2 = arange(pi/4.0,pi+pi/4.0, 0.4)
    th1 = arange(pi/2.0,pi+pi/2.0, 0.4)

    X1 = cos(th1)
    Y1 = sin(th1)

    X2 = cos(th2)
    Y2 = sin(th2)    
    Z = zeros(len(X2))
    
    pts_model = [X1,Y1,Z]
    pts = [X2,Y2,Z]
    new_pts = icp(pts, pts_model, 0.1, 0.1)
    
    plot(X1, Y1, 'ro')
    #plot(X2,Y2, 'rx')

    X, Y, Z = new_pts
    plot(X, Y, 'g<')
    axis('equal')
    show()


def test2():
    #test
    A = transpose(array([[0,0,0],[1,0,0],[1,1,0],[0,1,0]]))

    #model
    B = transpose(array([[0,-0.9,0],[0.9,-0.9,0],[0.9,0.0,0], [0,0,0]]))

    #run icp
    new_pts = icp(A, B, 0.1, 0.1)

    X, Y, Z = A
    #test
    #plot(X, Y, 'ro')
    
    X, Y, Z = B
    #model
    plot(X,Y, 'rx')

    X, Y, Z = new_pts
    
    plot(X, Y, 'g<')
    show()

def test3():


    th1 = arange(pi/4.0,pi+pi/4.0, 0.5)
    th2 = arange(pi/2.0,pi+pi/2.0, 0.5)
    
    print len(th2);
    X1 = cos(th1)
    Y1 = sin(th1)
    
    X2 = cos(th2)
    Y2 = sin(th2)    
    Z = zeros(len(X2))
    
    pts = [X2,Y2,Z]
    pts_model = [X1,Y1,Z]

    new_pts = icp(pts, pts_model, 0.1, 0.1)
        
    #plot(X1, Y1, 'ro')
    plot(X2,Y2, 'rx')
    
    X, Y, Z = pts
    #plot(X, Y, 'g<')
    #show()

if __name__ == "__main__":
    test1()
    #test2()
    
    #test3()

