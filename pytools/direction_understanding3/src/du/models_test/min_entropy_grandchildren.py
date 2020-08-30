from du.dir_util import get_total_turn_amount
from math import pi, radians
from gsl_utilities import tklib_normalize_theta
import min_entropy_extended
import min_entropy
import numpy as na

class model(min_entropy.model):
    
    def get_transition_matrix(self, direction="straight", p_self=1.0 ):
        """
        Use children and grandchildren
        """
        T_mat = na.zeros([self.num_regions*self.num_viewpoints, 
                       self.num_regions*self.num_viewpoints])*1.0
        
        if(direction == "straight"):
            new_tmap = self.get_topological_map_viewpoint(pi, 0)
        elif(direction == "right"):
            new_tmap = self.get_topological_map_viewpoint(pi, -1.0*pi/2.0)
        elif(direction == "left"):
            new_tmap = self.get_topological_map_viewpoint(pi, +1.0*pi/2.0)
        else:
            raise ValueError("Unexpected direction: " + `direction`)
        
        #for each of the viewpoints
        for i in range(len(self.viewpoints)):
            connections = new_tmap[self.viewpoints[i]]
            
            
            #find the areas connected and if they are reasonable            
            for conn in connections:
                cconn = conn 
                connofconn = [conn]
                connofconn.extend(new_tmap[conn])
                
                #if(i==0):
                #    print "start viewpoint:", self.viewpoints[i]
                #    print "tmap:", self.tmap[0.0], "to", self.tmap_locs[11.0]
                #    print "connections", connofconn
                #    raw_input()

                for conn_i, cconn in enumerate(connofconn):

                    #convert this into topo numbers
                    topo_st, topo_st_ang = self.viewpoints[i].split("_")
                    topo_end, topo_end_ang = cconn.split("_")

                    if(cconn < 0 or self.viewpoints[i] == -1):
                        continue
                    elif(topo_st == topo_end):
                        continue

                    loc1 = self.tmap_locs[float(topo_st)]
                    loc2 = self.tmap_locs[float(topo_end)]

                    #for each of the to-node's orientations, check its relative angle to 
                    #          the from node's orientation and give it a relative probability
                    #          accordingly
                    start_num = self.vpt_to_num[self.viewpoints[i]]
                    end_num = self.vpt_to_num[cconn]

                    #make this dependent on how much we turn in total
                    orient_diff, d_turn = get_total_turn_amount(loc1[0], loc1[1], 
                                                                radians(float(topo_st_ang)),
                                                                loc2[0], loc2[1], 
                                                                radians(float(topo_end_ang)))
                    #going to end_num from i
                    if(direction == 'straight'):
                        T_mat[end_num,start_num] = max(-1.75/pi*abs(orient_diff)+1, 0.0)
                        #T_mat[start_num][end_num] = max(-1.5/pi*abs(orient_diff)+1, 0.0)
                    elif(direction == 'right' and d_turn < 0):
                        diff_from_neg_pi2 = tklib_normalize_theta(d_turn*orient_diff+(pi/2.0))
                        T_mat[end_num,start_num] = max(-2.5/pi*abs(diff_from_neg_pi2)+1, 0.0)
                        #T_mat[start_num][end_num] = max(-1.5/pi*abs(diff_from_neg_pi2)+1, 0.0)
                    elif(direction == 'left' and d_turn > 0):
                        diff_from_pi2 = tklib_normalize_theta(d_turn*orient_diff-(pi/2.0))
                        T_mat[end_num,start_num] = max(-2.5/pi*abs(diff_from_pi2)+1, 0.0)
                        #T_mat[start_num][end_num] = max(-1.5/pi*abs(diff_from_pi2)+1, 0.0)

                    if(not conn == cconn):
                        T_mat[end_num,start_num] = T_mat[end_num,start_num]*0.3
                        
            #connect self transitions
            topo_st, topo_st_ang = self.viewpoints[i].split("_")
            if(direction == "straight"):
                T_mat[i,i] = p_self
            elif(direction == "right"):
                newang = na.mod(int(float(topo_st_ang))-int(float(self.get_viewpoint_diff())), 360)*1.0
                T_mat[self.vpt_to_num[str(topo_st)+"_"+str(newang)],i] = p_self
            elif(direction == "left"):
                newang = na.mod(int(float(topo_st_ang))+int(float(self.get_viewpoint_diff())), 360.0)*1.0
                T_mat[self.vpt_to_num[str(topo_st)+"_"+str(newang)],i] = p_self
        
        return T_mat

