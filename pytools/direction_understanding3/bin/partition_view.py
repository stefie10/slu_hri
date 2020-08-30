from pylab import *
from sys import argv
import cPickle
import carmen_maptools
from map_partitioning2_0 import show_explosion, show_partitions
from scipy.io.mmio import *
from scipy.io import savemat

def partition_view(clusters):
    #load the map
    gridmap = clusters.get_map()
    themap = gridmap.to_probability_map_carmen();

    
    for i in range(clusters.numkmeans):
        #ion()
        figure()
        title(str(i))
        carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);

        #temporary
        #clusters.gridcell_skip = 25.0

        tmap, tmap_cnt, tmap_locs = clusters.get_topological_map(i)
        
        newtmap = {}
        for elt in tmap.keys():
            newtmap[str(elt)] =  array(tmap[elt])

        newtmap_locs = {}
        for elt in tmap_locs.keys():
            newtmap_locs[str(elt)] =  array(tmap_locs[elt])
        print newtmap_locs
        savemat('tmap.mat', newtmap)
        savemat('tmap_locs.mat', newtmap_locs);
        
        X, Y = [], []
        for loc_st_i in tmap_locs.keys():
            for loc_end_i in tmap[loc_st_i]:
                if(loc_st_i == -1 or loc_end_i == -1):
                    continue
                xy_st = tmap_locs[loc_st_i]
                xy_end = tmap_locs[loc_end_i]

                #vtags, itags = clusters.tf.compute_visibility_tag(xy_st[0], 
                #                                                  xy_st[1])
                #print vtags
                #vtags, itags = clusters.tf.compute_visibility_tag(xy_end[0],
                #                                                  xy_end[1])
                #print vtags
                
                plot([xy_st[0], xy_end[0]], [xy_st[1], xy_end[1]], 'ro-')
                #draw()
                #raw_input()
        figure()
        title(str(i))
        show_explosion(clusters)
        figure()
        title(str(i))
        show_partitions(clusters.get_map(), 
                        clusters.samples, clusters.mylabels[i])

        figure()
        clusters.skel.G = None
        topo_map_view_fullpaths(clusters)
        
    show()


def topo_map_view_fullpaths(clusters):
    #load the map
    gridmap = clusters.get_map()
    themap = gridmap.to_probability_map_carmen();

    
    for i in range(clusters.numkmeans):
        #ion()
        figure()
        title(str(i))
        carmen_maptools.plot_map(themap, gridmap.x_size, gridmap.y_size);

        #temporary
        #clusters.gridcell_skip = 25.0

        tmap, tmap_cnt, tmap_locs = clusters.get_topological_map(i)
        
        TXY = []
        for loc_st_i in tmap_locs.keys():
            for loc_end_i in tmap[loc_st_i]:
                if(loc_st_i == -1 or loc_end_i == -1):
                    continue
                xy_st = tmap_locs[loc_st_i]
                xy_end = tmap_locs[loc_end_i]

                XY = clusters.skel.compute_path(xy_st, xy_end)
                XY_tmp = transpose(XY).tolist()
                XY_fin = [xy_st]
                XY_fin.extend(XY_tmp)
                XY_fin.append(xy_end)
                XY_fin = transpose(XY_fin)

                #print "xy_start:", xy_st
                #print "xy_end:", xy_end
                #print "path:", XY
                #raw_input()
                
                plot(XY_fin[0],XY_fin[1], 'k-', linewidth=2.0)

            TXY.append(tmap_locs[loc_st_i])
            
        
        plot(transpose(TXY)[0], transpose(TXY)[1], 'ro', markersize=9)



if __name__ == "__main__":
    if(len(argv) >= 2):
        m=cPickle.load(open(argv[1], 'r'))
        print "m", m
        print "class", m.__class__
        if len(argv) > 2:
            m.skel.map_filename = argv[2]
        
        partition_view(m)

    else:
        print "usage:\n\tpython partition_view.py clusters.pck"
