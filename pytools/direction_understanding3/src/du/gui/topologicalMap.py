from modelBrowser import plot_map_for_model
import cPickle
import pylab as mpl

def main():
    import sys
    figure = mpl.figure(figsize=(14,10))
    model_fname = sys.argv[1]
    m4du = cPickle.load(open(model_fname, 'r'))

    plot_map_for_model(m4du)
    axis = mpl.axis()

    if False:
        for r_st in m4du.tmap_keys:
            sloc = m4du.tmap_locs[r_st]
            for r_end in m4du.tmap[r_st]:
                eloc = m4du.tmap_locs[r_end]
                X, Y = m4du.clusters.skel.compute_path(sloc, eloc)
                mpl.plot(X, Y, '-', linewidth=3, color="black")

    
        pts = [m4du.tmap_locs[r_st] for r_st in m4du.tmap_keys]
    
        X = [x for x, y in pts]
        Y = [y for x, y in pts]
        #mpl.scatter(X, Y, marker=(5,1,0), s=200, c="b", facecolor="white", zorder=10)
        mpl.scatter(X, Y, marker="o", s=100, c="k", facecolor="white", zorder=10)
        

    if True:
        from voom.gui.landmarkSelectorTableModel import plotLandmarks
        print "landmarks"
        plotLandmarks(figure, m4du.clusters.tf, 
                      useText=True, washoutFactor=0)


    mpl.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    mpl.gca().set_axis_off()
    mpl.axis(axis)
    mpl.show()
        
    
if __name__=="__main__":
    main()
