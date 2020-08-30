import Image
from glob import glob
from sys import argv
from pylab import *

def flickr_plot_nneighbors(mydir):
    
    myfiles = glob(mydir+"/*_small.jpeg")
    
    i = 0
    for myfile in myfiles:
        print "opening:", myfile
        im = Image.open(myfile)
        im2 = im.resize((32, 32), Image.ANTIALIAS)

        subplot(7,7,i)
        imshow(im2, origin=0)
        axis('off')
        i+=1

    show()
        



if __name__=="__main__":
    if(len(argv) == 2):
        flickr_plot_nneighbors(argv[1])

    else:
        print "usage:\n\tpython flickr_plot_nneighbors folder_name"

