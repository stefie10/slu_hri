from pyTklib import *
from pylab import *
from gaussian import *

def test1():
    #test me here
    pts = []
    for i in range(100):
        pts.append(normal_sample([[3, 0], [0,3]], [0,0]))
    for i in range(100):
        pts.append(normal_sample([[3, 0], [0,3]], [10,-10]))

    test_pts = pts
    pts = array([[0, 10], [0, -10]])

    ion()
    nn_plt, = plot([], [], 'ro', markersize=10);
    pt_plt, = plot([], [], 'go', markersize=10);
    plot(pts[0,:], pts[1,:], 'kx');
    
    for pt in test_pts:
        print "start"
        ret_pts = kNN(pt, pts, 2);
        ret_pts = array(ret_pts);
        nn_plt.set_data([ret_pts[0,0]], [ret_pts[1,0]]);
        pt_plt.set_data([pt[0]], [pt[1]]);
        axis([-5,15, -15, 5])
        draw()

        print ret_pts
        #raw_input()
    show()


if __name__=="__main__":
    test1()
