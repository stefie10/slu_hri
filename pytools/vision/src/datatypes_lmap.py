from carmen_maptools import *
from annote_utils import *
import sys
from sys import argv
import sys
import cPickle
from pyTklib import *
from pylab import *
import cPickle
from math import *
from scipy import *
from carmen_util import load_carmen_logfile
from tag_util import tag_file 
from classifier_util import *
from glob import glob
from mpmath import mpf, exp, log

class likelihood_map:
    def __init__(self, known_classes, flickr_cache, mylogfile, num_iterations=50):
        #deprecated
        #self.path_pts = self.mylogfile.get_path_pts()
        #self.path_pts_unique = self.mylogfile.path_pts_unique        
        
        self.flickr_cache = flickr_cache
        self.mylogfile = mylogfile
        
        self.likelihood_map = {}
        self.object_names = self.mylogfile.get_object_list()
        self.known_classes = known_classes
        self.num_bp_iterations = num_iterations

    def get_lmap(self, object_name):
        
        gridmap = self.mylogfile.get_map()
        
        ix = gridmap.get_map_width()
        iy = gridmap.get_map_height()
        
        lmap = zeros([ix,iy])*1.0
        
        I = self.mylogfile.xy_to_ind(self.mylogfile.path_pts_unique)
        
        for i in range(len(I[0])):
            ix, iy = I[:,i]
            lmap[ix,iy]=self.likelihood_map[object_name][i]
            
        return lmap

    def get_lmap_nn(self, object_name, minval=0.0):
        xyFree =  array(self.mylogfile.get_map().get_free_locations());
        indFree =  array(self.mylogfile.get_map().get_free_inds());
        
        if(len(xyFree) == 0):
            return None
        
        #make the gridmap
        ix = self.mylogfile.get_map().get_map_width()
        iy = self.mylogfile.get_map().get_map_height()
        lmap = zeros([ix,iy])*1.0


        #get the nearest neighbors
        try:
            print "got cache"
            I = self.I_nn
        except:
            print "starting nearest neighbors"
            self.I_nn = NNs_index(xyFree, self.mylogfile.path_pts_unique)
            I = self.I_nn
            
        print "filling out lmap"
        #fill out the likelihood map
        for i in range(len(I)):
            #print i
            #print indFree[:,i]
            ix, iy = indFree[:,i]
            
            v = self.likelihood_map[object_name][int(I[i])]

            if(v > minval):
                lmap[ix,iy] = v

        print self.likelihood_map[object_name]
        print "object_name", object_name
        raw_input("press something")

        return lmap


    def get_lmap_nn_orient(self, object_name):
        xyFree =  array(self.mylogfile.get_map().get_free_locations());
        indFree =  array(self.mylogfile.get_map().get_free_inds());
        
        if(len(xyFree) == 0):
            return None
        
        #make the gridmap
        ix = self.mylogfile.get_map().get_map_width()
        iy = self.mylogfile.get_map().get_map_height()
        lmap0 = zeros([ix,iy])*1.0
        lmap90 = zeros([ix,iy])*1.0
        lmap180 = zeros([ix,iy])*1.0
        lmap270 = zeros([ix,iy])*1.0


        #get the nearest neighbors
        try:
            print "got cache"
            I = self.I_nn
        except:
            print "starting nearest neighbors"
            self.I_nn = NNs_index(xyFree, self.mylogfile.path_pts_unique)
            I = self.I_nn
            
        print "filling out lmap"
        #fill out the likelihood map
        for i in range(len(I)):
            ix, iy = indFree[:,i]
            
            lmap0[ix,iy] = self.likelihood_map0[object_name][int(I[i])]
            lmap90[ix,iy] = self.likelihood_map90[object_name][int(I[i])]
            lmap180[ix,iy] = self.likelihood_map180[object_name][int(I[i])]
            lmap270[ix,iy] = self.likelihood_map270[object_name][int(I[i])]

        return lmap0, lmap90, lmap180, lmap270


    def MAP(self):
        MAP = []
        
        for i in range(len(self.likelihood_map[self.likelihood_map.keys()[0]])):
            max_class = "";
            max_val = -10000;
            print "*************"
            all_zero = True
            for elt in self.likelihood_map.keys():
                print elt, self.likelihood_map[elt][i]
                if(self.likelihood_map[elt][i] > max_val):
                    max_val = self.likelihood_map[elt][i]
                    max_class = elt

                if(self.likelihood_map[elt][i] < 0.0):
                    all_zero = False

            if(all_zero == True):
                print "adding unknown"
                print "*******************"
                MAP.append('unknown')
            else:
                MAP.append(max_class)

        return MAP


def check_prior_keys(prior, keylist=None):
    """
    Check that all the keys are symmetric, but don't require all entries to be.
    """
    if keylist == None:
        keylist = prior.keys()
    for key1 in keylist:
        for key2 in keylist:
            assert prior[key1][key2] == prior[key2][key1], (key1, key2)

def check_prior_sparse(prior):
    """
    check that prior[key1][key2] always equals prior[key2][key1]
    """
    print "checking prior (", len(prior), "entries)"
    for key1 in prior.keys():
        for key2 in prior[key1].keys():
            assert key2 in prior, key2
            try:
                assert prior[key1][key2] == prior[key2][key1]
            except:
                print "key1", key1
                print "key2", key2
                print "prior[key1]", prior[key1]
                print "prior[key2]", prior[key2]

                print "prior[key1][key2]", prior[key1][key2]
                print "prior[key2][key1]", prior[key2][key1]
                raise

def make_symmetric(prior):
    """
    There are entries where prior[key1][key2] exists, but not key2 in prior.
    This fixes that problem by putting in the corresponding entries. 
    """
    print "making symmetric"

    new_map = {}
    for key1 in prior.keys():
        for key2 in prior[key1].keys():
            if not key2 in prior:
                new_map.setdefault(key2, {})
                new_map[key2][key1] = prior[key1][key2]

    for key in new_map:
        assert not key in prior
        prior[key] = new_map[key]
    print "fixed", len(new_map), "entries"

def fill_in_empty_tags(prior, tags):
    """
    Fill in the tags that aren't already in the prior with 0/empty maps
    """
    print "filling in empty entries for tags"
    for key in tags:
        if not key in prior:
            prior[key] = {}
    for key1 in tags:
        for key2 in tags:
            prior[key1].setdefault(key2, 0.0)

def smooth_tags(prior, tags):
    """ Smooth tags by adding 1 to everything."""
    print "smoothing tags"
    for key1 in prior.keys():
        for key2 in tags:
            if key2 in prior[key1]:
                prior[key1][key2] += 1
                prior[key2][key1] += 1


class flickr_cache:
    def __init__(self, prior, tagnames=None):

        if(tagnames == None):
            self.tagnames=prior.keys()
        else:
            self.tagnames = tagnames
            self.prior = {}
        

        make_symmetric(prior)
        fill_in_empty_tags(prior, self.tagnames)        
        #smooth_tags(prior, self.tagnames)
        check_prior_sparse(prior) 
        check_prior_keys(prior, self.tagnames) 

        for elt in self.tagnames:
            self.prior[elt] = prior[elt]

        self._p_obj = {}
        self.overall_total_entries = sum([sum([v for v in prior[obj].values()]) 
                                          for obj in prior.keys()])*0.5
        
        print "saving priors", len(self.prior.keys())
        for i, key in enumerate(self.prior.keys()):
            self._p_obj[key] = (mpf(sum([v for v in prior[key].values()])*1.0) /
                                self.overall_total_entries)
            
            print "%.2f%% done" % (100.0 *i/len(self.prior.keys()))

        
        self.mins = {}
        self.means = {}
        self.variances = {}
        self.sums = {}
        self.lengths = {}
        print "computing statistics"
        for elt in self.prior.keys():
            if(len(self.prior[elt].keys()) == 0):
                self.sums[elt] = 0;
                self.means[elt] = 0;
                self.mins[elt] = 0;
                self.lengths[elt] = 0;
                self.variances[elt] = 0;
                continue

            self.means[elt] = mean(self.prior[elt].values())
            self.mins[elt] = min(self.prior[elt].values())
            self.sums[elt] = sum(self.prior[elt].values())
            self.lengths[elt] = len(self.prior[elt].values())
            self.variances[elt] = var(self.prior[elt].values())

        self.total_entries = sum(self.lengths.values())*1.0
        self.total_objects = sum(self.sums.values())
        self.global_mean = sum(self.sums.values())*1.0/self.total_entries
        self.category_mean = mean(self.sums.values())

        print "computing global variance"
        self.global_variance = 0
        for elt in self.prior.keys():
            self.global_variance += sum((array(self.prior[elt].values())-self.global_mean)**2.0)
        self.global_variance = self.global_variance / self.total_entries
        self.category_variance = var(self.sums.values())

        print "getting hashes"
        #compute the probability of this pair
        #self.no_prob = log(1.0/(1.0+exp(-1.0*(0.0-self.category_mean-1)/self.category_variance)))
        self.pos_log_prob, self.neg_log_prob = self.get_log_prob_hashes()

        # the filtered prior doesn't hold the real invariant,
        # but this one should still hold. 
        
                
        check_prior_keys(self.prior)

 
    #e.g. self.get_val("cup", True, "mug", False)
    def get_val(self, oname, valo, ogiven, valg):
        #raw_input("press enter")
        try:
            if(valo == True and valg == True 
               and not isnan(self.pos_log_prob[oname][ogiven])):
                #print "getting prob 1", self.pos_log_prob[oname][ogiven]
                return self.pos_log_prob[oname][ogiven]
            elif(valo == False and valg == True 
                 and not isnan(log(1.0-exp(self.pos_log_prob[oname][ogiven])))):
                #print "getting prob 2", log(1.0-exp(self.pos_log_prob[oname][ogiven]))
                return log(1.0-exp(self.pos_log_prob[oname][ogiven]))
            elif(valo == True and valg == False and
                 not isnan(self.neg_log_prob[oname][ogiven])):
                #print "getting prob 3", self.neg_log_prob[oname][ogiven]
                return self.neg_log_prob[oname][ogiven]
            elif(valo == False and valg == False 
                 and not isnan(log(1.0-exp(self.neg_log_prob[oname][ogiven])))):
                #print "getting prob 4", log(1.0-exp(self.neg_log_prob[oname][ogiven]))
                return log(1.0-exp(self.neg_log_prob[oname][ogiven]))
        except(KeyError):
            if(((valo == True and valg == False) or (valo == True and valg == True)) 
               and not isnan(log(1.0) -  log(self.sums[ogiven]+1.1))):
                #print "keyerror 1", log(1.0) -  log(self.sums[ogiven]+1.1)
                return log(1.0) -  log(self.sums[ogiven]+1.1)
            elif(not isnan(log(1.0 - exp(log(1.0) - log(self.sums[ogiven]+1.1))))):
                #print "keyerror 2", log(1.0 - exp(log(1.0) - log(self.sums[ogiven]+1.1)))
                return log(1.0 - exp(log(1.0) - log(self.sums[ogiven]+1.1)))

        print "returning junk"
        sys.exit(0)
        #return log(1.0/(1.0*len(self.tagnames)))


    def get_val_unnorm(self, oname, valo, ogiven, valg):
        try:
            if(valo == True and valg == True):
                #print self.prior[oname][ogiven]
                return (self.prior[ogiven][oname] + self.prior[oname][ogiven])/2.0
            elif(valo == False and valg == True):
                #print self.prior[oname][ogiven]
                #return log(1.0-exp(selfp.os_log_prob[oname][ogiven]))
                #self.sums[ogiven]-self.prior[ogiven][oname]
                #return max(self.means[ogiven]-self.prior[ogiven][oname],1) 
                return self.means[ogiven]
            elif(valo == True and valg == False):
                #print self.prior[oname][ogiven]
                #return self.neg_log_prob[oname][ogiven]
                #return self.sums[oname]-self.prior[ogiven][oname]
                #return max(self.means[oname]+self.prior[ogiven][oname],1)
                return self.means[oname]
            elif(valo == False and valg == False):
                #return self.total_objects - self.sums[ogiven] - self.sums[oname]
                return self.global_mean;
        except(KeyError):
            if(valo == True and valg == True):
                return 1
            elif(valo == False and valg == True):
                #print "error", self.sums[ogiven]
                return self.means[ogiven]
            elif(valo == True and valg == False):
                #print "error", self.sums[oname]
                return self.means[oname]
            elif(valo == False and valg == False):
                #print "total:", self.total_objects
                return self.global_mean


    def get_val_exp(self, oname, valo, ogiven, valg):
        mymin = self.mins[ogiven]
        mu = self.means[ogiven]
        s = self.variances[ogiven]

        if(s == 0):
            #print "ogiven=", ogiven, " std = ", s, " mu=", mu, " mymin=", mymin
            #raw_input()
            s = 100000
        
        try:
            val = (self.prior[ogiven][oname] + self.prior[oname][ogiven])/2.0
        except:
            val = -5

        #print "val=", val
        retval = None
        if(valo == True and valg == True):
            #print "1:",  1.0/(1.0+exp(-1.0*(val-mu-mymin)/s ))
            retval = 1.0/(1.0+exp(-1.0*(val-mu-mymin)/s ))
        elif(valo == False and valg == True):
            #print "2:", 1.0 - 1.0/(1.0+exp(-1.0*(val-mu-mymin)/s ))
            retval =  1.0 - 1.0/(1.0+exp(-1.0*(val-mu-mymin)/s ))
        elif(valo == True and valg == False):
            #print "3:", 1.0 - 1.0/(1.0+exp(-1.0*(val-mu-mymin)/s ))
            retval =  1.0 - 1.0/(1.0+exp(-1.0*(val-mu-mymin)/s ))
        elif(valo == False and valg == False):
            #print "4:", 1.0/(1.0+exp(-1.0*(val-mu-mymin)/s))
            retval = 1.0/(1.0+exp(-1.0*(val-mu-mymin)/s))

        if(retval == 0.0):
            retval+=10**-200

        return retval

            
    def get_log_prob_hashes(self):
    
        pos_hash = {}
        neg_hash = {}


        for elt in self.tagnames:
            pos_hash[elt] = {}
            neg_hash[elt] = {}

        for i in range(len(self.tagnames)):
            print "getting i, ", i, " of ", len(self.tagnames)
            for j in range(i, len(self.tagnames)):
                #if(mod(j, 500) == 0):
                #    print "getting j, ", j, " of ", len(self.tagnames)

                if(self.tagnames[i] == self.tagnames[j]):
                    pos_hash[self.tagnames[i]][self.tagnames[j]] = log(0.999999)
                    pos_hash[self.tagnames[j]][self.tagnames[i]] = log(0.999999)
                    neg_hash[self.tagnames[i]][self.tagnames[j]] = log(0.000001)
                    neg_hash[self.tagnames[j]][self.tagnames[i]] = log(0.000001)
                    continue
                #elif(not self.tagnames[j] in self.prior[self.tagnames[i]].keys()):
                #    #print "tagname not found", self.tagnames[j], " in ", self.tagnames[i]
                #    continue

                p1 = self.get_pos_prob(self.tagnames[i], self.tagnames[j])
                p2 = self.get_neg_prob(self.tagnames[i], self.tagnames[j])
                p3 = self.get_pos_prob(self.tagnames[j], self.tagnames[i])
                p4 = self.get_neg_prob(self.tagnames[j], self.tagnames[i])
                
                #print self.tagnames[i], self.tagnames[j]
                #print "p_pos", exp(p1), exp(p3)
                #print "p_neg", exp(p2), exp(p4)
                #raw_input()

                if(not p1 == None):
                    pos_hash[self.tagnames[i]][self.tagnames[j]] = p1
                if(not p2 == None):
                    neg_hash[self.tagnames[i]][self.tagnames[j]] = p2
                if(not p3 == None):
                    pos_hash[self.tagnames[j]][self.tagnames[i]] = p3
                if(not p4 == None):
                    neg_hash[self.tagnames[j]][self.tagnames[i]] = p4

        return pos_hash, neg_hash

    #this is the probability of oi being true given os = true
    def get_pos_prob(self, oi, os):
        if(not self.prior.has_key(os) 
           or not self.prior[os].has_key(oi)):
            return None
        
        #compute the current value of this pair
        val = self.prior[os][oi]*1.0
        my_prob = log(val) - log(self.sums[os]*1.0)
        
        #print my_prob
        #raw_input()
        return my_prob


    #this is the probability of oi being true given os = false and oi = true
    '''def get_pos_neg_prob(self, oi, os):
        if(not os in self.prior.keys()):
            print "bad context name", os
            sys.exit(0)
        
        my_prob = 0.0
        
        #compute the current value of this pair
        try:
            val = self.prior[os][oi]
            #my_prob = log(self.sums[oi]-val) - log(self.sums[os])
            my_prob = log(self.sums[os]-val) - log(self.sums[os])

            if(exp(my_prob) > 1.0):
                print "invalid val 1", os, oi
                print exp(my_prob)
                raw_input()
            
            #compute the mean, variance and minimum
            #mu = self.means[os]
            #mymin = self.mins[os]
            #v = self.variances[os]
            
            #compute the probability of this pair
            #my_prob = log(1.0/(1.0+exp(-1.0*(val-mu-mymin)/v)))


        except(KeyError):
            return None
        
        #except:
        #    my_prob = log(0.5)
                    
        
        return my_prob'''

    #this is the probability of oi being true given os = false
    def get_neg_prob(self, oi, os):
        if(not self.prior.has_key(os) 
           or not self.prior[os].has_key(oi)):
           #or not self.prior.has_key(oi)):
            return None

        obj_cnt = (self.sums[os]-self.prior[os][oi])*1.0
        
        norm = (self.total_objects - self.sums[os])*1.0

        #if(exp(log(obj_cnt) - log(norm)) > 1.0):
        #    print "invalid val 2", oi, os
        #    print exp(log(obj_cnt) - log(norm))
        #    #raw_input()

        return log(obj_cnt) - log(norm)

    def p_obj1_given_no_obj2(self, obj1, obj2):
        """
        prob of seeing obj1 given that we can't see obj2
        """
        if obj2 in self.prior[obj1]:
            obj1_and_obj2_count = self.prior[obj1][obj2]
        else:
            obj1_and_obj2_count = 0

        p = (self.sums[obj1] - obj1_and_obj2_count) / float(self.total_objects - obj1_and_obj2_count)
        assert 0 <= p and p <= 1, (p, obj1, obj2)
        return p

    def p_obj1_given_obj2(self, obj1, obj2):
        """
        prob of seeing obj1 given that I can see obj2"
        """
        if not obj2 in self.sums:
            raise ValueError("Object " + `obj2` + " not in self.sums.")

        if self.sums[obj2]  != 0:
            return self.prior[obj2][obj1] / float(self.sums[obj2])
        else:
            return self.prior[obj2][obj1] / (float(self.sums[obj2])+1.0)
    

    def p_obj1(self, obj1, prior=None, total=None):
        """
        prob of seeing an object.
        """
        if prior == None:
            prior = self.prior
        return (mpf(sum([v for v in prior[obj1].values()])) / 
                (sum([sum([v for v in prior[obj].values()]) for obj in prior.keys()])*0.5))
    



class logfile_lmap:
    def __init__(self, logfilename, 
                 mapfilename, tag_filename, image_dir,               #pts_tag, polys_tag, 
                 tp=1.0, tn=1.0, seed=1):


        self.flaser, self.rlaser, self.tpos = load_carmen_logfile(logfilename)
        self.map_filename = mapfilename
        self.gridmap = None
        
        self.tfile = tag_file(tag_filename, mapfilename)
        #self.tags_pts = pts_tag
        #self.tags_polys = polys_tag

        self.tp = tp
        self.tn = tn
        tklib_init_rng(seed)

        self.path_pts = self.get_path_pts()
        
        #get the path points as well as their indicies
        ppts = self.get_unique_path_pts()
        self.path_pts_unique, self.path_pts_to_unique_index, self.unique_to_path_pts = ppts
        
        #get the visible objects for each direction
        myvisible = self.get_visible(self.path_pts_unique)
        self.visible_objects, self.vobjs0, self.vobjs90, self.vobjs180, self.vobjs270 = myvisible

        #get the path pts
        self.path_pts_unique_nn = self.get_neighbors()
        self.image_to_laser_mapping = self.associate_images(image_dir)
        
        '''print "image to laser mapping"
        for elt in self.image_to_laser_mapping.keys():
            print elt, self.image_to_laser_mapping[elt]
            raw_input()'''

        #if(pclass_filename != None and  image_dir != None and class_type != None):
        #    #image number to classifications
        #    self.det_type = class_type
        #    self.class_tp = class_tp
        #    self.class_tn = class_tn
        #    self.detections = self.associate_classifications(pclass_filename, image_dir)

    def load_timestamps(self, dirname):
        ts_filenames = glob(dirname + "/*.txt")
        ts_filenames.sort()
    
        print "loading timestamps"
        image_timestamps = {}
        for fn in ts_filenames:
            fh = open(fn, 'r')
            ts_str = fh.readline().split(':')[1]
            ts = float(ts_str)
            imnum = int(fn.split("/")[-1].split(".")[0])
            #print imnum, ts
            #raw_input()
            image_timestamps[imnum] = ts
            fh.close()

        return image_timestamps

    def associate_images(self, dirname):
        #load the image timestamps
        image_timestamps = self.load_timestamps(dirname)
    
        #associate the flaser data with the image data
        image_to_laser_mapping = {}        
        
        #sort the classifications by their number
        mykeys = image_timestamps.keys()
        mykeys.sort()

        fread_i = 0
        #iterate through all of the image numbers in the classificaitons
        for imnum in mykeys:
            im_ts = image_timestamps[imnum]
        
            if(fread_i >= len(self.flaser)):
                break
        
            while(im_ts/1000000.0 > self.flaser[fread_i].timestamp):
                fread_i += 1
                if(fread_i >= len(self.flaser)):
                    break

            if(fread_i <= 0):
                continue;
            
            #myloc = self.flaser[fread_i-1].location.x, self.flaser[fread_i].location.y
            #j = self.path_pts_to_unique_index[fread_i-1]

            image_to_laser_mapping[imnum] = fread_i -1

        return image_to_laser_mapping
        

    def get_neighbors(self):
        ind_nn  = []
        print "getting neighbors"
        for i in range(len(self.path_pts_unique[0])):
            #print i, " of ", len(self.path_pts_unique[0])
            loc1 = self.path_pts_unique[:,i]
            loc1_NN_indexes = kNN_index(loc1, self.path_pts_unique, 9);

            ind_nn.append(loc1_NN_indexes)

        return ind_nn


    def get_visible(self, free_pts):
        my_vobjs = []
        my_vobjs0, my_vobjs90, my_vobjs180, my_vobjs270 = [], [], [], [] 

        print "getting visible"
        for i in range(len(free_pts[0])):
            print i, " of ", len(free_pts[0])
            x, y = free_pts[:,i]

            #plot([x],[y], 'ro')
            #draw()
            
            vobjs = self.get_visible_objects([x,y])
            vobjs0 = self.get_visible_objects_orientation([x,y], 0, pi/2.0)
            vobjs90 = self.get_visible_objects_orientation([x,y], pi/2.0, pi/2.0)
            vobjs180 = self.get_visible_objects_orientation([x,y], pi, pi/2.0)
            vobjs270 = self.get_visible_objects_orientation([x,y], (3*pi)/2.0, pi/2.0)

            my_vobjs.append(vobjs)
            my_vobjs0.append(vobjs0)
            my_vobjs90.append(vobjs90)
            my_vobjs180.append(vobjs180)
            my_vobjs270.append(vobjs270)

            print "vobjs"
            for elt in vobjs:
                print elt.tag

            print "vobjs0"
            for elt in vobjs0:
                print elt.tag

            print "vobjs90"
            for elt in vobjs90:
                print elt.tag

            print "vobjs180"
            for elt in vobjs180:
                print elt.tag

            print "vobjs270"
            for elt in vobjs270:
                print elt.tag
            #raw_input()
        
        return my_vobjs, my_vobjs0, my_vobjs90, my_vobjs180, my_vobjs270

    def get_path_pts(self):
        path_pts = self.ind_to_xy(self.get_path_indices())

        return path_pts

    def get_unique_path_pts(self):
        path_pts = self.get_path_pts()
        
        free_pts = []
        free_pts_to_unique_index = {}
        unique_to_free_pts_index = {}

        p_list = transpose(path_pts).tolist()

        i = 0; j = 0;
        for elt in p_list:
            if(not elt in free_pts):
                free_pts.append(elt)
                j+=1
            
            try:
                unique_to_free_pts_index[j-1].append(i)
            except(KeyError):
                unique_to_free_pts_index[j-1] = [i]
            free_pts_to_unique_index[i] = j-1
        
            i+=1
        free_pts = transpose(free_pts)
        return free_pts, free_pts_to_unique_index, unique_to_free_pts_index


    def get_path_indices(self):
        mymap = self.get_map()
        I = []
        for elt in self.flaser:
            x, y = elt.location.x, elt.location.y
            ind = mymap.to_index([x,y])

            I.append(ind)
        return transpose(I)


    def ind_to_xy(self, I):
        if(len(I) == 0):
            return None
        
        XY = []
        mymap = self.get_map()
        for j in range(len(I[0])):
            #print "index", I[:,j]
            XY.append(mymap.to_xy(I[:,j]))
            
        return transpose(XY)


    def xy_to_ind(self, XY):
        if(len(XY) == 0):
            return None
        
        I = []
        mymap = self.get_map()
        for j in range(len(XY[0])):
            I.append(mymap.to_index(XY[:,j]))
            
        return transpose(I)

    def get_map(self):
        if(self.gridmap==None):
            self.gridmap  = tklib_log_gridmap()
            self.gridmap.load_carmen_map(self.map_filename);
        
        return self.gridmap

    def get_object_list(self):
        return self.tfile.get_tag_names()


    def compute_overlap(self, curr_pos, next_pos):
        mymap = self.get_map()
        
        I1 = self.compute_visible_indicies(mymap, curr_pos)
        I2 = self.compute_visible_indicies(mymap, next_pos)
        
        present = 0
        for elt in I1:
            if(elt in I2):
                present+=1
                
        return present/(1.0*len(I1))

    def compute_overlap_orient(self, curr_pos, next_pos, orient, fov):
        mymap = self.get_map()
        
        I1 = self.compute_visible_indicies_orient(mymap, curr_pos, orient, fov)
        I2 = self.compute_visible_indicies_orient(mymap, next_pos, orient, fov)
        
        present = 0
        for elt in I1:
            if(elt in I2):
                present+=1
                
        return present/(1.0*len(I1))


    def compute_visible_indicies_orient(self, mymap, curr_pos, orient, fov):
        D = mymap.ray_trace(curr_pos[0], curr_pos[1], 
                            linspace((orient-fov)/2.0,(orient+fov)/2.0,360/4.0))
        
        Angles = linspace((orient-fov)/2.0,(orient+fov)/2.0,360/4.0)

        X1 = D*cos(Angles)+curr_pos[0]
        Y1 = D*sin(Angles)+curr_pos[1]
        
        I1 = []
        
        for i in range(len(X1)):
            ind1 = mymap.to_index([X1[i],Y1[i]])
            I1.append(ind1)
            
        return I1

    def compute_visible_indicies(self, mymap, curr_pos):
        D = mymap.ray_trace(curr_pos[0], curr_pos[1], linspace(0,2*pi,360))
        
        X1 = D*cos(linspace(0,2*pi,360))+curr_pos[0]
        Y1 = D*sin(linspace(0,2*pi,360))+curr_pos[1]
        
        I1 = []
        
        for i in range(len(X1)):
            ind1 = mymap.to_index([X1[i],Y1[i]])
            I1.append(ind1)
            
        return I1


    def get_visible_objects(self, loc):
        x, y = loc

        vpts, vpolys, ipts, ipolys = self.tfile.compute_visibility(x, y)

        vpolys.extend(vpts);
        ipolys.extend(ipts);
        
        ipolys_fin = []
        ipolys_names = []
        #check that no two objects are repeated
        
        for elt in ipolys:
            repeat = False

            for elt2 in vpolys:
                if(elt2.tag == elt.tag):
                    repeat = True

            if(not repeat and not elt.tag in ipolys_names):
                ipolys_fin.append(elt)
                ipolys_names.append(elt.tag)

        finpolys = []
        for myelt in vpolys:
            if(tklib_random() <= self.tp):
                finpolys.append(myelt)
        for myelt in ipolys_fin:
            if(tklib_random() > self.tn):
                finpolys.append(myelt)


        #compute the posterior
        return finpolys


    def get_visible_objects_orientation(self, loc, theta, fov):
        x, y = loc

        vpts, vpolys, ipts, ipolys = self.tfile.compute_visibility_orient(x, y, theta, fov)

        vpolys.extend(vpts);
        ipolys.extend(ipts);
        
        ipolys_fin = []
        ipolys_names = []
        #check that no two objects are repeated
        
        for elt in ipolys:
            repeat = False

            for elt2 in vpolys:
                if(elt2.tag == elt.tag):
                    repeat = True

            if(not repeat and not elt.tag in ipolys_names):
                ipolys_fin.append(elt)
                ipolys_names.append(elt.tag)

        finpolys = []
        for myelt in vpolys:
            if(tklib_random() <= self.tp):
                finpolys.append(myelt)
        for myelt in ipolys_fin:
            if(tklib_random() > self.tn):
                finpolys.append(myelt)


        #compute the posterior
        return finpolys
        


if __name__ == "__main__":
    if(len(argv) == 3):
        myl = logfile_lmap(argv[1], argv[2])
        print "path indicies"
        print myl.get_path_indices()
        print "ind to xy"
        print myl.ind_to_xy(myl.get_path_indices())
        print "xy to ind"
        print myl.xy_to_ind(myl.ind_to_xy(myl.get_path_indices()))
        
        plot_map(myl.get_map().to_probability_map_carmen() , 
                 myl.get_map().x_size, myl.get_map().y_size)

        myXY = myl.ind_to_xy(myl.get_path_indices())
        plot(myXY[0], myXY[1], 'b--')
        plot([myXY[0][0]], [myXY[1][0]], 'ro')
        plot([myXY[0][-1]], [myXY[1][-1]], 'go')
        show()
        
    else:
        print "usage:\n\tpython logfile mapfile"


