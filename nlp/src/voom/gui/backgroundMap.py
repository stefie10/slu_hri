from voom.gui.recorder import loadTagFile
import cPickle
import carmen_maptools
import pylab as mpl
from environ_vars import TKLIB_HOME

'''
Created on Dec 16, n2009

@author: stefie10
'''

def makeBackground(tagFile):
    
    gridmap = tagFile.map
    print "x, y", gridmap.x_size, gridmap.y_size
    #figure = mpl.figure(figsize=(10,10), dpi=600, frameon=False)
    figure = mpl.figure(frameon=False)
    axes = figure.add_axes([0, 0, 1, 1], frameon=False)
    

    carmen_maptools.plot_map(tagFile.carmen_map, 
                             gridmap.x_size, gridmap.y_size, 
                             cmap="carmen_cmap_white",
                             curraxis=axes)

    from landmarkSelectorTableModel import plotLandmarks
    plotLandmarks(figure, tagFile, useText=False, washoutFactor=0.4)
    mpl.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    
    axes.axis([0, gridmap.x_size, 0, gridmap.y_size])    

    def save():
        axes.set_axis_off()
        fname = "%s/data/directions/stata3_aaai/stata3_aaai.png" % TKLIB_HOME

        print "saving", fname
        mpl.savefig(fname, dpi=200)
        
    save()
    #mpl.show()
    
    #os.system("convert background.pdf background.png")
def main():
    from sys import argv
    map_fn = argv[1]
    gtruth_tag_fn = argv[2]
    skeleton_fn = argv[3]
    
    tagFile = loadTagFile(argv[2], argv[1])
    skeleton = cPickle.load(open(skeleton_fn, 'r'))

    makeBackground(tagFile)
    #mpl.show()
if __name__ == "__main__":
    main()

        
