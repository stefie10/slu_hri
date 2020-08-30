from carmen_maptools import *
from sys import argv
import basewindow
import cPickle
matplotlib.use("Qt4Agg")




class Clicker:
    def __init__(self, mskel):
        self.startP = None

        self.mskel = mskel
    def onClick(self, event):
        print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.button, event.x, event.y, event.xdata, event.ydata)
        if self.startP is None:
            self.startP = event.xdata, event.ydata
            mpl.plot(self.startP, 'go')

        else:
            startP = self.startP
            self.startP = None
            endP = event.xdata, event.ydata
            mpl.plot(endP, 'go')
            print "Drawing"
            X, Y = self.mskel.compute_path(startP, endP)
            mpl.plot(X, Y, 'yx-')
            #mpl.show()
            
def graphMap(mskel, points):
    """
    Graph tk's map, with a clicker enabled to select the start and end
    points.
    """

    #print "figure", mpl
    #print "figure", mpl.figure
    fig = mpl.figure()
    sloc = points[0]
    eloc = points[-1]
    #mpl.plot([sloc[0]],[sloc[1]], 'go')
    #mpl.plot([eloc[0]],[eloc[1]], 'ro')
    print "getting map"
    gm = mskel.get_map()
    print "get pm map"
    mymap = gm.to_probability_map_carmen()
    clicker = Clicker(mskel)
    fig.canvas.mpl_connect('button_press_event', clicker.onClick)
    X = [x for x, y  in points]
    Y = [y for x, y in points]

    #mpl.plot(X, Y, 'yx-')
    plot_map(mymap, gm.x_size, gm.y_size)
    mpl.show()

def cleanPolygons(polygons):
    """
    """

def main():
    if(len(argv) == 3):
        app = basewindow.makeApp()
        print "loading"

        #mapPartitioner = cPickle.load(open('../data/directions/direction_floor_8/partitions/d8_small.pck'))
        mapPartitioner = cPickle.load(open('../data/directions/direction_floor_8/partitions/d8_small.pck'))
        print "loaded", mapPartitioner
        mapPartitioner.skel.map_filename = argv[2]
        mapPartitioner.tf.map_filename = argv[2]
        
        polygons = mapPartitioner.tf.as_slimd_polygons()
        sloc = (20, 25)
        eloc = (21, 38)
        X, Y = mapPartitioner.skel.compute_path(sloc, eloc)
        points = [(x, y) for x, y in zip(X, Y)]
        
        graphMap(mapPartitioner.skel, points)
        #mskel = mapPartitioner.skel
        
        #get path

        #wnd = pathDescriberWindow.makeWindow(polygons, [points])
        #wnd.show()
        

        print "firstPoint", points[0]
        #points = [p for p in zip(X,Y)]
        #wnd.generateInstructions(points)
        
        

        retval = app.exec_()
        
    else:
        print "usage:\n\t python skel_shortest_path.py skeleton.pck map.cmf.gz"

if __name__=="__main__":
    main()
