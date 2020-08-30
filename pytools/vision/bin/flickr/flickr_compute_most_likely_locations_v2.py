from annote_utils import *
from sys import argv
import cPickle
from pyTklib import *
from math import atan2, sqrt, log
from scipy import array, zeros
from pylab import *
import cPickle

#pt is in x, y
#pts are indicies
#mymap is a tklib_log_gridmap
def get_visible_points(pt, pts, mymap):
    x, y = pt 

    visible_pts = []

    for pt in pts:
        xp, yp = mymap.to_xy([pt.x, pt.y]);
        theta = atan2(xp-y, yp-x)
        
        d, = mymap.ray_trace(x, y, [theta])
        d_elt = sqrt((y-yp)**2.0 + (x-xp)**2.0)

        if(d_elt < d):
            visible_pts.append(pt)
        elif(abs(d-d_elt) < 0.2):
            visible_pts.append(pt)

    return visible_pts


def get_visible_polygons(pt, polygons, mymap):
    x, y = pt
    
    visible_polygons = []
    
    for polygon in polygons:

        for i in range(polygon.num_segments()):
            xi, yi = polygon.get_segment(i)
            xp, yp = mymap.to_xy([xi, yi])
            theta = atan2(xp-y, yp-x)
            
            d, = mymap.ray_trace(x, y, [theta])
            d_elt = sqrt((y-yp)**2.0 + (x-xp)**2.0)
            
            if(d_elt < d):
                visible_polygons.append(polygon)
                break
            elif(abs(d-d_elt) < 0.2):
                visible_polygons.append(polygon)
                break
                
    return visible_polygons


def compute_log_posterior(obj_name, prior_cond, prior, vpolygons):
    #print "computing posterior"
    log_num, log_denom = 0.0, 0.0
    for i in range(1,len(vpolygons)):
        tag = vpolygons[i].tag
        tagp = vpolygons[i-1].tag
        
        try:
            log_num += log((prior_cond[obj_name][tag]/(1.0*prior[obj_name])) + 10**(-6.0))
        except:
            log_num += log(10**-6.0)

        try:
            log_denom += log((prior_cond[tagp][tag]/(1.0*prior[tagp])) + 10.0**(-6.0))
        except:
            log_denom += log(10**-6.0)
    
    #print "finishing posterior"
    try:
        log_num += log((prior[obj_name]/ sum(prior.values())) + 10**(-6.0))
    except:
        log_num += log(10**(-6.0))

    return log_num - log_denom, log_num, log_denom


def get_likelihood_map(obj_name, pts, polygons, prior_cond, prior, mymap):
    free_pts =  array(mymap.get_free_locations());
    
    print "w x h", mymap.get_map_width(), mymap.get_map_height()
    likelihood_map = zeros([mymap.get_map_width(), mymap.get_map_height()])*1.0

    #if there are none
    if(len(free_pts) == 0):
        return

    #when we iterate through them
    for i in range(len(free_pts[0])):
        print "i=", i,  " of ", len(free_pts[0]), " grid cells"
        #print "free pts", free_pts
        #print "free pts:", free_pts[:,i]
        x, y = free_pts[:,i]
        vpts = get_visible_points([x,y], pts, mymap)
        vpolys = get_visible_polygons([x,y], polygons, mymap)        
        vpolys.extend(vpts);
        
        i, j = mymap.to_index([x, y])
        #print "i, j-->", i, j

        #compute the posterior
        v, l1, l2 = compute_log_posterior(obj_name, prior_cond, prior, vpolys)
        likelihood_map[i,j]=v
        
        for v in vpolys:
            print v.tag,
        print ""
        #raw_input()
    return likelihood_map
        

        

def compute_most_likely_locations(obj_name, map_filename, 
                                  tag_filename, prior_cond, spline_filename):
    
    print "loading map"
    #load the map
    mymap = tklib_log_gridmap()
    mymap.load_carmen_map(map_filename)
    
    print "loading polygons"
    #load the tag file
    poly, pts = load_polygons(tag_filename)
    #vpts = get_visible_points([46.4,26.2], pts, mymap)

    print "computing prior"
    prior = {}
    for key in prior_cond.keys():
        prior[key] = sum(prior_cond[key].values())

    print "getting likelihood map"
    l_map = get_likelihood_map(obj_name, pts, poly, 
                               prior_cond, prior, mymap)

    gray()
    imshow(l_map)
    show()
    cPickle.dump(l_map, open("test_out.pck", 'w'))

if __name__=="__main__":
    if(len(argv) == 6):
        print "loading prior"
        compute_most_likely_locations(argv[1], argv[2], argv[3], 
                                      cPickle.load(open(argv[4], 'r')),
                                      argv[5])
    else:
        print "usage:\n\t python flickr_compute_most_likely_locations.py obj_name map_file tag_file prior spline_file"



