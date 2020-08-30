from pyTklib import tklib_log_gridmap, kNN_index
from gsl_utilities import tklib_euclidean_distance 
from map_partitioning2_0 import show_graph, partition_map
from map_partitioning2_0 import partition_map_semantic, show_partitions
from map_partitioning2_0 import show_explosion, get_colors, show_graph_no_map, is_visible
import carmen_maptools
from sys import argv
from pylab import *
from scipy import *
from cPickle import load, dump
from tag_util import tag_file
import math
import numpy

class map_partitioner:
    """
    alpha - controls number of clusters.  higher values of alpha mean
    more nodes.
    """
    def __init__(self, skel_filename, alpha=1.0, 
                 num_classes=None, num_samples=None,
                 numkmeans=1, gridcell_skip=15.0, 
                 map_filename=None,seed_number=987):
        self.skel_filename = skel_filename
        self.num_classes = num_classes
        self.num_samples = num_samples
        self.alpha = alpha
        self.tmap = {}
        self.tmap_cnt = {}
        self.tmap_locs = {}
        self.numkmeans = numkmeans
        self.gridcell_skip = gridcell_skip
        self.seed_number=seed_number
        
        #self.gridmap = None
        print "loading skeleton", self.skel_filename
        self.skel = load(open(self.skel_filename, 'r'))
        if map_filename != None:
            self.skel.map_filename = map_filename

    def get_map(self):
        return self.skel.get_map()
    
    def run(self):
        res = partition_map(self.get_map(),
                            self.skel,
                            self.numkmeans,
                            self.alpha,
                            self.num_classes,
                            self.num_samples,
                            seed_number=self.seed_number);

        self.samples, self.mylabels, self.k, self.dists = res

        #print this is new
        for i in range(len(self.mylabels)):
            self.mylabels[i] = self.get_connected_components(self.samples, self.mylabels[i])
        
        self.labels = self.mylabels[0]
        
    def get_topological_bounding_boxes(self,numkmean=0):
        free_locs, free_inds, labels = self.get_labeled_map()

        #get a hash from the mapindex to the list of indices
        print "creating hash"
        mapind2index = zeros(amax(free_inds, axis=1))-1
        for i, elt in enumerate(free_inds):
            mapind2index[elt[0],elt[1]]=i

        landmarks = []
        curr_index = 0
        done = zeros(len(free_locs[0]), dtype='bool')
        while(True):
            print curr_index, "of->", len(free_locs[0])
            if(curr_index >= len(free_locs[0])-1):
                break
            elif(done[curr_index] == True):
                curr_index+=1
                continue
            
            #initialize the current landmark
            curr_landmark = []
            curr_label = None
            for i in range(len(free_locs[0])):
                v = self.count_label_boundary(free_locs[:,i], labels[i], mapind2index, labels)
                
                if(v <= 6 and done[i] != True):
                    curr_landmark.append(i)
                    done[i] = True
                    curr_label = labels[i]
                    break
                elif(done[i] == False):
                    done[i] = True

            if(len(curr_landmark) == 0):
                break

            
            #want to trace around the neighbors of each location
            #  ignoring ones that are in the internal of a region
            #  and following ones that are not
            landmark_complete = False
            while(not landmark_complete):
                mdn = self.get_minimum_degree_neighbor(free_inds[:,curr_landmark[-1]], 
                                                       curr_label, 
                                                       mapind2index, labels, done)
                print "ind_loc", mdn
                
                
                if(mdn[0] >= len(mapind2index) 
                   or mdn[1] >= len(mapind2index[0])):
                    landmark_complete = True
                    continue
                elif(mapind2index[mdn[0]][mdn[1]]==curr_landmark[0] 
                     and len(curr_landmark) > 3):
                    landmark_complete = True
                    continue
                
                print "index", mapind2index[mdn[0]][mdn[1]]
                raw_input()
                
                curr_landmark.append(mapind2index[mdn[0]][mdn[1]])
                done[mapind2index[mdn[0]][mdn[1]]] = True
                
            
            for i, c in enumerate(labels):
                if(c == curr_label):
                    done[i] = True
            
            landmarks.append(curr_landmark)
            curr_index+=1
        
        return landmarks

    def get_minimum_degree_neighbor(self, map_ind, curr_label, mi2ind, labels_I, visited_I):
        neighs = self.get_neighbors(map_ind)
        
        vals = []
        for n in neighs:
            if(n[0] < len(mi2ind) and n[1] < len(mi2ind[0])):
                print "n[0], n[1]", n[0], n[1]
                print "mi2ind[n[0], n[1]]", mi2ind[n[0]][n[1]]
            
            if(n[0] < len(mi2ind) and n[1] < len(mi2ind[0]) and 
               mi2ind[n[0]][n[1]] >= 0 and 
               not visited_I[int(mi2ind[n[0]][n[1]])]
               and labels_I[int(mi2ind[n[0]][n[1]])] == curr_label):
                v = count_label_boundary(n, curr_label, mi2ind, labels_I)
                vals.append(v)
            else:
                vals.append(float('inf'))
                
        i = argmin(vals)
        print "neighbors:", neighs
    
        return neighs[i]
            

    def count_label_boundary(self, map_ind, curr_label, mi2ind, labels_I):
        neighs = self.get_neighbors(map_ind)
        
        num_labels = 0
        for n in neighs:
            i = int(mi2ind[n[0]][n[1]])
            if(i >= 0 and labels_I[i] == curr_label):
                num_labels += 1
        
        return num_labels
    
    
    def get_labeled_map(self,numkmean=0):
        
        #get the open locations
        free_locs = array(self.get_map().get_free_locations());
        free_inds = array(self.get_map().get_free_inds())
        
        index_labels = []
        curr_labels = self.mylabels[numkmean]
        
        for i in range(len(free_locs[0])):
            indicies = kNN_index(free_locs[:,i], self.samples, len(self.samples[0]));
            
            found = False
            for j in indicies:
                #we can see this pt from the current location
                if(is_visible(self.samples[:,int(j)], free_locs[:,i], self.get_map())):
                    index_labels.append(curr_labels[int(j)]);
                    found = True
                    break
                
            if(found == False):
                #label this location with the closest location if 
                #    none are visible
                index_labels.append(-1)
                print "not found", i
                
        return free_locs, free_inds, index_labels


    

    def get_topological_map(self, numkmean=0):
        """
        Returns a triple o tmap, tmap_cnt, tmap_locs.
        
        tmap is a dict.  keys are nodes in the map.  values are lists of destination nodes.
        tmap_cnt unknown
        tmap_locs is a map from node to x,y location
        """
        
        try:
            tm = self.tmap[numkmean] 
            tc = self.tmap_cnt[numkmean] 
            tl = self.tmap_locs[numkmean]
            return tm, tc, tl
        except(KeyError):
            pass
        
        #get the map... labelled
        free_locs, free_inds, index_labels = self.get_labeled_map(numkmean)
        
        
        free_ind_hash = {}
        for i in range(len(free_inds[0])):
            free_ind_hash[str(free_inds[:,i])] = i 

        
        mygraph = {}
        mygraphcnt = {}
        mygraphloc = {}
        for i in range(len(free_locs[0])):
            if(mod(i, 1000) == 0):
                print i, "/", len(free_locs[0])
            
            if(index_labels[i] == -1):
                print "skipping", i
                
                continue

            #get the neighbors

            neighs = self.get_neighbors(free_inds[:,i])
            
            for j in range(len(neighs[0])):

                #get the actual value of the element
                elt = None
                if(free_ind_hash.has_key(str(neighs[:,j]))):
                    elt = free_ind_hash[str(neighs[:,j])]
                else:
                    continue

                if index_labels[elt] == -1:
                    continue

                #add to the counts
                if(not mygraphcnt.has_key(index_labels[i])):
                    mygraphcnt[index_labels[i]] = {}
                if(not mygraphcnt[index_labels[i]].has_key(index_labels[int(elt)])):
                    mygraphcnt[index_labels[i]][index_labels[int(elt)]]=1
                if(not mygraphcnt.has_key(index_labels[int(elt)])):
                    mygraphcnt[index_labels[int(elt)]] = {}
                if(not mygraphcnt[index_labels[int(elt)]].has_key(index_labels[i])):
                    mygraphcnt[index_labels[int(elt)]][index_labels[i]] =1
                
                mygraphcnt[index_labels[int(elt)]][index_labels[i]]+=1
                mygraphcnt[index_labels[i]][index_labels[int(elt)]]+=1
                
                
                #add to the neighbors if we haven't already
                if(mygraph.has_key(index_labels[i])):
                    if(not index_labels[int(elt)] in mygraph[index_labels[i]] and
                       mygraphcnt[index_labels[i]][index_labels[int(elt)]] > self.gridcell_skip):
                        mygraph[index_labels[i]].append(index_labels[int(elt)])
                    mygraphloc[index_labels[i]].append(free_locs[:,i])
                else:
                    #mygraph[index_labels[i]] = [index_labels[int(elt)]]
                    mygraph[index_labels[i]] = []
                    mygraphloc[index_labels[i]] = [free_locs[:,i]]

        
        
        for region_from in mygraph.keys():
            for region_to in mygraph[region_from]:
                if(not region_from in mygraph[region_to]):
                    mygraph[region_to].append(region_from)
        
        locs = {}
        for key in mygraphloc.keys():
            loc = sum(transpose(mygraphloc[key]), 1)/(1.0*len(mygraphloc[key]))
            locs[key] = loc

        for key in mygraph.keys():
            mygraph[key] = array(mygraph[key])


        return mygraph, mygraphcnt, locs
        
    def get_neighbors(self, elt):
        #first create a hash from the index-based location to the 
        myinds = []
        
        myinds.append(elt - [0,1]);
        myinds.append(elt + [0,1]);
        myinds.append(elt - [1,1]);
        myinds.append(elt + [1,1]);
        myinds.append(elt - [1,0]);
        myinds.append(elt + [1,0]);
        myinds.append(elt - [-1,1]);
        myinds.append(elt + [1,-1]);

        return transpose(myinds)


    def get_connected_components(self, locations, labels):
        adj_matrix = self.dists #self.get_adj_matrix(locations)
        
        all_categories = []
        print "labels", labels
        for k in range(int(max(labels))+1):
            #make a hash of the current categories
            numGroup = 0
            curr_categories = {}
            for i in range(len(locations[0])):
                if(labels[i] == k):
                    #process the label here by splitting groups
                    isGrouped = False
                    for key in curr_categories.keys():
                        for elt in curr_categories[key]:
                            if(adj_matrix[i,elt] > 0):
                                curr_categories[key].append(i)
                                isGrouped = True
                                break;
                        if(isGrouped == True):
                            break;
                    
                    #process categories that are not grouped
                    if(not isGrouped):
                        curr_categories[numGroup] = [i]
                        numGroup += 1

            all_categories.append(curr_categories)

        #now make the topological areas
        curr_grp = 0
        fin_labels = zeros(len(locations[0]))-1.0
        for i in range(len(all_categories)):
            for mykey in all_categories[i].keys():
                G_I = all_categories[i][mykey]
                fin_labels[G_I] = zeros(len(G_I))+curr_grp
                curr_grp += 1
        
        return fin_labels

        

    def get_adj_matrix(self, locations):
        adj_matrix = zeros([len(locations[0]), len(locations[0])])*1.0
        
        for i in range(len(locations[0])):
            for j in range(len(locations[0])):
                if(is_visible(locations[:,i], locations[:,j], self.get_map())):
                    adj_matrix[i,j] = 1
        
        return adj_matrix

    def get_topological_distance_graph(self):
        tmap, tmap_cnt, tmap_locs = self.get_topological_map()
        
        mygraph = {}
        
        for topo1 in tmap.keys():
            mygraph[topo1] = {}
            
            for topo2 in tmap[topo1]:
                XY = self.skel.compute_path(tmap_locs[topo1], 
                                            tmap_locs[topo2])
                #print "integrate path"
                mygraph[topo1][topo2]=integrate_path(XY)

        return mygraph


def integrate_path(XY):
    D = 0
    for i in range(1, len(XY[0])):
        d = tklib_euclidean_distance(XY[:,i-1], XY[:,i]);
        D += d
    return D
        
        

class map_partitioner_semantic(map_partitioner):
    
    def __init__(self, skel_filename, tagfilename, 
                 alpha=1.0, num_classes=None, num_samples=None, 
                 numkmeans=1, gridcell_skip=15.0, 
                 map_filename=None,seed_number=987, augment_tmap=False):

        print "loading map partitioner"
        map_partitioner.__init__(self, skel_filename, 
                                 alpha, num_classes, 
                                 num_samples,numkmeans,gridcell_skip,
                                 map_filename,seed_number=seed_number)

        print "loading tagfile"
        self.tf = tag_file(tagfilename, self.skel.map_filename)
        self.augment_tmap = augment_tmap
        
    def run(self):
        print self.get_map()
        res = partition_map_semantic(self.get_map(),
                                     self.tf,
                                     self.skel,
                                     self.numkmeans,
                                     self.alpha,
                                     self.num_classes,
                                     self.num_samples,
                                     seed_number=self.seed_number)
        self.samples, self.mylabels, self.k, self.dists = res
        
        for i in range(len(self.mylabels)):
            self.mylabels[i] = self.get_connected_components(self.samples, self.mylabels[i])
        
        self.labels = self.mylabels[0]
        
        for i in range(self.numkmeans):
            if self.augment_tmap:
                self.tmap[i], self.tmap_cnt[i], self.tmap_locs[i] = self.get_topological_map_augmented(i)
            else:
                self.tmap[i], self.tmap_cnt[i], self.tmap_locs[i] = self.get_topological_map(i)

    def get_topological_map_augmented(self, numkmean=0):
        print 'changed'
        mygraph, mygraphcnt, locs = self.get_topological_map(numkmean)
        gridmap = self.get_map()
        
        print 'Augmenting over', len(mygraph), 'nodes and',len(self.tf.points),'points'
        new_nodes = {}
        for pt in self.tf.points:
            min_dist = float('inf')
            nearest_visible = None

            for node in mygraph:
                xy = gridmap.to_xy([pt.x,pt.y])
                print 'matcing pt:',xy,'with loc:',locs[node]
                dist = math.hypot(xy[0] - locs[node][0], xy[1] - locs[node][1])
                print 'distance:',dist
                if(dist > min_dist):
                    continue
                if self.tf.is_visible_point(locs[node], pt):
                    if dist < min_dist:
                        min_dist = dist
                        nearest_visible = node

            if nearest_visible != None:
                print 'adding node',pt.tag
                new_nodes[pt] = nearest_visible

        for pt in new_nodes:
            new_node = float(len(mygraph))
            nearest_visible = new_nodes[pt]
            mygraph[nearest_visible] = numpy.append(mygraph[nearest_visible],new_node)
            mygraph[new_node] = numpy.array([new_node, nearest_visible])
            locs[new_node] = numpy.array(gridmap.to_xy([pt.x,pt.y]))
            mygraphcnt[new_node] = 1

        return mygraph, mygraphcnt, locs
                        
    def unload(self):
        self.skel.gridmap = None
        self.tf.map = None

    
