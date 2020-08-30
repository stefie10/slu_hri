from du import composedModel
import numpy as na

class model(composedModel.model):
    """
    only use the last sdc
    """
    def __init__(self, m4du):
        composedModel.model.__init__(self, m4du)
        self.viewpoints = m4du.viewpoints

    def infer_path(self, sdcs, loc=None, start_orient_rad=None):
        mysdcs = self.m4du.get_usable_sdc(sdcs)

        for k in range(len(mysdcs)):
            #last_keyword = observations[len(observations)-k-1]

            print "current sdc:", mysdcs[len(mysdcs)-k-1]["landmarks"]
            if(len(mysdcs[len(mysdcs)-k-1]["landmarks"]) > 0):
                last_keyword = mysdcs[len(mysdcs)-k-1]["landmarks"][0]
            else:
                continue
            
            print "doing inference with:", last_keyword
            #raw_input()
            
            try:
                i = na.argmax(self.m4du.O_mat[:,self.m4du.names_to_index[last_keyword]])
                return [self.m4du.viewpoints[i]], self.m4du.O_mat[i,self.m4du.names_to_index[last_keyword]], mysdcs
            except(KeyError):
                print "keyerror for", last_keyword
                raise
        return [], 0.0, []

