class model:
    """
    A model that has another model inside it.
    """ 
    
    def __init__(self, m4du):
        self.m4du = m4du
    def initialize(self):
        self.m4du.initialize()
    
    @property
    def tmap_keys(self):
        return self.m4du.tmap_keys
    
    @property
    def tmap_locs(self):    
        return self.m4du.tmap_locs


    @property
    def tmap(self):
        return self.m4du.tmap
    
    @property
    def num_viewpoints(self):
        return self.m4du.num_viewpoints
    
    
    @property
    def clusters(self):
        return self.m4du.clusters
    @property
    def vpt_to_num(self):
        return self.m4du.vpt_to_num
    
    def get_viewpoint_orientations(self, *argl, **argm):
        return self.m4du.get_viewpoint_orientations(*argl, **argm)
