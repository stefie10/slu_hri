from pyTklib import *
from pylab import *
from gaussian import *
from probability import *
import kmeans

def test1():
    #test me here
    pts = []
    for i in range(100):
        pts.append(normal_sample([[3, 0], [0,3]], [0,0]))
    for i in range(100):
        pts.append(normal_sample([[3, 0], [0,3]], [10,-10]))
    for i in range(100):
        pts.append(normal_sample([[3, 0], [0,3]], [10,10]))
    for i in range(100):
        pts.append(normal_sample([[3, 0], [0,3]], [20,20]))
    pts = transpose(pts)
    means = kmeans_autoinit(pts, 15, 4)
    labels = kmeans_get_labels(pts, means)

    std = 1
    res = kmeans_get_log_likelihood(pts, means, labels, std)
    print "log likelihood C:", res
    res = kmeans.kmeans_get_neg_log_likelihood(array(pts), array(means), array(labels), std)
    print "log likelihood python:", res
    
    colors = ['r', 'g', 'b', 'y', 'm']
    types = ['o', 'x', '>', '<']
    
    for j in range(len(means[0])):
        X, Y = [],[]
        for i in range(len(labels)):
            if(labels[i]==j):
                X.append(pts[0][i])
                Y.append(pts[1][i])

        plot(X,Y,colors[j]+types[j])

        plot([means[0][j]], [means[1][j]], "k"+types[j], markersize=10)
    show()

def test_sample_discrete():
    P = [0.1, 0.2, 0.3, 0.4]
    
    count_hash = {0:0, 1:0, 2:0, 3:0}
    
    for i in range(100):
        #print sample_discrete(P, 1);
        count_hash[tklib_sample_discrete(P, 1)[0]]+=1;

    print count_hash

def test_get_distances():
    X = [[1, 2, 3, 4, 5],
         [1, 2, 3, 4, 5]]
    pts = transpose([[0,0]])

    print kmeans_get_distances(X, pts)

def test_get_mean():
    X = [[1, 2, 3, 4, 5],
         [0, 1, 2, 3, 4]]

    labels = [0,0,1,1,1]
    
    print kmeans_compute_mean(X, labels)


if __name__=="__main__":
    print "**********************"
    print "**sample discrete*****"
    test_sample_discrete()

    print "**********************"
    print "***get distances*****"
    test_get_distances()

    print "**********************"
    print "********get mean******"
    test_get_mean()

    print "**********************"
    print "*****kmeans test******"
    test1()
