from du.dir_util import *
from du.inference.hri2010_log_gm import hri2010_log_gm
from du.srel_utils import *
from maphacking.trainer import createLandmarkPt
from numpy import *
from probability import normalize
from pyTklib import kNN_index
from scipy import *
import tag_util



class MatrixMetadata:
    def __init__(self, key, **rest):
        self.key = key
        for key, value in rest.iteritems():
            self.__dict__[key] = value


class model(model_prototype_du):
    """
    This one overrides p_can_see_tag with max, and adds an epsilon transition.
    This is the version used in the paper. 
    """
    """
    This uses a fancy modifier model, trying to capture what object
    the landmark is vs what it can see.
    """

    def __init__(self, clusterfile, cachelmap, srelMatFname, map_filename, 
                 tag_filename, **args):
        #model4_du.__init__(self, clusterfile, cachelmap, srelMatFname, map_filename, tag_filename, **args)
        self.use_spatial_relations = True

        self.mygm = None

        model_prototype_du.__init__(self, clusterfile, cachelmap, 
                                    map_filename=map_filename, tag_filename=tag_filename, **args)


        # TODO TK, should this get moved to dir_util? 
        #get the possible locations for objects
        self.obj_names, self.obj_locations, self.obj_geometries = \
            self.get_tag_locations()
        self.obj_to_visibility = self.get_object_to_object_visibility_hash()
        
        
        # doesn't help in greedy.  global inference is broken for this, so fix before trying.
        self.topo_i_to_location_mask = [[]]  # self.get_topo_i_to_location_mask() 
        
        self.srelMatFname = srelMatFname

        print "get_observation_matrix"
        self.O_mat, self.O_mat_oriented = self.get_observation_matrix()
        
        self.L_hash = {}
        print "srel_mat shape", self.srel_mat_expected_shape()
        self.is_initialized = False
        
    def initialize(self):
        self.is_initialized = True
        #initializes self.srel_mat
        self.load_srel_given_lmark_vpts_matrix()
        #self.get_prob_l_can_see_x = memoized(self.get_prob_l_can_see_x)
        #self.get_prob_l_is_x = memoized(self.get_prob_l_is_x)
        #self.p_can_see_tag = memoized(self.p_can_see_tag)
        self.initialize_transition_matrices()
        print "initializing update args"
        self.save_update_args = False

    def initialize_transition_matrices(self):
        #get the relevent transition matricies 
        self.T_mat_str = self.get_transition_matrix("straight")
        self.T_mat_right = self.get_transition_matrix("right")
        self.T_mat_left = self.get_transition_matrix("left")
        #self.T_mat_back = self.get_transition_matrix("back")
        self.T_mat_uniform = self.get_transition_matrix_uniform()

#    @MemoizeInstance
    def p_can_see_tag(self, tag, vtags, itags):
        return self.p_can_see_tag_max(tag, vtags, itags)
    

    def sdc_to_distributions(self, mysdc):
        """
        Convert the SDC to distributions used in the inference.    
        """
        if "right" in  mysdc["verb"]:
            D_mat = transpose(self.T_mat_right)
        elif "left" in mysdc["verb"]:
            D_mat = transpose(self.T_mat_left)
        else:
            D_mat = transpose(self.T_mat_str)
            
        T_mat = ones([len(D_mat), len(D_mat[0])])*1.0
        
        
        if mysdc["sr"] != None and len(mysdc["landmarks"]) > 0 and self.use_spatial_relations:

            sr_i = self.sr_class.engineToIdx(mysdc["sr"])
            SR_mat = self.srel_mat[sr_i,:,:,:]
            L_mat = self.get_prob_landmark_given_sdc_modifiers(mysdc)
            L_mat_entropy = entropy(L_mat)
            print "using spatial relations", str(mysdc)
            if L_mat_entropy > 2 and False:
                SR_mat = None
                L_mat = None
        else:
            SR_mat = None
            L_mat = None
            
        if mysdc["landmark"] != None:
            O_mat = self.O_mat[:,self.names_to_index[mysdc["landmark"]]]
        else:
            O_mat = None
        
        return O_mat, T_mat, SR_mat, L_mat, D_mat

    #more that needs to get merged
    def infer_path(self, sdcs, loc=None, sorient_rad=None, vp_slocs_i=None):
        assert self.is_initialized

        
        print "performing local L_seq opt"
        #T_seq, O_seq, SR_seq, L_seq, newpi, SDC_utilized 
        dists = self.inference_prepare(sdcs, loc, sorient_rad, vp_slocs_i)
        
        T_seq, O_seq, SR_seq, L_seq, D_seq, SDC_utilized, newpi = dists
        #Create the model and perform the inference here
        self.mygm = hri2010_log_gm(SDC_utilized, T_seq, O_seq, SR_seq, L_seq, newpi, self.viewpoints,
                                   self.vp_i_to_topo_i, self.topo_i_to_location_mask,
                                   self.path_lengths, 
                                   len(self.tmap_keys), D_seq,
                                   allow_multiple_sdcs_per_transition=True,
                                   allow_backtracking=self.allow_backtracking)
        print "setting save update args", self.save_update_args
        self.mygm.save_update_args = self.save_update_args
        mypath, myprob = self.mygm.inference_approx()
        #print 'ATTRIBUTE:',dir(self.mygm)
        #mypath, myprob = self.mygm.inference_approx_first_N()
        #return the relevant things
        return mypath, myprob, SDC_utilized


    def infer_destination(self, sdcs, loc, sorient_rad=None, vp_slocs_i=None):
        assert self.is_initialized

        print "preparing inference"
        dists = self.inference_prepare(sdcs, loc, sorient_rad, vp_slocs_i)

        T_seq, O_seq, SR_seq, L_seq, D_seq, SDC_utilized, newpi = dists

        print "performing inference"
        #Create the model and perform the inference here
        self.mygm = hri2010_log_gm(SDC_utilized, T_seq, O_seq, SR_seq, L_seq, newpi, self.viewpoints,
                                   self.vp_i_to_topo_i,
                                   self.topo_i_to_location_mask, 
                                   self.path_lengths,
                                   len(self.tmap_keys), D_seq,
                                   allow_multiple_sdcs_per_transition=True,
                                   allow_backtracking=self.allow_backtracking)
        
        mypath, myprob_log, probs_log = self.mygm.inference_sum_product()

        #return the relevant things
        return mypath, myprob_log, SDC_utilized, probs_log
    

    def infer_path_align(self, sdcs, loc, sorient_rad, num_eps):
        assert self.is_initialized

        mysdcs = create_alignments_sdc(sdcs, num_eps)

        myprobs = []
        mypaths = []
        mysdcs_kw = []
        for sdc in mysdcs:
            path, prob, sdc_utilized = self.viterbi(sdc, loc, sorient_rad)
            myprobs.append(prob)
            mypaths.append(path)
            mysdcs_kw.append(sdc_utilized)

        i = argmax(myprobs)
        
        return mypaths[i], myprobs[i], mysdcs_kw[i]

    
    
    def get_prob_l_can_see_x_strict(self, obj_type):
        """ Only uses vtags and itags"""
        ret_probs = zeros(len(self.obj_names)) + 1e-12
        for i, name in enumerate(self.obj_names):
            vtags, itags_t = self.obj_to_visibility[i]
            vtags = set(vtags)
            itags = set([t for t in itags_t if not t in vtags])

            if obj_type in vtags:
                ret_probs[i] = 1.0
        return ret_probs

#    @MemoizeInstance
    def get_prob_l_can_see_x(self, obj_type):
        """  Use ground truth when available, otherwise backoff to Flickr."""
        if obj_type in self.obj_names:
            return self.get_prob_l_can_see_x_strict(obj_type)
        else:
            return self.get_prob_l_can_see_x_flickr(obj_type)
    
        
    def get_prob_l_can_see_x_flickr(self, obj_type):
        """
        Return the probability that l can see the object type.
        
        Not normalized, because it's independent.  More than one door
        can perfectly well see an elevator. Each element in the vector
        is a probability between zero and one.
        """
        ret_probs = []

        for i in range(len(self.obj_locations[0])):
            #get the visibility here
            vtags, itags_t = self.obj_to_visibility[i]

            itags = []
            for elt_t in itags_t:
                if(not elt_t in vtags and not elt_t in itags):
                    itags.append(elt_t)


            myprob = self.p_can_see_tag(obj_type, vtags, itags)
            if obj_type in vtags:
                myprob = 1.0
            
            ret_probs.append(myprob)
        
        return ret_probs


    def get_prob_l_is_x_strict(self, obj_type):
        """
        For each L, return probability L is X. the returning array
        won't normalize. Each number is a probability between zero and 1. 

        Be strict about it - don't use the flickr cache. there's
        another backoff method for that.
        """
        ret_probs = []

        for i in range(len(self.obj_locations[0])):
            name = self.obj_names[i]
            if name == obj_type:
                myprob = 1.0
            else:
                myprob = 1e-12

            ret_probs.append(myprob)
        return ret_probs

#    @MemoizeInstance
    def get_prob_l_is_x(self, objtype_x):
        if objtype_x in self.obj_names:
            return self.get_prob_l_is_x_strict(objtype_x)
        else:
            return self.get_prob_l_is_x_flickr(objtype_x)


    def get_prob_l_is_x_flickr(self, objtype_x):
        ret_probs = []

        for i in range(len(self.obj_locations[0])):
            #get the visibility here
            vtags, itags_t = self.obj_to_visibility[i]

            itags = []
            for elt_t in itags_t:
                if(not elt_t in vtags and not elt_t in itags):
                    itags.append(elt_t)


            myprob = self.p_can_see_tag(objtype_x, vtags, itags)
            
            ret_probs.append(myprob)
        return ret_probs


    def get_prob_landmark_given_sdc_modifiers(self, sdc):
        """
        for each object, find P(sdc["landmark"] is X), using modifiers in a funky way. 
        """
        l_mat = zeros(len(self.obj_names)) + 0.0
        
        for kw1 in sdc["landmarks"]:
            p_l_is_kw1 = self.get_prob_l_is_x(kw1)
            product_term = array(p_l_is_kw1)
            for kw2 in sdc["landmarks"]:

                if kw1 != kw2:
                    p_l_can_see_kw2 = self.get_prob_l_can_see_x(kw2)
                    product_term *= p_l_can_see_kw2

            l_mat += product_term

        l_mat = l_mat/len(sdc["landmarks"]) # uniform prior on landmarks


        return normalize(l_mat)

    def get_prob_landmark_given_sdc_multiply_landmarks(self, sdc):
        """
        return landmarks that can see all the other keywords. 
        """
        L_mats = [self.get_location_given_obj_vector(l) for l in sdc["landmarks"]]
        L_mat = zeros(L_mats[0].shape) + 1.0
        for l in L_mats:
            L_mat *= l
        return L_mat


    #def viterbi(self, sdcs, loc, sorient_rad=None):
    def get_probability_distributions(self, sdcs):
        #check if they are usable
        if str(type(sdcs[0])).find("instance")>=0:
            SDC_utilized = self.get_usable_sdc(sdcs)
        else:
            SDC_utilized = sdcs
        
        T_seq = []; O_seq = [];
        SR_seq = []; L_seq = []
        D_seq = []
        for i, mysdc in enumerate(SDC_utilized):
            ############################################
            #add the current SDC to the list
            #print "i", i, mysdc
            O_mat, T_mat, SR_mat, L_mat, D_mat = self.sdc_to_distributions(mysdc)
            O_seq.append(O_mat); T_seq.append(T_mat); 
            SR_seq.append(SR_mat); L_seq.append(L_mat);
            D_seq.append(D_mat)

        return T_seq, O_seq, SR_seq, L_seq, D_seq, SDC_utilized    



    def srel_mat_expected_shape(self):
        return srel_mat_expected_shape(self.sr_class,
                                       self.tmap,
                                       self.obj_locations)
    
    def load_srel_given_lmark_vpts_matrix(self):
        self.srel_mat = loadSrelMatrix(self.srelMatFname, self.srel_mat_expected_shape())

    def create_srel_given_lmark_vpts_matrix(self):
        self.srel_mat = get_srel_given_lmark_vpts_matrix(self)
        print "saving", self.srelMatFname
        self.srel_mat.tofile(self.srelMatFname)
        print "done saving", self.srelMatFname
        return self.srel_mat

    def metadataForMatrixKey(self, key, wantArgs=True):
        i, j, k, l = key
        sloc = self.tmap_locs[self.tmap_keys[j]]
        eloc = self.tmap_locs[self.tmap_keys[k]]
        sr = self.spatial_relations[i]
        engine = self.sr_class.engineMap[sr]

        metadata = MatrixMetadata(key, sloc=sloc, eloc=eloc,engine=engine,
                                  groundName=self.obj_names[l])

        if wantArgs:
            metadata.args = {"figure":createFigure(self.clusters, sloc, eloc),
                             "ground":self.createGround(l)}
            
        return metadata

    def get_location_given_obj_vector(self, obj_type):
        if(self.L_hash.has_key(obj_type)):
            return self.L_hash[obj_type]

        ret_probs = []

        for i in range(len(self.obj_locations[0])):
            #get the visibility here
            vtags, itags_t = self.obj_to_visibility[i]

            itags = []
            for elt_t in itags_t:
                if(not elt_t in vtags and not elt_t in itags):
                    itags.append(elt_t)


            myprob = self.p_can_see_tag(obj_type, vtags, itags)
            
            ret_probs.append(myprob)
        
        ret_probs = array(ret_probs)/(sum(ret_probs)+0.000001)
        
        self.L_hash[obj_type] = ret_probs
        return ret_probs


    def get_tag_locations(self):
        #self.clusters.get_topological_map()
        mymap = self.clusters.get_map()
        allp = list(copy(self.clusters.tf.polygons))
        allp.extend(self.clusters.tf.points)

        names = []
        ret_pts = [] 

        for p in allp:
            if(isinstance(p, tag_util.polygon)):
                xp, yp = mymap.to_xy(p.centroid())
            elif(isinstance(p, tag_util.point)):
                xp, yp = mymap.to_xy([p.x, p.y])
            else:
                raise ValueError("error... wrong type for compute_location_probs")
            names.append(p.tag)
            ret_pts.append([xp, yp])

                                 

        return names, transpose(ret_pts), allp
    
    @property
    def orients(self):
        return self.get_viewpoint_orientations(self.num_viewpoints)
    
    def loc_to_idx(self, loc):
        i, = kNN_index(loc, transpose(self.tmap_locs.values()), 1)
        return i
    
    def inference_prepare(self, sdcs, loc=None, start_orients_rad=None, vp_slocs_i=None):
        
        if loc is not None:
            assert vp_slocs_i is None
            ###################################################
            #get the locations and get the nearest
            #    center for the start location
            i, = kNN_index(loc, transpose(self.tmap_locs.values()), 1)
        
            ###################################################
            #now we have to get the region and all the orientations
            #    and initialize all of them as feasible
            #mytopo_i = self.tmap_locs.keys()[int(i)]
            mytopo_i = self.tmap_locs.keys()[int(i)]
            if(start_orients_rad is None or start_orients_rad[0] is None):            
                vp_slocs_i = [self.vpt_to_num[str(mytopo_i)+"_"+str(ang)] for ang in self.orients]
            else:
                vp_slocs_i = [] 
                for start_orient_rad in start_orients_rad:
                    i_tmp, = kNN_index([degrees(start_orient_rad)], [self.orients], 1);
                    myi = self.vpt_to_num[str(mytopo_i)+"_"+str(self.orients[int(i_tmp)])]
                    vp_slocs_i.append(myi)
        else:
            assert vp_slocs_i != None

        newpi = zeros(len(self.O_mat))*1.0
        for vp_i in vp_slocs_i:
            newpi[vp_i] = 0.99


        ###################################################
        #    get the sequence of distributions 
        print "sdcs", sdcs, sdcs[0].__class__
        #T_seq, O_seq, SR_seq, L_seq, SDC_utilized = self.get_probability_distributions(sdcs)
        dists = list(self.get_probability_distributions(sdcs))
        dists.append(newpi)
        
        return dists


    def unload(self):
        self.clusters.unload()

    def createGround(self, l):
        return self.createGroundFromPoint(l)

    def createGroundFromPolygon(self, l):
        obj = self.obj_geometries[l]
        mymap = self.clusters.get_map()
        if(isinstance(obj, tag_util.polygon)):
            if len(obj) <= 2:
                return createLandmarkPt(mymap.to_xy(obj.centroid()))
            else:
                return [mymap.to_xy((x, y)) for x, y in zip(obj.X, obj.Y)]
        elif(isinstance(obj, tag_util.point)):
            return self.createGroundFromPoint(l)
        else:
            raise ValueError("error... wrong type for compute_location_probs")
    
    def createGroundFromPoint(self, l):
        taggedGeom = self.obj_geometries[l]
        isDoor = taggedGeom.tag == "door"
        return createLandmarkPt(self.obj_locations[:, l], isDoor=isDoor)



    

