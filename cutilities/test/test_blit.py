from pylab import *
from time import *
from scipy import mod
import carmen_maptools

ion()

#write down the matrix
A = ones([10, 10])*1.0;
A[0:5,0:5]=0.0

#show the image
im = carmen_maptools.plot_map(A, 40, 40)

#plot it all
for i in range(1000):
    print "i:", i
    A=None
    if(mod(i, 2) == 0):
        A = zeros([10, 10])*1.0;
    else:
        A = ones([10, 10])*1.0;
        A[0:5,0:5]=0.0

    carmen_maptools.plot_map(A, 40, 40, curr_plt=im)
    #im.set_data(A)
    #gcf().canvas.blit()
    draw()

    
