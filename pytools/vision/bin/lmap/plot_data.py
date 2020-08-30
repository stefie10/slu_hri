from pylab import *
import cPickle
from scipy import maximum

mylmap = cPickle.load(open('test_out.pck'))


gray()
imshow(mylmap)
title("zebra")

show()
