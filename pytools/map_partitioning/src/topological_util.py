from collections import deque
from copy import copy
from scipy import transpose, mod


def compute_topological_map(skel, topo_len):
    print "getting graph"
    G, I = skel.get_graph()
    XY_junct = transpose(skel.get_junction_points()).tolist()
    print "junct:", XY_junct

    visited = dict((i,False) for i in G.keys())
    
    
    #tmap = dict((i,[]) for i in G.keys())
    tmap={}
    sub_paths = []
    myq = deque([[G.keys()[0]]])
    visited[G.keys()[0]] = True  

    print "running"
    iter = 0
    while(len(myq) > 0):
        if(mod(iter, 1000)==0):
            print len(myq)

        #print myq            
        elt = myq.popleft()
        curr_pt = skel.ind_to_xy(transpose([I[:,elt[-1]]]))[:,0].tolist()
        
        #else if the curr path includes a junction point
        if(curr_pt in XY_junct and len(elt) > 1):
            #if(1875 in elt or 1896 in elt or 1905 in elt):
            #    print "new junction: was added as:", elt
            #    raw_input()
            
            sub_paths, tmap = add_to_paths(sub_paths, tmap, elt)

            for conn in G[elt[-1]]:
                if(visited[conn] == False):
                    myq.appendleft([elt[-1], conn])
                    visited[conn] = True
                    #break
        #add a new subpath and create the topology
        elif(len(elt) == topo_len):

            #$if(1875 in elt or 1896 in elt or 1905 in elt):
            #    print "new subpath: was added as:", elt
            #    raw_input()
            sub_paths, tmap = add_to_paths(sub_paths, tmap, elt)
            
            for conn in G[elt[-1]]:
                if(visited[conn] == False):
                    myq.appendleft([elt[-1], conn])
                    visited[conn] = True
                    #break
        #otherwise, add additional elements to the queue
        else:
            #print "add new"
            was_added = False

            for conn in G[elt[-1]]:
                ecp = copy(elt)

                if(tmap.has_key(elt[-1])):
                    pass
                elif(not conn in ecp and not visited[conn]):
                    ecp.append(conn)      
                    myq.appendleft(ecp)
                    visited[conn] = True
                    was_added = True
                elif(not conn in ecp and visited[conn]):
                    #add the final location
                    was_added = True
                    ecp.append(conn)
                    sub_paths, tmap = add_to_paths(sub_paths, tmap, ecp)


                    #if(1875 in elt or 1896 in elt or 1905 in elt):
                    #    print "1896 was visited:", visited[1896]
                    #    print '2: was added as:', ecp
                    #    raw_input()
                        
            
            if(not was_added):
                #if(1875 in elt or 1896 in elt or 1905 in elt):
                #    print "3: was added as:", elt
                #    raw_input()
                sub_paths, tmap = add_to_paths(sub_paths, tmap, elt)

        if(len(myq) == 0 and False in visited.values()):
            #print "other"
            unvisit = get_first_unvisited(visited)
            
            added_elt = False
            for conn in G[unvisit]:
                if(visited[conn]):
                    added_elt = True
                    myq.append([conn, unvisit])
            if(not added_elt):
                myq.append([unvisit])
            
            visited[unvisit] = True

        #if(1875 in elt or 1896 in elt or 1905 in elt):
        #    print elt
        #    raw_input()
        
        iter+=1
    return tmap, sub_paths, skel.ind_to_xy(I)

def add_to_paths(sub_paths, tmap, elt):
    sub_paths.append(elt)
    
    myst = elt[0]
    myend = elt[-1]
    
    if(not tmap.has_key(myend)):
        tmap[myend] = []
    if(not tmap.has_key(myst)):
        tmap[myst] = []
            
    if(not myst in tmap[myend]):
        tmap[myend].append(myst)
    if(not myend in tmap[myst]):
        tmap[myst].append(myend)
    
    return sub_paths, tmap


def get_first_unvisited(visited):
    for elt in visited.keys():
        if(visited[elt] == False):
            return elt

def compute_xy_ind_to_ppath_ind(topo_paths):
    XY_ind_to_path_ind_ext = {}
    XY_ind_to_path_ind_center = {}
    for i in range(len(topo_paths)):
        for j in topo_paths[i]:
            if(XY_ind_to_path_ind_ext.has_key(j)
               and (topo_paths[i][0] == j or topo_paths[i][-1] == j)):
                XY_ind_to_path_ind_ext[j].append(i)
            elif(topo_paths[i][0] == j or topo_paths[i][-1] == j):
                XY_ind_to_path_ind_ext[j] = [i]
            elif(XY_ind_to_path_ind_center.has_key(j)):
                XY_ind_to_path_ind_center[j].append(i)  
            else:
                XY_ind_to_path_ind_center[j] = [i]
                
    #for key in XY_ind_to_path_ind_center.keys():
    #    if(not XY_ind_to_path_ind_ext.has_key(key)):
    #        XY_ind_to_path_ind_ext[key] = XY_ind_to_path_ind_center[key]

    return XY_ind_to_path_ind_ext, XY_ind_to_path_ind_center
